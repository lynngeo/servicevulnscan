import random
import requests

from config import UrlConfig
from auxiliary.logs import logger
from auxiliary.auxiliary import orig_reqhandle, orig_reshandle, orig_reshandle

from lib.plugin import Plugin

def ActiveMQUnauthorized(target):
    url = target + "/admin"
    try:
        basicAuth = requests.get(url, random.choice(UrlConfig.user_agents), verify=False, auth=('admin', 'admin'))
        if basicAuth.status_code == 200 and "Version" in basicAuth.text:
            print("[!]ActiveMQ Unauthorized", url)
    except Exception:
        pass