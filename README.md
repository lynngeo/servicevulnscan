# 解释
主机漏扫，支持下列组件漏扫

ActiveMQ, AtlassianCrowd, CouchDB, DockerAPI, Druid, Dubbo, Elasticsearch, Ftp, HadoopYARN, JBoss, Jenkins, JupyterNotebook, Kibana, KubernetesApiServer, ldap_anonymous, Memcache, MongoDB, Mssql, Mysql, NFS, Openssl, Oracle, Postgres, RabbitMQ, Redis, Rsync, Solr, Springboot, SSH, Weblogic, Zabbix, Zookeeper


- 如果策略位置处填写ALL,会对指定端口进行所有策略的扫描

    python run.py ALL 47.99.167.129 [80,443]

- 如果指定策略和端口，只会取ip，端口就是指定的端口
    python run.py PostgresVuln [8080,8081] 