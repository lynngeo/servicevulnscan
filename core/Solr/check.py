def Solr(target):
    url = target + config.Solrvuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "Collections" in vuln.text and "Cloud" in vuln.text:
            print("[!] Solr Unauthorized", url)
    except Exception:
        pass