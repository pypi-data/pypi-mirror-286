from setuptools import setup

NAME = 'Orange3-BPK-CAATT'

MAJOR = 1
MINOR = 1
MICRO = 1
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

DESCRIPTION = 'Orange3 Computer Assisted Audit Technique Tools (CAATT) add-on.'
AUTHOR = 'The Audit Board of The Republic of Indonesia (BPK-RI)'
AUTHOR_EMAIL = 'eppid@bpk.go.id'
URL = 'https://www.bpk.go.id/'

KEYWORDS = [
    'orange3-caatt',
    'caatt',
    'bpk-caatt'
]

ENTRY_POINTS = {
    'orange.widgets': (
        'BPK CAATT = caatt'
    )
}

PACKAGES = ['caatt']
PACKAGE_DATA = {
    'caatt' : ["icons/*.svg"]
}

setup(
    name=NAME,
    description=DESCRIPTION,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    entry_points=ENTRY_POINTS,
    keywords=KEYWORDS
)