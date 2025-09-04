	def oracle(self, ip):
		for i in range(1, len(oracle_user)):
			try:
				user = oracle_user[i]
				pwd  = oracle_pass_default[i]
				conn = cx_Oracle.connect(user, pwd, ip+':1521/orcl')
				print u'{}[+] {}:1521  Oracle存在弱口令: {} {}{}'.format(G, ip, user, pwd, W)
				conn.close()
			except Exception as e:
				pass
		for pwd in passwd:
			try:
				pwd = pwd.replace('{user}', 'sys')
				conn = cx_Oracle.connect('sys', pwd, ip+':1521/orcl')
				print u'{}[+] {}:1521  Oracle存在弱口令: sys {}{}'.format(G, ip, pwd, W)
				conn.close()
				break
			except Exception as e:
				pass