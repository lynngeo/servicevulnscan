from queue import Queue


# 全局变量
KB = dict()
KB["service_task"] = Queue()   # 任务队列
KB["remain_task"] = 0 # 剩余任务数
KB["is_all_task_end"] = False