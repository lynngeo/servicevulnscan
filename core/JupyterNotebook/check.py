def JupyterNotebook(target):
    url = target + config.JupyterNotebookVuln
    try:
        vuln = requests.get(url, headers, verify=False)
        if vuln.status_code == 200 and "Jupyter Notebook" in vuln.text:
            print("[!] JupyterNotebook Unauthorized", url)
    except Exception:
        pass