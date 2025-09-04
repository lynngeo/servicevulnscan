# import sys,os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from urllib.parse import urlparse

from lib.data import KB
from auxiliary.auxiliary import toolthread_decorator
from .jsonp import JsonpScanner

@toolthread_decorator
def jsonp_run():
    jsonp = JsonpScanner()
    has_jsonp = False
    for crawl_result in KB["crawl_result"]:
        for filter in jsonp.FILTER_WORD:
            if filter in urlparse(crawl_result["url"]).query:
                has_jsonp = jsonp.scan(crawl_result,filter)
                if has_jsonp:
                    break

    #{'url': 'http://192.168.50.88:9080/crlf/', 
    # 'method': 'GET', 'headers': {'Spider-Name': 
    # 'sniffer-Anban-Tech'}, 'data': '', 'source': 'Target'}
        

if __name__ == '__main__':
    jsonp_run()
