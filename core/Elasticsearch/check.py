def Elasticsearch(target):
    url = target + config.ElasticsearchVuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "/_cat/master" in vuln.text:
            print("[!] Elasticsearch Unauthorized", url)
    except Exception:
        pass


    