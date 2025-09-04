import requests
from .connctions import *

requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
# 设置连接活跃状态为False
s.keep_alive = False
   
REQ_DICT = {
    "GET": s.get,
    "POST": s.post,
    "DELETE": s.delete,
    "PUT": s.put,
    "PATCH": s.patch,
    "HEAD": s.head
}


CONNECTION = {
    "http": TCPSocketConnection,
    "https": SSLSocketConnection,
    "other": TCPSocketConnection
}