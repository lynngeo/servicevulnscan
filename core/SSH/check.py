import paramiko

from auxiliary.logs import logger

from lib.plugin import Plugin
from lib.data import KB
from config import ScanConfig


def SShVuln(ip,port):
    try:
        userdir = ["/servicevulnscan/weakpassdict/username","/root/sniffer/servicevulnscan/weakpassdict/username"]
        passdir = ["/servicevulnscan/weakpassdict/passh","/root/sniffer/servicevulnscan/weakpassdict/passh"]
        for dir in passdir:
            try:
                f = open(dir)
            except Exception as e:
                continue

        pwd = f.readline()

        for dir in userdir:
            try:
                f = open(dir)
            except Exception as e:
                continue

        user = f.readline()

        for username in user:
            for password in pwd:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    sshresult = ssh.connect(ip,port,username,password,timeout=5)
                    logger.log("INFOR", f'[+] SSH weak password: {user},{pwd}')
                    orig_req = ""
                    orig_res = f"SSH weak password: {user},{pwd}"
                    _scan_write(plugin=Plugin.MongodbUnauthorized, url=f"{ip}:{str(port)}", payload=orig_req, raw=[
                                orig_req, orig_res])
                    ssh.close()
                except:
                    logger.log("INFOR", f'[-] checking for {user},{pwd} fail')
                
                    
                    
    except Exception as e:
        logger.log("INFOR",f"{e}")
    finally:
        logger.log("INFOR","剩余任务减1")
        KB["remain_task"] -= 1