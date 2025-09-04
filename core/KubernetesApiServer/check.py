def KubernetesApiServer(target):
    url = target + config.KubernetesApiServervuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "paths" in vuln.text and "/api" in vuln.text:
            print("[!] KubernetesApiServer", url)
    except Exception:
        pass