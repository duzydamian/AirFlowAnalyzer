#!/usr/bin/pythons
#
# Author : Damian Karbowiak
# Company: Silesian Softing
#
# Date   : 20.06.2017
#

##################################################################################################################
# IMPORT BIBLIOTEK
##################################################################################################################
import os
import sys
from setuptools import setup, find_packages

def checkPathAndRemove(path):
    if os.path.exists(path):
        for fileName in os.listdir(path):
            fileNameWithPath = os.path.join(path, fileName)
            os.remove(fileNameWithPath)
            
here = os.path.abspath(os.path.dirname(__file__))
checkPathAndRemove(here+"/dist")
#README = open(os.path.join(here, 'README.txt')).read()
#CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

if "--version" in sys.argv:
    wersja = sys.argv.pop(sys.argv.index("--version")+1)
    sys.argv.remove("--version") 
        
requires = [
    'pygatt',    
    'pyexpect',
]

setup(
    name='ss-afa-tc',
    version=wersja,
    description='Testo Concentrator software to run on Raspberry Pi for example to get and collect data from many sensors.',
    #long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Damian Karbowiak',
    author_email='',
    url='',
    keywords='testo sensor air flow',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
#    console=["run.py"],
)
