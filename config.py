import uuid
import yaml
import os

UTF8 = 'utf-8'
LATIN1 = 'latin1'



class DataConfig:
    filter_data = ["Login","login"]   #设置不进行payload替换的参数
    regex = r'[\S]+=[\S]+[&]{0,1}$'

class ScanConfig:
    TIMEOUT = 5     # 超时设置
    REDIRECT = False  # 是否可以重定向
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
    TEMPLATE_DIR = os.path.join(ROOT_PATH, 'files')


class Pattern:
    DOMAIN_PATTERN = r'(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+'
    IP_PATTERN = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'

class UrlConfig:
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '
    'Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0',
    ]
