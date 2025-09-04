def Weblogic(target):
    url = target + config.Weblogicvuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "管理控制台主页" in vuln.text and "注销" in vuln.text:
            print("[!] Weblogic Unauthorized", url)
    except Exception:
        pass