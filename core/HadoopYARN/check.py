def HadoopYARN(target):
    url = target + config.HadoopYARNVuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "All Applications" in vuln.text:
            print("[!] HadoopYARN Unauthorized", url)
    except Exception:
        pass