#!/usr/bin/env python3
"""This module attempts to find lost passwords for Zip 2.0 encrypted zip files.

False positives are minimized by validating the header of the extracted data against a list of known file signatures.
The user provides the file extension/type of a known file in the archive.
"""
import sys

alias_keys = {
    "pkzip": 1,
    "zip": 1,
    "asf": 2,
    "wmv": 2,
    "wma": 2,
    "jpg": 3,
    "jpeg": 3,
    "png": 4,
    "xml": 5,
}

file_sigs = {
    1: bytes([0x50, 0x4B, 0x03, 0x04]),
    2: bytes([0x30, 0x26, 0xB2]),
    3: bytes([0xFF, 0xD8]),
    4: bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]),
    5: bytes([0x3C, 0x3F, 0x78, 0x6D, 0x6C, 0x20]),
}


def get_file_sig(file_ext):
    """Gets the file singature for a given file extension

    Args:
        file_ext: File extension of known file in archive

    Returns:
        The file signature of the given file extension/type
    """
    file_key = alias_keys.get(file_ext, None)
    file_sig = file_sigs.get(file_key, None)
    return file_sig


def get_info(enc_zip, file_ext):
    """Gets the ZipInfo instance of the first file found with the given file extension

    Args:
        enc_zip: ZipFile instance of the encrypted zip
        file_ext: File extension of known file in archive

    Returns:
        The ZipInfo instance of the file if found
        None if a file with the given file extension is not found
    """
    for info in enc_zip.infolist():
        if file_ext in info.filename:
            return info


def find_password(enc_zip, file_sig, info, pw_source=sys.stdin):
    """Attempts to find the password for an encrypted zip.

    Attempts to extract the file provided by info from
    the archive with passwords provided from pw_source.
    To minimize false positives the method checks the file signature
    of the extracted file to make sure it's valid

    Args:
        enc_zip: A ZipFile instance of the encrypted zip
        file_sig: File signature of the file used for validation
        info: A ZipInfo instance of the file used for validation
        pw_source: Source of stream of passwords. The default is stdin
    Returns:
       If the password is found, then it returns the password
       If the password is not found, then it returns None
    """
    found_it = False
    for line in pw_source:
        guess_pwd = line.strip().rstrip().encode("utf-8", "ignore")
        try:
            with enc_zip.open(info, "r", pwd=guess_pwd) as myzip:
                try:
                    head = myzip.__next__()
                    if file_sig in head:
                        found_it = True
                        guess_pwd = str(guess_pwd, "utf-8")
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
