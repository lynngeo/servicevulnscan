def NFS(target):
    url = target.replace("http://", "")
    if "https://" in target:
        url = target.replace("https://", "")
    if "Linux" in platform.platform():
        rsynctext = "showmount  -e  " + url
        result = os.popen(rsynctext)
        for line in result:
            if "Export list" in line:
                print("[!] NFS Unauthorized", url)
                return
    else:
        print("[*] Windows does not support NFS unauthorized scanning")