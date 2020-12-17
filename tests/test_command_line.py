from breakzip import command_line
import unittest
import pytest
import os
from unittest.mock import Mock

@pytest.fixture
def enc_zip(rootdir):
    '''Returns an EncryptedZipFile instance with a test zip'''
    test_zip = os.path.join(rootdir, 'cats.zip')
    return test_zip

def test_reading_file(enc_zip, mocker):
	mocker.patch.object(command_line.sys, 'argv')
	mocker.patch.object(command_line.breakzip, 'get_info')
	mocker.patch.object(command_line.breakzip, 'find_password')
	command_line.sys.argv = ['', enc_zip, 'jpg']
	command_line.main()
	assert command_line.breakzip.get_info.called_once()
	assert command_line.breakzip.find_password.called_once()

def test_reading_file_not_found(enc_zip, mocker):
	mocker.patch.object(command_line.sys, 'argv')
	command_line.sys.argv = ['', '', 'jpg']
	with pytest.raises(FileNotFoundError):
		command_line.main()

def test_reading_ext_not_found(enc_zip, mocker):
	mocker.patch.object(command_line.sys, 'argv')
	command_line.sys.argv = ['', enc_zip, 'drwho']
	with pytest.raises(SystemExit):
		command_line.main()

def test_insufficient_input(enc_zip, mocker):
	mocker.patch.object(command_line.sys, 'argv')
	command_line.sys.argv = ['', '']
	with pytest.raises(SystemExit) as e:
		command_line.main()
	assert "Usage" in str(e.value)
