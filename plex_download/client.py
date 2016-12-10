from __future__ import absolute_import

import plex_version

import plex_download.version


class DownloadClient(plex_version.Client):
    version_class = plex_download.version.DownloadablePlexVersion

    def __init__(self, *args, **kwargs):
        self.interface = kwargs.pop('interface', None)

        super(DownloadClient, self).__init__(*args, **kwargs)

    def debug(self, message, *args, **kwargs):
        if self.interface is not None:
            self.interface.debug(1, message, *args, **kwargs)

    def request(self, *args, **kwargs):
        self.debug('{} request to {} (args={}, kwargs={})', args[0].lower(),
                   args[1], args, kwargs)

        return super(DownloadClient, self).request(*args, **kwargs)


__all__ = ('DownloadClient',)
