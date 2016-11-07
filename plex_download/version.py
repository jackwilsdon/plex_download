
import posixpath as path

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import plex_version
import requests


class DownloadablePlexVersion(plex_version.PlexVersion):
    def __init__(self, *args, **kwargs):
        super(DownloadablePlexVersion, self).__init__(*args, **kwargs)

    @property
    def filename(self):
        url_pieces = urlparse.urlparse(self.url)
        urlpath = path.normpath(url_pieces.path)
        return path.basename(urlpath)

    def download(self, destination):
        response = requests.get(self.url, stream=True)
        response.raise_for_status()

        with open(destination, 'wb') as destfile:
            for block in response.iter_content(1024):
                if block:
                    destfile.write(block)


__all__ = ('DownloadablePlexVersion',)
