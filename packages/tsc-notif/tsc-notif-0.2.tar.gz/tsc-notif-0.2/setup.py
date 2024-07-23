from setuptools import setup, find_packages


with open('version.txt', 'r') as f:
    version = f.read().strip()
with open('url.txt', 'r') as f:
    url = f.read().strip() or None
with open('readme.md', 'r') as f:
    long_description = f.read()


setup(
    name='tsc-notif',
    version=version,
    description="自动通知",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='aitsc',
    url=url,
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
