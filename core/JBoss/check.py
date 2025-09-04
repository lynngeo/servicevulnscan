def JBoss(target):
    url = target + config.JBossVuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "JBoss JMX Management Console" in vuln.text:
            print("[!] JBoss Unauthorized", url)
    except Exception:
        pass
