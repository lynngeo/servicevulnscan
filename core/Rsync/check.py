def Rsync(target):
    url = target.replace("http://", "")
    if "https://" in target:
        url = target.replace("https://", "")
    if "Linux" in platform.platform():
        rsynctext = "rsync  " + "rsync://" + url + config.Rsyncvuln
        result = os.popen(rsynctext)
        bool = False
        for line in result:
            if "Password:" in line:
                bool = True
                return
        if bool:
            print("[!] Rsync Unauthorized", url)
    else:
        print("[*] Windows does not support Rsync unauthorized scanning")