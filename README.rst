Plex Version Downloader
=======================

Plex Version Downloader is tool designed to allow the quick and easy downloading of the latest version of Plex software from plex.tv_.

.. code-block:: shell

    $ plex_download -s server ubuntu
    ubuntu linux-ubuntu-x86_64 (1.2.6.2975-9394c87)
    ubuntu linux-ubuntu-i686 (1.2.6.2975-9394c87)

    $ plex_download server ubuntu linux-ubuntu-x86_64
    plex_download: starting download...
    plex_download: download complete

    $ plex_download -h
    usage: plex_download [-h] [-v] [-V] [-s] [-S] [-u USERNAME] [-p PASSWORD]
                         [-d DESTINATION]
                         [PLATFORM] [DISTRO] [BUILD]

    Plex Version Downloader

    positional arguments:
      PLATFORM              the platform of the version to download (possible
                            values: server, theater, player, player_embedded)
      DISTRO                the distro of the version to download
      BUILD                 the build of the version to download

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         enable verbose output (use twice for more)
      -V, --version         print version information and exit
      -s, --show-versions   show server versions without downloading
      -S, --show-versions-only
                            show server versions without downloading and without
                            extra metadata
      -u USERNAME, --username USERNAME
                            set plex account username
      -p PASSWORD, --password PASSWORD
                            set plex account password
      -d DESTINATION, --destination DESTINATION
                            set download location

    showing a list of the latest normal server versions:
      plex_download -s server

    showing a list of the latest plex pass server versions:
      plex_download -s -u "AzureDiamond" -p "hunter2" server

    downloading non plex pass server version:
      plex_download server ubuntu linux-ubuntu-x86_64

    downloading plex pass server version:
      plex_download -u "AzureDiamond" -p "hunter2" server english windows-i386

    downloading the latest server to a specific directory:
      plex_download -d ~/downloads server macosx darwin-x86_64

    downloading the latest server to a specific path:
      plex_download -d ~/downloads/plex.deb server synology linux-synology-i686

.. _plex.tv: https://plex.tv
