from zipfile import ZipFile
import sys

love = ZipFile(sys.argv[1])
love.debug = 3
info = love.infolist()[len(love.infolist())-1]
password = ''
test = b'lol'
zippity = b'PK\x03\x04'
for line in sys.stdin:
	pwd = line.strip('\n')
	try:
		with love.open(info, 'r', pwd=pwd.strip().encode('utf-8', 'ignore')) as myzip:
			try:
				head = myzip.__next__()
				#print("Trying: ", pwd)
				if (zippity in head):
					password = 'Found it!: %s' % pwd
					break
			except:
				pass
	except UnicodeDecodeError:
		pass
	except RuntimeError:
		pass
	except:
		print(line)
		print("Unexpected error:", sys.exc_info()[0])
		raise

if password:
	print(password)
else:
	print("Password not found")
