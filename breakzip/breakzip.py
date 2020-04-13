#!/usr/bin/env python3
from zipfile import ZipFile
import sys

alias_keys = {
        'pkzip': 1, 
        'zip': 1,
        'asf': 2,
        'wmv': 2,
        'wma': 2,
        'jpg': 3,
        'jpeg': 3,
        'png': 4,
        'xml': 5,
}

file_types = { 
        1: b'PK\x03\x04', 
        2: b'\x30\x26\xb2',
        3: b'\xff\xd8',
        4: b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a',
        5: b'\x3c\x3f\x78\x6d\x6c\x20',
}

class EncryptedZipFile(ZipFile):
    def __init__(self, zip_name):
        ZipFile.__init__(self, zip_name)
        self.debug = 3
    def get_info(self, file_ext):
        for info in self.infolist():
            if file_ext in info.filename:
                return info
        return None

def find_password(enc_zip, file_type, info, pw_source=sys.stdin):
    found_it = False
    for line in pw_source:
        guess_pwd = line.strip().rstrip().encode('utf-8', 'ignore')
        try:
            with enc_zip.open(info, 'r', pwd=guess_pwd) as myzip:
                try:
                    head = myzip.__next__()
                    if (file_type in head):
                        found_it = True
                        guess_pwd = str(guess_pwd, 'utf-8')
                        break
                except:
                    pass
        except UnicodeDecodeError:
            pass
        except RuntimeError:
            pass
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    if found_it:
        return guess_pwd
    return None
