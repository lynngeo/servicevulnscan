import requests

def DockerAPI(target):
    url = target + config.DockerAPIVuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "Version" in vuln.text:
            print("[!] DockerAPI Unauthorized", url)
    except Exception:
        pass