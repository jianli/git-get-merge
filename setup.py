from setuptools import find_packages
from setuptools import setup


setup(
    name='git-get-merge',
    version='0.1',
    url='http://github.com/jianli/git-get-merge',
    packages=find_packages('.'),
    entry_points={
        'console_scripts': (
            'git-get-merge = get_merge:get_merge',
        ),
    },
    install_requires=[
        'gitpython',
    ],
)
