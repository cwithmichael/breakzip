#!/usr/bin/env python3
import sys
from zipfile import ZipFile
from . import breakzip, db


def main():
    try:
        file_name = sys.argv[1]
        file_ext = sys.argv[2]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <zip_filename> <file_ext>")

    enc_zip = ZipFile(file_name)

    info = breakzip.get_info(enc_zip, file_ext)
    if not info:
        print(f"Couldn't find requested file type in archive")
        sys.exit(1)

    # Create DB
    try:
        conn = db.create_connection()
    except:
        print("Something went wrong creating the database. The script cannot continue.")
        sys.exit(1)
    # Initialize DB
    try:
        db.init_db(conn)
    except:
        print("Something went wrong initializing the database. Check the logs for more info.")
        sys.exit(1)
    finally:
        conn.close()
 
    # Fetch file signature
    try:
        file_sig = db.find_signature(conn, file_ext)
        if not file_sig:
            print(f"Unknown file extension/type: {file_ext} ")
            sys.exit(1)
    except:
        print("Something went wrong querying the database. Check the logs for more info.")
        sys.exit(1)
    finally:
        conn.close()

    password = breakzip.find_password(enc_zip, file_sig, info)
    if password:
        print(f"Found it! -> {password}")
    else:
        print("Password not found")


if __name__ == "__main__":
    main()
