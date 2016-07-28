'''Plex Version Downloader

Version information is retrieved using plex_version.
'''

from os import path as _path
import setuptools as _setuptools
from setup_functions import get_file_content, get_assignment_value


setup_directory = _path.dirname(__file__)
init_path = _path.join(setup_directory, 'plex_downloader', '__init__.py')
readme_path = _path.join(setup_directory, 'README.rst')


_setuptools.setup(
    name='plex_downloader',
    version=get_assignment_value(init_path, '__version__', True),
    description='Plex Version Downloader',
    long_description=get_file_content(readme_path),
    author='Jack Wilsdon',
    author_email='jack.wilsdon@gmail.com',
    url='https://github.com/jackwilsdon/plex_downloader',
    license='AGPL-3.0',
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
    keywords='plex downloader',
    packages=['plex_downloader'],
    entry_points={
        'console_scripts': ['plex_downloader=plex_downloader.__main__:main'],
    },
    dependency_links=[
        ('git+https://github.com/jackwilsdon/plex_version.git@1.0.7'
            '#egg=plex_version-1.0.7')
    ],
    install_requires=[
        'plex_version==1.0.7'
    ]
)
