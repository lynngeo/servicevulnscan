def ldap_anonymous(target):
    url = target.replace("http://", "")
    if "https://" in target:
        url = target.replace("https://", "")
    try:
        server = Server(url, get_info=ALL, connect_timeout=1)
        conn = Connection(server, auto_bind=True)
        print("[+] ldap login for anonymous")
        conn.closed()
    except Exception:
        pass