from setuptools import setup, find_packages

setup(name='breakzip',
        version='0.1',
        description='',
        author='Michael Terrell',
        author_email='cwithmichael@gmail.com',
        license='MIT',
        packages=find_packages(),
        tests_require=['pytest', 'pytest-mock'],
        entry_points = {
            'console_scripts': ['breakzip=breakzip.command_line:main'],
        },
        zip_safe=False
)
