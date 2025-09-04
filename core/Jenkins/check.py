def Jenkins(target):
    url = target + config.JenkinsVuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "Jenkins-Crumb" in vuln.text:
            print("[!] Jenkins Unauthorized", url)
    except Exception:
        pass