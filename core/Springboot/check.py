def Springboot(target):
    try:
        url = target + config.Springbootvuln
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "/info" in vuln.text and "/health" in vuln.text:
            print("[!] SpringbootActuator Unauthorized", url)
    except Exception:
        pass
