#!/usr/bin/env python3
import sys
from zipfile import ZipFile
from . import breakzip

def main():
    try:
        file_name = sys.argv[1]
        file_ext = sys.argv[2]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <zip_filename> <file_ext>")

    enc_zip = breakzip.ZipFile(file_name)
    file_sig = breakzip.FileSignature().get_file_sig(file_ext)
    if not file_sig: 
        print(f"Unknown file extension/type: {file_ext} ")
        sys.exit(1)

    info = enc_zip.get_info(file_ext)
    if not info:
        print(f"Couldn't find requested file type in archive")
        sys.exit(1)

    password = breakzip.find_password(enc_zip, file_sig, info)
    if password:
        print(f"Found it! -> {password}")
    else:
        print("Password not found")

if __name__ == '__main__':
    main()
