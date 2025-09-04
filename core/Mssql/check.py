def mssql(self, ip):
    for pwd in passwd:
        try:
            pwd = pwd.replace('{user}', 'sa')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, 1433))
            husername = binascii.b2a_hex('sa')
            lusername = len('sa')
            lpassword = len(pwd)
            hpwd = binascii.b2a_hex(pwd)
            address = binascii.b2a_hex(ip) +'3a'+ binascii.b2a_hex(str(1433))
            data1 = data.replace(data[16:16+len(address)], address)
            data2 = data1.replace(data1[78:78+len(husername)], husername)
            data3 = data2.replace(data2[140:140+len(hpwd)], hpwd)
            if lusername >= 16:
                data4 = data3.replace('0X', str(hex(lusername)).replace('0x', ''))
            else:
                data4 = data3.replace('X', str(hex(lusername)).replace('0x', ''))
            if lpassword >= 16:
                data5 = data4.replace('0Y', str(hex(lpassword)).replace('0x', ''))
            else:
                data5 = data4.replace('Y', str(hex(lpassword)).replace('0x', ''))
            hladd = hex(len(ip) + len(str(1433))+1).replace('0x', '')
            data6 = data5.replace('ZZ', str(hladd))
            data7 = binascii.a2b_hex(data6)
            s.send(data7)
            if 'master' in s.recv(1024):
                print u'{}[+] {}:1433  SQLserver存在弱口令: sa  {}{}'.format(G, ip, pwd, W)
                break
        except Exception as e:
            pass
        finally:
            s.close()