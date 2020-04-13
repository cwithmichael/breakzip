#!/usr/bin/env python3
import sys
from . import breakzip

def main():
    try:
        file_name = sys.argv[1]
        file_ext = sys.argv[2]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <zip_filename> <file_ext>")

    enc_zip = breakzip.EncryptedZipFile(file_name)
    file_key = breakzip.alias_keys.get(file_ext, None)
    file_type = breakzip.file_types.get(file_key, None)
    if not file_type: 
        print(f"Unknown file extension/type: {file_ext} ")
        sys.exit(1)

    info = enc_zip.get_info(file_ext)
    if not info:
        print(f"Couldn't find requested file type in archive")
        sys.exit(1)

    password = breakzip.find_password(enc_zip, file_type, info)
    if password:
        print(f"Found it! -> {password}")
    else:
        print("Password not found")

if __name__ == '__main__':
    main()
