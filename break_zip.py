from zipfile import ZipFile
import sys

love = ZipFile(sys.argv[1])
dictionary = 'dict.txt'
password = ''
with open(dictionary, 'r') as dic:
	for line in dic.readlines():
		pwd = line.strip('\n')
		try:
			love.open(name='Archive.zip',mode='rw', pwd=bytes(pwd, 'utf-8'))
			love.printdir()
			#love.read(name='Archive.zip', pwd=pwd)
			#love.testzip()
			password = 'Found it!: %s' % pwd
			break
		except:
			pass	
if password:
	print(password)
else:
	print("Password not found")
