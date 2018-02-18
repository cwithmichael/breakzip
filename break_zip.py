from zipfile import ZipFile
import sys

love = ZipFile(sys.argv[1])
love.debug = 3
info = love.infolist()[len(love.infolist())-1]
dictionary = sys.argv[2]
password = ''
test = b'lol'
zippity = b'PK\x03\x04'
with open(dictionary, 'r') as dic:
	for line in dic.readlines():
		pwd = line.strip('\n')
		print("Trying: ", pwd)
		try:
			with love.open(info, 'r', pwd=pwd.encode()) as myzip:
				try:
					head = myzip.__next__()
					print(head)
					if (zippity in head):
						password = 'Found it!: %s' % pwd
						break
				except:
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
