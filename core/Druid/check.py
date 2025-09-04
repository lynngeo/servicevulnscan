def Druid(target):
    url = target + config.DruidVuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "Druid Stat Index" in vuln.text:
            print("[!] Druid Unauthorized", url)
    except Exception:
        pass