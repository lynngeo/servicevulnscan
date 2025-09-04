import socket

from auxiliary.logs import logger

from lib.plugin import Plugin
from lib.data import KB


def RedisUnsafeAuth(ip,port):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.connect((ip, port))
        s.send(bytes("INFO\r\n", 'UTF-8'))
        result = s.recv(1024).decode()
        if 'redis_version' in result:
            logger.log("INFOR",f'{ip}:{port} Redis存在未授权访问')
            _scan_write(plugin=Plugin.RedisUnauthorized, url=f"{ip}:{port}", payload=f"INFO\r\n", raw=[
                            "INFO\r\n", result])
            s.close()
        else:
            if 'NOAUTH Authentication required' in result:
                files = ["/servicevulnscan/weakpassdict/passusual","/root/sniffer/servicevulnscan/weakpassdict/passusual"]
                filename = ""
                for file in files:
                    try:
                        f = open(file)
                        filename = file
                    except Exception as e:
                        continue

                with open(filename) as f:
                    for pwd in f.readlines():
                        pwd = pwd.strip().strip("\n")
                        try:
                            pwd = pwd.replace('{user}', 'admin')
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.connect((ip, port))
                            message = 'AUTH {}\r\n'.format(pwd)
                            s.send(message.encode())
                            if b'+OK' in s.recv(1024):
                                logger.log("INFOR",f'{ip}:{port} Redis存在弱口令: {pwd}')
                                _scan_write(plugin=Plugin.RedisWeakauth, url=f"{ip}:{port}", payload=message, raw=[
                                    message, '+OK'])
                                break
                                
                        except Exception as e:
                            logger.log("INFOR",e)
                        finally:
                            s.close()
    except Exception as e:
        logger.log("INFOR",f"错误原因:{e}")

    finally:
        logger.log("INFOR","剩余任务减1")
        KB["remain_task"] -= 1
        s.close()


    