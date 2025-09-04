import socket

from auxiliary.logs import logger

from lib.plugin import Plugin
from lib.config import DubboVulnUnauthorizedConfig


def DubboUnauthorized(target):
    try:
        payload = DubboVulnUnauthorizedConfig.payload
        socket.setdefaulttimeout(5)

        for port in DubboVulnUnauthorizedConfig.port:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.send(payload)
            result = s.recv(1024).decode()
            if "server" in result:
                logger.log("INFOR", f"[!] Dubbo Unauthorized {target}:{port}")
                break
            s.close()

    except Exception as e:
        logger.log("ALERT",f"提示信息:{e}")

    finally:
        s.close()
