def Zookeeper(target):
    url = target.replace("http://", "")
    if "https://" in target:
        url = target.replace("https://", "")
    ip = socket.gethostbyname(url)
    try:
        socket.setdefaulttimeout(10)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, config.Zookeepervuln))
        s.send(bytes("envi\r\n", 'UTF-8'))
        result = s.recv(1024).decode()
        if "Environment" in result:
            print("[!] Zookeeper Unauthorized", ip)
        s.close()
    except Exception:
        pass
