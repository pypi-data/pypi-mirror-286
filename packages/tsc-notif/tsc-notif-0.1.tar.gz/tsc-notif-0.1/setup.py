from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

version_txt = os.path.join(here, 'tsc_notif/version.txt')
with open(version_txt, 'r') as f:
    version = f.read().strip()
    
setup(
    name='tsc-notif',
    version=version,
    packages=find_packages(),
    install_requires=[
        'pydantic',
        'tenacity',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'supervisor-eventlistener=tsc_notif.supervisor_eventlistener:main',
        ],
    },
    python_requires='>=3.7',
)
