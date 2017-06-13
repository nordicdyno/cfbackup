import cfbackup
from setuptools import setup, find_packages

install_requires = [
    'cloudflare>=1.5.1',
    'argparse>=1.2.1',
]

setup(
    name='cfbackup',
    version=cfbackup.__version__,
    description=cfbackup.__doc__.strip(),
    url='https://github.com/nordicdyno/cfbackup',
    download_url='https://github.com/nordicdyno/cfbackup',
    author=cfbackup.__author__,
    author_email='nordicdyno@gmail.coms',
    license=cfbackup.__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cfbackup = cfbackup.__main__:main',
        ],
    },
    install_requires=install_requires,
)
