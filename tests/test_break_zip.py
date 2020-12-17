import os
import pytest
from zipfile import ZipFile
from breakzip.breakzip import FileSignature, find_password, get_info


@pytest.fixture
def enc_zip(rootdir):
    """Returns an EncryptedZipFile instance with a test zip"""
    test_zip = os.path.join(rootdir, "cats.zip")
    return ZipFile(test_zip)


def test_enc_zip_get_info_correct_ext(enc_zip):
    file_ext = "jpg"
    info = get_info(enc_zip, file_ext)
    assert info


def test_enc_zip_get_info_incorrect_ext(enc_zip):
    file_ext = "dos"
    info = get_info(enc_zip, file_ext)
    assert not info


def test_find_password_correct_pwd(enc_zip):
    file_ext = "jpg"
    info = get_info(enc_zip, file_ext)
    file_sig = FileSignature().get_file_sig(file_ext)
    assert find_password(enc_zip, file_sig, info, pw_source=["fun"]) == "fun"


def test_find_password_incorrect_pwd(enc_zip):
    file_ext = "jpg"
    info = get_info(enc_zip, file_ext)
    file_sig = FileSignature().get_file_sig(file_ext)
    assert not find_password(enc_zip, file_sig, info, pw_source=["buns"])


def test_get_file_sig():
    file_ext = "asf"
    file_sig = FileSignature().get_file_sig(file_ext)
    assert file_sig == b"\x30\x26\xb2"
