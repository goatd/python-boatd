from distutils.core import setup

with open('README.md') as file:
        long_description = file.read()

setup(
    name='goatd_client',
    version='0.1',
    author='Louis Taylor',
    author_email='kragniz@gmail.com',
    description=('Python wrapper for the goatd API, used to write behavior scripts.'),
    long_description=long_description,
    license='GPL',
    keywords='goat sailing wrapper rest',
    url='https://github.com/goatd/python-goatd',
    packages=['goatd_client'],
    requires=['docopt'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
