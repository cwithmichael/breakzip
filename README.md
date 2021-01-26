## BreakZip

[![Build Status](https://travis-ci.org/cwithmichael/breakzip.svg?branch=master)](https://travis-ci.org/cwithmichael/breakzip)


### Motivation
This program was created for a very specfic problem I had. I had a large encrypted zip file that I lost/forgot the password for. Using traditional bruteforce methods resulted in a lot of false positives.

This program hopes to minimize false positives. It works by actually checking to see if a given file type exists in the 'plaintext' after attempting a guess password.
More info about Python's ZipFile lib can be found here:
https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.open

### Requirements
Python >= 3.9

### Installation Instructions (Recommended)
Make sure you have [Pipenv installed](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

Install the requirements and start a pipenv shell

`pipenv install` 

`pipenv shell`


### Running Tests

If you want to run the tests, then you'll have to install `pytest`

`pipenv install -e ".[testing]"`

`pytest`


### Installation Instructions (Without Pipenv)
Create a virtualenv and activate it 

`python3 -m venv venv`

`source venv/bin/activate` 

Run install

`python setup.py install`


### Running Tests

If you want to run the tests, then you'll have to install `pytest`

`pip install -e ".[testing]"`

`pytest`


### Usage
`breakzip <zipfile_name> <known_file_extension>`

Let's say we had an encrypted zip file named `cats.zip` with a jpg file in it.
In this example the password is `fun` and our wordlist contains `fun`.

```
$ breakzip cats.zip jpg < wordlist
Found it! -> fun
```

We can also use a password generator like JohnTheRipper to provide passwords.

```
$ ./JohnTheRipper/run/john --mask=fu?a -stdout | breakzip cats.zip jpg
Press 'q' or Ctrl-C to abort, almost any other key for status
95p 0:00:00:00 100.00% (2020-04-13 17:35) 1520p/s fu|
Found it! -> fun
```

### Important Notes
Supports PKZip/ZipCrypto Encryption _only_

Only a limited number of file types are supported at the moment: zip, wmv/asf/wma, jpg, png, xml

But it's pretty easy to extend support for various file types.
