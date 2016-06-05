try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='python-goatdclient',
    version='0.7.0',
    author='Louis Taylor',
    author_email='louis@kragniz.eu',
    description=('Python wrapper for the goatd API, used to write behavior scripts.'),
    long_description=open("README.rst").read(),
    license='GPL',
    keywords='goat sailing wrapper rest',
    url='https://github.com/goatd/python-goatd',
    packages=['goatdclient'],
    scripts=['goatdctl'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
