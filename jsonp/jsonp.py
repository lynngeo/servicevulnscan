import copy
import js2py
import re
from urllib.parse import urlparse

from auxiliary.auxiliary import orig_reqhandle, orig_reshandle, send_request
from auxiliary.logs import logger

from lib.plugin import Plugin


class JsonpScanner():
    """ Scans URLs for CRLF injection.
    """

    FILTER_WORD = ["jcb", "jsonp", "jsoncb", "jsonpcb", "jsonp_cb" "cb", "json",
                   "jsonpcall", "jsoncall", "jQuery", "callback", "call", "ca"
                   "back", "jsoncallback", "jsonpcallback"]

    JAVASCRIPT_TYPE = ["application/ecmascript",
                       "application/javascript",
                       "application/x-ecmascript",
                       "application/x-javascript",
                       "text/ecmascript",
                       "text/javascript",
                       "text/javascript1.0",
                       "text/javascript1.1",
                       "text/javascript1.2",
                       "text/javascript1.3",
                       "text/javascript1.4",
                       "text/javascript1.5",
                       "text/jscript",
                       "text/livescript",
                       "text/x-ecmascript",
                       "text/x-javascript"]

    def __init__(self):
        pass

    def scan(self, api_info: dict, filter: str) -> bool:
        """ 
            Scan target URL for JSONP vuln
            Args:
                api_info: dict 原始api信息
                filter: str 回调关键字
            Return:
                :bool 如果存在jsonp，返回True
        """
        result = False
        try:
            response = send_request(api_info)
            new_api_info = copy.deepcopy(api_info)
            new_api_info["headers"]["Referer"] = "http://test.com"
            response_ref = send_request(new_api_info)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.log("ERROR", f'错误原因{e}')
            return False

        if response.status_code == 200 and response_ref.status_code == 200 and response.text == response_ref.text:
            for jstype in self.JAVASCRIPT_TYPE:
                if jstype in response.headers.get("Content-type"):
                    callbackparse = urlparse(new_api_info["url"]).query
                    if not callbackparse:
                        return False
                    callbackname = ""
                    for param in callbackparse.split("&"):
                        data = param.split("=")
                        if re.search(filter, data[0]):
                            callbackname = data[1]
                            break

            esprima = js2py.require('esprima')
            tree = esprima.parse(response_ref.text).to_dict()
            try:
                for body in tree.get("body"):
                    tmp = body.get("expression").get("callee").get("name")
                    if tmp:
                        callee = tmp
                    else:
                        callee = None
            except TypeError:
                callee = None

            if callee == callbackname:
                try:
                    for body in tree.get("body"):
                        for argument in body.get("expression").get("arguments"):
                            for properties in argument.get("properties"):
                                key = properties.get("key").get("value")
                                if key and re.search("(?m)(?i)(id)|(userid)|(user_id)|(nin)|(name)|(username)|(nick)|(email)|(phone)", key):
                                    result = True
                except Exception as e:
                    logger.log("ERROR", f'错误信息{e}')

                if result:
                    payload = ""
                    orig_req = orig_reqhandle(
                        new_api_info["method"], new_api_info["url"], new_api_info["headers"], new_api_info["data"])
                    orig_res = orig_reshandle(response)
                    _scan_write(plugin=Plugin.jsonp, url=api_info["url"], payload=payload, raw=[
                                orig_req, orig_res])

        return result
