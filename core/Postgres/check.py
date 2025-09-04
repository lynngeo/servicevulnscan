import psycopg2

from auxiliary.logs import logger
from lib.plugin import Plugin
from lib.data import KB
from config import ScanConfig


def PostgresAuth(ip,port):
    try:
        conn = psycopg2.connect(user="postgres", password="", host=ip, port=port,connect_timeout=ScanConfig.TIMEOUT)
        logger.log("INFOR",f"{ip}:{port}存在postgres未授权漏洞")

    except Exception as e:
        logger.log("ALERT",f"提示信息:{e}")
        comparestr = e.args[0].strip("\n").strip(' ')
        if comparestr == 'fe_sendauth: no password supplied':
            # 如果空口令不存在，尝试弱口令问题
            dirs = ["/servicevulnscan/weakpassdict/passusual","/root/sniffer/servicevulnscan/weakpassdict/passusual"]
            for dir in dirs:
                try:
                    f = open(dir)
                except Exception as e:
                    continue

            pwd = f.readline()
            while pwd:
                try:
                    pwd = pwd.replace('{user}', 'postgres').strip("").strip("\n")
                    conn = psycopg2.connect(host=ip, port=port, user='postgres', password=pwd, connect_timeout=ScanConfig.TIMEOUT)
                    logger.log("INFOR",f"{ip}:{port}存在postgres弱口令漏洞，postgres,{pwd}")
                    conn.close()
                    break
                except Exception as e:
                    logger.log("INFOR",f"{e}")
                    pwd = f.readline()

    finally:
        logger.log("INFOR","剩余任务减1")
        KB["remain_task"] -= 1

        