import time

from lib.config import portdict,checkfunc
from lib.data import KB
from auxiliary.logs import logger
from threading import Thread


def task_distribute_controller(args) -> None:
    """
    ip:str,port:int
    """

    for key,value in portdict.items():
        if int(args[1]) in value:
            KB["service_task"].put((args[0],int(args[1]),key))
            KB["remain_task"] += 1

    

def task_start_controller() -> None:
    """
    """
    try:
        while KB["is_all_task_end"]:
            break
        while not KB["service_task"].empty():
            task = KB["service_task"].get(timeout=1)
            if task:
                Thread(target = checkfunc[task[2]](task[0],task[1]))
        
            
    except Exception as e:
        logger.log("ERROR",f"检测状态错误{e}")


def task_monitor_controller():
    while True:
        remain_task = KB["remain_task"]
        time.sleep(1)
        if remain_task == 0:
            logger.log("INFOR","所有任务结束")
            KB["is_all_task_end"] = True
            break
        logger.log("INFOR",f"剩余任务{remain_task}")


            

    
