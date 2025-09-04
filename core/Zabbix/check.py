def Zabbix(target):
    url = target + config.Zabbixvuln
    try:
        vuln = requests.get(url, headers=RabbitMQheaders, verify=False)
        if vuln.status_code == 200 and "Latest data" in vuln.text:
            print("[!] RabbitMQ Unauthorized", url)
    except Exception:
        pass
