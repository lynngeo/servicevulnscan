import threading
import sys
import time
import json
from multiprocessing.dummy import Pool as ThreadPool


from lib.data import KB
from lib.config import portdict
from auxiliary.logs import logger

from controller.controller import task_distribute_controller, task_monitor_controller, task_start_controller



def main():
    '''
    vulscan入口
    '''
    try:
       

      
        strategy_name = str(sys.argv[1])  #具体漏扫的策略  None:未指定策略
        ip = str(sys.argv[2])  #具体扫描的ip  None:未指定ip  []:扫描所有ip
        ports = str(sys.argv[3])  #具体扫描的端口 None:未指定端口 []
        if not isinstance(ports,list):
            ports = [80]
        KB['LOCK'] = threading.Lock()
        

        # querylist = [(query.ip,query.port) for query in ports_task_config_query ]
        querylist = []
        for port in ports:
            querylist.append((ip,port))

        # 如果指定了策略只扫描指定的策略
        if strategy_name != 'ALL':
            for checkservice, checkports in portdict.items():
                if checkservice == strategy_name:
                    checkports.extend(ports)
                elif checkservice != strategy_name:
                    portdict[checkservice] = []
        else:
            for checkservice, checkports in portdict.items():
                checkports.extend(ports)
                    
    except Exception as e:
        logger.log("INFOR",f'输入参数不合法{e},示例: python run.py ALL 192.168.1.1 [80, 443]')
        return



    time1 = time.time()
    # 将获取到的ip， port 发送至任务指派控制
  
    
    pool = ThreadPool()

    pool.map(task_distribute_controller,querylist)
    
    if KB["remain_task"] == 0:
        logger.log("INFOR","无相关检测插件，退出")
    else:
        task = threading.Thread(target=task_start_controller) 
        task_monitor = threading.Thread(target=task_monitor_controller)
        task.start()
        task_monitor.start()
        
        task.join()
        task_monitor.join()

   
    time2 = time.time()
    print("执行时间",time2-time1)


if __name__ == '__main__':
    main()
