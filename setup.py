# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='yaml-injection',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    description='pyyaml loader. '
                'With this loader you can inject (include) other yaml files '
                'either from local file system '
                'or from public web '
                'or from already constructed sections of the yaml.',
    author='Grigorii Koksharov',
    author_email='grigorii.koksharov@pthystech.edu',
    url='https://github.com/oztqa/yaml-injection',
    py_modules=['yaml_injection'],
    install_requires=[
        'pyyaml',
        'requests',
    ],
    keywords='yaml pyyaml include extend inject',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
