from plex_version import client as _plex_client
from plex_version import version as _plex_version

from plex_download import version as _version


class Client(_plex_client.Client):
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)

    def _wrap_versions(self, versions):
        versions_copy = versions[:]

        for index, version in enumerate(versions_copy):
            if isinstance(version, _plex_version.PlexVersion):
                versions_copy[index] = (_version.DownloadablePlexVersion
                                                .from_version(version))

        return versions_copy

    def get(self, *args, **kwargs):
        matches = super(Client, self).get(*args, **kwargs)

        self.versions = self._wrap_versions(self.versions)

        return self._wrap_versions(matches)


__all__ = ('Client',)
