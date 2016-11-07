Plex Version Downloader Changelog
=================================

1.0.6
-----
 - Fix outdated documentation
 - Add platform variety to documentation
 - Update changelog to cover previous versions

1.0.5
-----
 - Add usage examples to documentation

1.0.4
-----
 - Increment ``plex_version`` dependency version to 1.1.1

1.0.3
-----
 - Add ``setup_functions.py`` to distribution

1.0.2
-----
 - Update changelog to cover previous versions
 - Improve ``setup.py`` layout
 - Use ``__all__`` instead of an underscore prefix on variables and imports
 - Import all classes into the top-level ``plex_downlaod`` module

1.0.1
-----
 - Make PLATFORM, DISTRO and BUILD optional for version query
 - Rename ``-r/--version-only`` argument to ``-S/--show-version-only`` and make it mutually exclusive with ``-s/--show-versions``

1.0.0
-----
 - Improve CLI interface for downloading versions
 - Rename ``DownloadClient`` to ``Client``

0.1.5
-----
 - General code improvements

0.1.4
-----
 - Use correct python executable when setting argv

0.1.3
-----
 - Add special argv case for ``__main__``

0.1.2
-----
 - Run main if needed

0.1.1
-----
 - Move main logic into ``plex_downloader/__main__.py``

0.1.0
-----
 - Initial release
