
portdict = {
    #"ActiveMQVuln":[8161],
    #"DubboVulnUnauthorized":[20880],
    # "SShVuln":[22],
    "PostgresVuln":[5432,15432,25432,35432],
    #"RabbitMQUnauthorized":[5672,15672,25672,15692],
    "RedisUnsafeAuth":[6379],
    "OpensslHeartbleed":[443],
    "MemcachedUnauthorized":[11211],
    "MongodbUnauthorized":[27017],
   
}

class ActiveMQVulnConfig:
    payload = "/admin"    
    port = [8161]

class PostgresVulnConfig:
    port = [5432,15432,25432,35432]

class DubboVulnUnauthorizedConfig:
    payload = bytes("status -l\r\n", 'UTF-8')
    port = [20880]

class RabbitMQUnauthorizedConfig:
    payload = "/api/whoami"
    port = [5672,15672,25672,15692]

class RedisUnauthorizedConfig:
    port = [6379]


from core.Postgres.check import PostgresAuth
from core.RabbitMQ.check import RabbitMQUnauthorized
from core.Redis.check import RedisUnsafeAuth
from core.Openssl.check import OpensslHeartbleed
from core.MongoDB.check import MongoDBUnauthorized
from core.SSH.check import SShVuln
from core.Memcache.check import MemcachedUnauthorized

# 目前可检测的所有组件/中间件/服务漏洞
checkfunc = {
    "PostgresVuln":PostgresAuth,
    #"RabbitMQUnauthorized":RabbitMQUnauthorized,
    "RedisUnsafeAuth":RedisUnsafeAuth,
    "OpensslHeartbleed":OpensslHeartbleed,
    "MongodbUnauthorized":MongoDBUnauthorized,
    "MemcachedUnauthorized":MemcachedUnauthorized,
    "SShVuln":SShVuln
}


Redisvuln = 6379

AtlassianCrowdVuln = "/crowd/admin/uploadplugin.action"
CouchDBVuln = ":5984"
DockerAPIVuln = ":2375/version"

DruidVuln = "/druid/index.html"
ElasticsearchVuln = ":9200/_cat"
FtpVuln = 21
HadoopYARNVuln = ":8088/cluster"
JBossVuln = ":8080/jmx-console/"
JenkinsVuln = ":8080/script"
JupyterNotebookVuln = ":8889/tree"
Kibanavuln = ":5601/app/kibana#"
KubernetesApiServervuln = ":6443"
Weblogicvuln = ":7001/console/css/%252e%252e%252fconsole.portal"
Solrvuln = ":8983/solr/#/"
Springbootvuln = "/actuator/"


Zabbixvuln = "/latest.php?ddreset=1"

Rsyncvuln = ":873/"
Memcachevuln = 11211
MongoDBvuln = 27017
Zookeepervuln = 2181


#coding:utf-8

#扫描的服务类型及默认对口
service = {'mssql':'1433',
		   'oracle':'1521',
		   'mysql':'3306',
		   'postgresql':'5432',
           'redis':'6379',
           'elasticsearch':'9200',
           'memcached':'11211',
           'mongodb':'27017'}

passwd = ['123456','admin','root','password','123123','123','1','','{user}',
		  '{user}{user}','{user}1','{user}123','{user}2016','{user}2015',
		  '{user}!','P@ssw0rd!!','qwa123','12345678','test','123qwe!@#',
		  '123456789','123321','1314520','666666','woaini','fuckyou','000000',
		  '1234567890','8888888','qwerty','1qaz2wsx','abc123','abc123456',
		  '1q2w3e4r','123qwe','159357','p@ssw0rd','p@55w0rd','password!',
		  'p@ssw0rd!','password1','r00t','system','111111','admin']

#colour
W = '\033[0m'
G = '\033[1;32m'
O = '\033[1;33m'
R = '\033[1;31m'
B = '\033[1;34m'

#oracle默认用户及密码
oracle_user = ['sys','system','sysman','scott','aqadm','Dbsnmp']
oracle_pass_default = ['','manager','oem_temp','tiger','aqadm','dbsnmp']

#mssql登陆请求数据流
data = '0200020000000000123456789000000000000000000000000000000000000000000000000000ZZ5440000000000000000000000000000000000000000000000000000000000X3360000000000000000000000000000000000000000000000000000000000Y373933340000000000000000000000000000000000000000000000000000040301060a09010000000002000000000070796d7373716c000000000000000000000000000000000000000000000007123456789000000000000000000000000000000000000000000000000000ZZ3360000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000Y0402000044422d4c6962726172790a00000000000d1175735f656e676c69736800000000000000000000000000000201004c000000000000000000000a000000000000000000000000000069736f5f31000000000000000000000000000000000000000000000000000501353132000000030000000000000000'

# [ActiveMQ, AtlassianCrowd, CouchDB, DockerAPI, Dubbo, Druid,
#                     Elasticsearch, Ftp, HadoopYARN, JBoss, Jenkins, JupyterNotebook,
#                     Kibana, KubernetesApiServer, ldap_anonymous, Weblogic, Solr, Springboot,
#                     RabbitMQ, Zabbix, Redis, Rsync, NFS, Memcache, MongoDB, Zookeeper
#                     ]