try:
    import urlparse as _urlparse
except ImportError:
    import urllib.parse as _urlparse

from os import path as _path
import requests as _requests

from plex_version import version as _plex_version


class DownloadablePlexVersion(_plex_version.PlexVersion):
    def __init__(self, *args, **kwargs):
        super(DownloadablePlexVersion, self).__init__(*args, **kwargs)

    @property
    def filename(self):
        url_pieces = _urlparse.urlparse(self.url)
        url_path = _path.normpath(url_pieces.path)

        return _path.basename(url_path)

    def download(self, destination):
        response = _requests.get(self.url, stream=True)
        response.raise_for_status()

        with open(destination, 'wb') as destfile:
            for block in response.iter_content(1024):
                if block:
                    destfile.write(block)

    @classmethod
    def from_version(cls, version):
        return cls(**vars(version))


__all__ = ('DownloadablePlexVersion',)
