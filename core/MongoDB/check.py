import pymongo

from auxiliary.logs import logger

from lib.plugin import Plugin
from lib.data import KB
from config import ScanConfig


def MongoDBUnauthorized(ip,port):
    try:
        conn = pymongo.MongoClient(ip, port, socketTimeoutMS=ScanConfig.TIMEOUT, serverSelectionTimeoutMS=ScanConfig.TIMEOUT)
        dbname = conn.database_names()
        server_version = conn.server_info()["version"]
        if dbname:
            logger.log("INFOR","[!] MongoDB Unauthorized")
            
    except Exception as e:
        logger.log("ALERT",f"MongoDB check error{e}")
    finally:
        logger.log("INFOR","剩余任务减1")
        KB["remain_task"] -= 1