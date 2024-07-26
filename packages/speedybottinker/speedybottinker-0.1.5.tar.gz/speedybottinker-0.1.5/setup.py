from setuptools import setup, find_packages

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from version import __version__

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


print(__version__)


setup(
    name="speedybottinker",
    version=__version__,
    author="Victor Algaze",
    author_email="valgaze@gmail.com",
    description="Use googles-- highly experimental conversation design infra",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/valgaze/speedybot-loco",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
        entry_points={
        'console_scripts': [
            'speedybot-loco = speedybot.cli:main',
        ],
    },
)
