import socket
from auxiliary.logs import logger

from lib.plugin import Plugin
from lib.data import KB
from config import ScanConfig

def MemcachedUnauthorized(ip, port):
    try:
        socket.setdefaulttimeout(ScanConfig.TIMEOUT)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send(bytes("stats\r\n", 'UTF-8'))
        result = s.recv(1024).decode()
        if "STAT version" in result:
            logger.log("INFOR",f"{ip}:{port}存在memcached未授权漏洞")
            orig_req = "stats\r\n"
            orig_res = result
            _scan_write(plugin=Plugin.MemcachedUnauthorized, url=f"{ip}:{port}", payload="stats\r\n", raw=[
                        orig_req, orig_res])
        s.close()
    except Exception:
        pass
    finally:
        logger.log("INFOR","剩余任务减1")
        KB["remain_task"] -= 1

