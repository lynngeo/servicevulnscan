import requests

def CouchDBUnauthorized(target):
    url = target + config.CouchDBVuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "version" in vuln.text:
            print("[!] CouchDB Unauthorized", url)
    except Exception:
        pass

    