import requests

def AtlassianCrowdUnauthorized(target):
    url = target + config.AtlassianCrowdVuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 400:
            print("[!]AtlassianCrowd Unauthorized(RCE https://github.com/jas502n/CVE-2019-11580)", url)
    except Exception:
        pass