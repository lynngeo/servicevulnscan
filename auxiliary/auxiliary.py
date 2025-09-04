from os import TMP_MAX
import requests
import socket
import json
import random

from tld import is_tld
from re import fullmatch
from urllib.parse import urlparse
from contextlib import contextmanager
from requests.exceptions import TooManyRedirects

from auxiliary.logs import logger
from config import Pattern, ScanConfig, UrlConfig
from config import DataConfig
from .connection import REQ_DICT, CONNECTION
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def toolthread_decorator(func):
    def wrapper(*args, **kwargs):
        logger.log("INFOR", f'{args[0]}检测线程启动')
        func()
        logger.log("INFOR", f'{args[0]}检测线程结束')

    return wrapper


def handle_requests(payload: str, request: dict) -> dict:
    """
        handle payload and the dict of request we get,substitude exact position of string in request with payload,
    return handlelist which finished handle
    Params:
        payload:str the payload to be substitute_payload
        requestlist:dict the dict of request
    Return:
        handlelist:dict after handle
    """
    try:
        # for request in requestlist:
        if request["method"] == "POST":
            contentype = request["headers"]["Content-Type"]
            if contentype == 'application/x-www-form-urlencoded':
                datas = request["data"].split("&")
                if datas == ['']:
                    return None
                datadict, datadict2 = {}, {}
                # handle data
                for data in datas:
                    data = data.split("=")
                    datadict[data[0]] = data[1]
                flag = False
                for key, value in datadict.items():
                    if key in DataConfig.filter_data:
                        datadict2[key] = value
                        flag = True
                    else:
                        datadict2[key] = payload
                if not flag:
                    return None
                datadict = datadict2
                # joint data
                newdata = ""
                lendata = len(datadict)
                i = 0
                for key, value in datadict.items():
                    newdata += key+"="+value
                    if i < lendata-1:
                        newdata += "&"
                        i += 1

                request["data"] = newdata
                return request
            else:
                return None
        else:
            return None
    except Exception as e:
        logger.log('ERROR', e)


def orig_reqhandle(method, url, headers, data):
    """
    splice request data to origin request format
    Params:
        method:str http method,like "GET" "POST"
        url:str http url
        headers: dict http headers
        data: str http data
    Return:
        org_req:str
    """
    parseurl = urlparse(url)
    orig_req = ""
    if parseurl.query:
        orig_req += method+" "+parseurl.path+"?" + parseurl.query+" "+"HTTP/1.1"+"\r\n"
    else:
        orig_req += method+" "+parseurl.path+" "+"HTTP/1.1"+"\r\n"

    for key, value in headers.items():
        orig_req += key+": "+value+"\r\n"

    if data != "":
        orig_req += "\r\n" + data + "\n"
    return orig_req


def orig_reshandle(response):
    """
    splice response data to origin response format
    Params:
        response:str http response
    Return:
        org_req:str

    """
    orig_res = ""
    orig_res += "HTTP/1.1 " + str(response.status_code) + "\r\n"
    for key, value in response.headers.items():
        orig_res += key+": "+value+"\r\n"
    if response.text != "":
        orig_res += "\r\n" + response.text+"\n"
    return orig_res


def request(request_dict: dict) -> tuple:
    '''
        返回原始请求和响应
    '''
    logger.log('DEBUG', f'{request_dict}')
    s = requests.session()
    s.keep_alive = False
    url = request_dict['url']
    headers = request_dict['headers']
    data = request_dict['data']
    method = request_dict['method']
    originreq = orig_reqhandle(method, url, headers, data)
    if method == 'GET':
        try:

            response = s.get(url,
                             headers=headers,
                             verify=False,
                             timeout=15,
                             )

            originres = orig_reshandle(response)
            return originreq, originres
        except requests.exceptions.ConnectionError as e:
            logger.log('ALERT', f'连接失败：{e}')
        except Exception as e:
            logger.log('ERROR', f'{e}')

    elif method == 'POST':
        try:
            response = s.post(url,
                              data=data,
                              headers=headers,
                              verify=False,
                              timeout=15,
                              )
            originres = orig_reshandle(response)
            return originreq, originres
        except Exception as e:
            logger.log('ERROR', f'{e}')
    else:
        print('存在其他HTTP方法请求，暂不支持')


def body_conversion(content_type: str, body: dict) -> any:
    '''
        根据content_type转化body为相应格式
        Args:
            content_type:str
            body:dict 请求体
        Return:
            body:Any
    '''
    if content_type == "application/json":
        return json.dumps(body)
    elif content_type == "application/x-www-form-urlencoded":
        return body
    elif content_type == "multipart/form-data":
        pass
    elif content_type == "text/plain":
        return body
    else:
        return


def check_api_status(api: str, method: str):
    '''判断api是否可用

    判断api状态是否为 200

    Args:
        url

    Returns:
        可用：
            原url 或 格式化后的url
        不可用：
            None

    '''
    method = method.lower()

    try:
        res_api = REQ_DICT.get(method)(url=api, timeout=30)

    except requests.exceptions.SSLError:
        try:
            res_api = REQ_DICT.get(method)(url=api, timeout=30, verify=False)
        except Exception:
            res_api = None
    except Exception:
        res_api = None
    try:
        res_code = res_api.status_code
        if res_code == 404:
            logger.log("ALERT", "API地址不可用")
            return {"code": 204}
    except AttributeError as e:
        logger.log('ALERT', f'无法连接到目标主机')
        return {"code": 204}
    except Exception as e:
        logger.log("ALERT", f"状态码解析失败，错误原因：{e}")
        return {"code": 204}
    return {"code": 200}


def check_url(url: str) -> any:
    '''判断URL格式是否正确

    Args:
        url

    Returns:
        正确：
            原url 或 格式化后的url
        不正确：
            None

    '''

    if not url.startswith('http'):
        if url.count(':') > 1:  # 判断用户输入的异常url
            return None
        url = 'http://' + url

    try:
        url_parse_res = urlparse(url)
    except Exception:
        logger.log('ALERT', 'URL解析失败：{0}'.format(
            url
        ))
        return None
    else:
        netloc = url_parse_res.netloc
        _netloc = netloc.split(":")

        if len(_netloc) > 2:
            logger.log('ALERT', '错误的netloc：{0}'.format(
                netloc
            ))
            return None

        if len(_netloc) == 2:
            netloc = _netloc[0]
            port_str = _netloc[1]
            if not port_str.isdigit():
                logger.log('ALERT', '错误的端口：{0}'.format(
                    port_str
                ))
                return None

            try:
                port_int = int(port_str)
            except Exception:
                logger.log('ALERT', '端口转换为Int时失败：{0}'.format(
                    port_str
                ))
                return None

            if port_int <= 0 or port_int >= 65536:
                logger.log('ALERT', '端口大小不合法：{0}'.format(
                    port_int
                ))
                return None

        if fullmatch(Pattern.DOMAIN_PATTERN, netloc) and check_domain(netloc):
            return url
        elif fullmatch(Pattern.IP_PATTERN, netloc):
            return url
        else:
            return None


def check_url_status(url):
    '''判断URL是否可用

    判断当此的request请求的返回值，若为None，不可用；若为Response对象，则可用，若存在其他可用情况，返回True

    Args:
        url

    Returns:
        可用：
            返回request请求的返回值
        可用其他情况：
            返回True
        不可用：
            None

    '''
    headers = gen_fake_header()
    s = requests.session()
    s.keep_alive = False
    a = s.get(url=url, timeout=30, headers=headers)
    try:
        s = requests.session()
        s.keep_alive = False
        return s.get(url=url, timeout=30, headers=headers)
    except TooManyRedirects:
        return True
    except requests.exceptions.SSLError:
        try:
            return s.get(url=url, timeout=30, verify=False, headers=headers)
        except Exception as e:
            logger.log('ALERT', f'url访问失败,原因{e}')
            return
    except Exception as e:
        logger.log('ALERT', f'url访问失败,原因{e}')
        return


def gen_fake_header():
    """
    生成伪造请求头
    """
    ua = random.choice(UrlConfig.user_agents)
    #ip = gen_random_ip()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://www.google.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua,
        # 'X-Forwarded-For': ip,
        # 'X-Real-IP': ip
    }
    return headers


def check_domain(domain):
    '''验证域名是否合法
    '''
    return is_tld(domain.split('.')[-1])


def strtodict(stod) -> dict:
    '''
        将从数据库获得的字符串进行处理，得到字典
        Args:
            stod:str  待处理的字符串
        Return:
            new_dict:dict 处理完毕的字典

    '''
    new_dict = json.loads(stod)
    # headers = ast.literal_eval(task.headers)
    # 由于和apifuzz数据结构一样数据需要处理
    new_headers = {}
    for key, value in new_dict.items():
        new_headers[key] = value[1]
    return new_headers


def get_host_ip(target: str) -> tuple:
    """
    获取目标机器的主机ip,port
    :param target: 主机ip或者域名
    :return: 返回ip和端口
    """

    try:
        host = urlparse(target).netloc.split(":")
        host_ip = socket.getaddrinfo(host[0], None)[0][4][0]
        if host:
            port = int(host[1])
    except IndexError as e:
        scheme = urlparse(target).scheme
        port = 80 if scheme == "http" else 443
    except Exception as e:
        logger.log("ALERT", f"ip地址解析失败，错误原因：{e}")
        host_ip, port = None, None

    return host_ip, port


def get_host(url: str) -> str:
    '''
        获取请求头中Host的地址
        Args:
            url:str 待解析的url
        Return:
            hostname:str 返回的Host值
    '''
    result = urlparse(url)
    return result.netloc


def send_request(api_info: dict, buffer=None) -> any:
    '''
    发送请求
    Args:
        api_info:dict api信息  {"api":str,"headers":{},"method":get,"body":xxx,"params":xxx,"role":[1,2,3]}
        buffer:bytes 如果是multipart/form-data则有该值
    Return:
        Response:如果content-type为multipart/form-data时返回原始的请求和响应(bytes)
                 其他类型时返回Response对象
                 
    '''
    url = api_info["url"]
    headers = api_info["headers"]
    headers["User-Agent"] = random.choice(UrlConfig.user_agents)
    content_type = get_content_type(api_info["headers"])
    body = body_conversion(content_type, api_info["data"])

    if buffer:
        host, port = get_host_ip(url)
        if url.startswith("https"):
            connection_choose = CONNECTION["https"]
            connection = connection_choose(
                host, port, server_hostname=get_host(url))
        elif url.startswith("http"):
            connection_choose = CONNECTION["http"]
            connection = connection_choose(host, port)
        else:
            connection_choose = CONNECTION["other"]
            connection = connection_choose(host, port)
            logger.log("ALERT", "其他协议，请检查")

        connection.open()
        connection.send(buffer)
        data, tmp = b'', b''
        while True:
            tmp = connection.recv(1024*1024)
            data += tmp
            if not tmp:
                break
        
        connection.close()
        return buffer,data

    else:
        try:
            response = REQ_DICT[api_info["method"]](
                url=url, headers=api_info["headers"], data=body, timeout=ScanConfig.TIMEOUT, allow_redirects=ScanConfig.REDIRECT, verify=False)
            return response
        except requests.exceptions.ConnectionError as e:
            logger.log(
                "ALERT", f'目标无法连接{e},{api_info["method"]},{url},{api_info["headers"]},{body}')
            return None
        except Exception as e:
            logger.log("ERROR", f'错误原因{e}')
            return None


def get_content_type(headers: dict) -> str:
    '''
        从body中获取Content-Type
        Args:
            headers:dict 请求头
        Return:
            :str Content-Type
    '''
    return headers["Content-Type"] if headers.get("Content-Type") else None

def update_authinfo(url_list, newer_cookie) -> list:
    """
        更新身份信息
        Args:
            url_list:list 接口信息列表
                    ex:[{'url': 'http://192.168.50.88:8080/ssrf/urlConnection/vuln?url=http://1.1.1.1', 
                    'method': 'GET', 'headers': {'Cookie': 'JSESSIONID=1307C4BDF5300B4497756AD9E336708B; 
                    XSRF-TOKEN=86a1b4a7-dd10-4645-87e4-c52dc6e0fbea; remember-me=YWRtaW46MTY2MDY0MDUzMzQ3ODpiYjc1ZTc1ZGI1ODU4MTcxMjM5YWJiYmI1YmFlNzBlZA'}, 
                    'data': '', 'source': 'Target'}]
            newer_cookie: 最新的cookie

        Return:
            url_list:list 
    """

    for url in url_list:
        url["headers"].update(newer_cookie)
    return url_list

if __name__ == '__main__':
    res = check_api_status('http://192.168.50.104:5001/index', 'get')
    print(res)
