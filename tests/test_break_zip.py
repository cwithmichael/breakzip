import os
import pytest
from breakzip.breakzip import alias_keys, file_types, find_password, EncryptedZipFile

@pytest.fixture
def enc_zip(rootdir):
    '''Returns an EncryptedZipFile instance with a test zip'''
    test_zip = os.path.join(rootdir, 'cats.zip')
    return EncryptedZipFile(test_zip)

def test_enc_zip_get_info_correct_ext(enc_zip):
    file_ext = 'jpg'
    info = enc_zip.get_info(file_ext)
    assert info

def test_enc_zip_get_info_incorrect_ext(enc_zip):
    file_ext = 'dos'
    info = enc_zip.get_info(file_ext)
    assert not info

def test_find_password_correct_pwd(enc_zip):
    file_ext = 'jpg'
    info = enc_zip.get_info(file_ext)
    file_type = file_types[alias_keys[file_ext]]
    assert find_password(enc_zip, file_type, info, pw_source=['fun']) == 'fun'

def test_find_password_incorrect_pwd(enc_zip):
    file_ext = 'jpg'
    info = enc_zip.get_info(file_ext)
    file_type = file_types[alias_keys[file_ext]]
    assert not find_password(enc_zip, file_type, info, pw_source=['buns'])

def test_alias():
    file_ext = 'asf'
    assert alias_keys[file_ext] == 2 
    assert file_types[2] == b'\x30\x26\xb2'

