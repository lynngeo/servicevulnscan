import requests

from auxiliary.logs import logger
from auxiliary.auxiliary import orig_reqhandle, orig_reshandle, orig_reshandle
from lib.plugin import Plugin
from lib.config import RabbitMQUnauthorizedConfig
from lib.data import KB

RabbitMQheaders = {
    'authorization': 'Basic Z3Vlc3Q6Z3Vlc3Q=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}

RabbitMQDefaultPassword = {
    "guest":"guest"
}

def RabbitMQUnauthorized(ip, port):

    try:
        payload = RabbitMQUnauthorizedConfig.payload
        prefixs = ["http://", "https://"]

        for prefix in prefixs:
            try:
                url = prefix + ip + ":" + str(port)
                fullpath = url + payload
                vuln = requests.get(fullpath, headers=RabbitMQheaders, verify=False, timeout=5)
                if vuln.status_code == 200 and "guest" in vuln.text:

                    logger.log("INFOR", f"[!] RabbitMQ default authorized. {url}")
                    orig_req = orig_reqhandle("GET", fullpath, RabbitMQheaders, "")
                    orig_res = orig_reshandle(vuln)
                    _scan_write(plugin=Plugin.RabbitMQUnauthorized, url=fullpath, payload=payload, raw=[
                                orig_req, orig_res])
                    break

            except Exception as e:
                logger.log("ALERT", f"{url}错误原因:{e}")
    except Exception as e:
            logger.log("ALERT", f"{url}错误原因:{e}")
    finally:
        logger.log("INFOR","剩余任务减1")
        KB["remain_task"] -= 1

