from setuptools import setup, find_packages

setup(
    name='hadolint-py',
    version='0.1.0', # This version is not used for determining hadolint version
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hadolint = hadolint_py.main:main',
        ],
    },
)