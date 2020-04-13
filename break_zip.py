#!/usr/bin/env python3
from zipfile import ZipFile
import sys

alias_keys = {
        'pkzip': 1, 
        'winzip': 1, 
        'zip': 1,
        'asf': 2,
        'wmv': 2,
        'wma': 2
}

file_types = { 1: b'PK\x03\x04', 2 : b'\x30\x26\xb2' }

class EncryptedZipFile(ZipFile):
    def __init__(self, zip_name):
        ZipFile.__init__(self, zip_name)
        self.debug = 3
    def get_info(self):
        if len(self.infolist()) >= 1:
            return self.infolist()[len(self.infolist())-1]

if __name__ == '__main__':
    enc_zip = EncryptedZipFile(sys.argv[1])
    file_type = file_types.get(alias_keys[sys.argv[2]], None)
    if not file_type: 
        print("Unknown file type")
        sys.exit(1)

    found_it = False
    for line in sys.stdin:
        pwd = line.strip('\n')
        try:
            with enc_zip.open(enc_zip.get_info(), 'r', pwd=pwd.strip().encode('utf-8', 'ignore')) as myzip:
                try:
                    head = myzip.__next__()
                    #print("Trying: ", pwd)
                    if (file_type in head):
                        found_it = True
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

    if found_it:
        print(f"Found it! -> {pwd}")
    else:
        print("Password not found")
