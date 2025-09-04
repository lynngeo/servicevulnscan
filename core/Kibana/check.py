def Kibana(target):
    url = target + config.Kibanavuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "Visualize" in vuln.text:
            print("[!] Kibana Unauthorized", url)
    except Exception:
        pass