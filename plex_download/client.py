from __future__ import absolute_import

import plex_version

import plex_download.version


class DownloadClient(plex_version.Client):
    version_class = plex_download.version.DownloadablePlexVersion


__all__ = ('DownloadClient',)
