from __future__ import absolute_import

from os import path

import setuptools

import setup_functions


setup_directory = path.dirname(__file__)
init_path = path.join(setup_directory, 'plex_download', '__init__.py')
readme_path = path.join(setup_directory, 'README.rst')
version = setup_functions.get_assignment_value(init_path, '__version__', True)
readme = setup_functions.get_file_content(readme_path)


setuptools.setup(
    name='plex_download',
    version=version,
    description='Plex Version Downloader',
    long_description=readme,
    author='Jack Wilsdon',
    author_email='jack.wilsdon@gmail.com',
    url='https://github.com/jackwilsdon/plex_download',
    packages=['plex_download'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    license='AGPL-3.0',
    keywords='plex downloader',
    entry_points={
        'console_scripts': ['plex_download=plex_download.__main__:main'],
    },
    install_requires=[
        'plex_version>=1.1.1,<2'
    ]
)


__all__ = ()
