def Ftp(target):
    url = target.replace("http://", "")
    if "https://" in target:
        url = target.replace("https://", "")
    ip = socket.gethostbyname(url)
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, config.FtpVuln)
        ftp.login("anonymous", "anonymous")
        print("[!] FTP Unauthorized", ip)
    except Exception:
        pass
