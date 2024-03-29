#!/usr/bin/env python3
import sys
import argparse
from zipfile import ZipFile
from . import breakzip


def main():
    parser = argparse.ArgumentParser(description="""Smarter PKZIP Brute-Forcing""")
    parser.add_argument(
        "file_name", help="The name of the zip file. i.e. encrypted.zip"
    )
    parser.add_argument(
        "file_ext", help="Known file extension in the zip file. i.e. jpg"
    )
    parser.add_argument(
        "-i",
        "--interactive_mode",
        action="store_true",
        help="Manually type passwords on the command line",
    )
    args = parser.parse_args()

    file_name = args.file_name
    try:
        open(file_name, mode="r")
    except:
        print(f"Unable to open zip file: {file_name}")
        sys.exit(1)

    file_ext = args.file_ext
    file_sig = breakzip.get_file_sig(file_ext)
    if not file_sig:
        print(f"Unknown file extension/type: {file_ext} ")
        sys.exit(1)

    enc_zip = ZipFile(file_name)
    info = breakzip.get_info(enc_zip, file_ext)
    if not info:
        print(f"Couldn't find requested file type in archive")
        sys.exit(1)

    # Start a manual session if interactive_mode is set
    if args.interactive_mode:
        while True:
            guess = input("Enter password: ")
            password = breakzip.find_password(
                enc_zip, file_sig, info, pw_source=[guess]
            )
            if password:
                print(f"Found it! -> {password}")
                sys.exit(0)
            else:
                print("Incorrect Password. Try again.")
    # Otherwise expect the passwords to be piped in
    else:
        password = breakzip.find_password(enc_zip, file_sig, info)
        if password:
            print(f"Found it! -> {password}")
        else:
            print("Password not found")


if __name__ == "__main__":
    main()
