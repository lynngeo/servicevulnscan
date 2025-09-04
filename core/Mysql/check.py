import pymysql

def MysqlUnauthorized(ip):
    try:
        conn = pymysql.connect(host=ip, user='root', password='', charset='utf8', autocommit=True)
        # print(ip + ":3306 存在mysql空口令漏洞")
        file_write("mysql_Empty_pwd.txt",ip + ":3306 存在mysql空口令漏洞")
    except Exception as e:
        pass
    finally:
        pass
       
def MysqlWeakauth(ip):
    for pwd in passwd:
        try:
            pwd = pwd.replace('{user}', 'root')
            conn = MySQLdb.connect(ip, 'root', pwd, 'mysql')
            print u'{}[+] {}:3306  Mysql存在弱口令: root  {}{}'.format(G, ip, pwd, W)
            conn.close()
            break
        except Exception as e:
            pass
    