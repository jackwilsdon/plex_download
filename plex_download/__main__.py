from __future__ import absolute_import, print_function

import argparse
import collections
import sys
import textwrap
from os import path

import plex_version

import plex_download


class _DownloaderArgumentParser(argparse.ArgumentParser):
    def __init__(self, interface, *args, **kwargs):
        super(_DownloaderArgumentParser, self).__init__(*args, **kwargs)
        self.interface = interface

    def error(self, *args, **kwargs):
        self.print_usage(sys.stderr)
        self.interface.error(*args, **kwargs)


class DownloaderInterface(object):
    HELP_EPILOG = textwrap.dedent('''\
    showing a list of the latest normal server versions:
      {filename} -t server -s

    showing a list of the latest plex pass server versions:
      {filename} -t server -s -u "Joe Bloggs" -p "hunter123"

    downloading non plex pass server version:
      {filename} -t server ubuntu linux-ubuntu-x86_64

    downloading plex pass server version:
      {filename} -t server -u "Joe Bloggs" -p "hunter123" ubuntu \
    linux-ubuntu-x86_64

    downloading the latest server to a specific directory:
      {filename} -t server -d ~/downloads ubuntu linux-ubuntu-x86_64

    downloading the latest server to a specific path:
      {filename} -t server -d ~/downloads/plex.deb ubuntu linux-ubuntu-x86_64
    ''')

    PLATFORMS = collections.OrderedDict([
        ['server', plex_version.PLEX_MEDIA_SERVER],
        ['theater', plex_version.PLEX_HOME_THEATER],
        ['player', plex_version.PLEX_MEDIA_PLAYER],
        ['player_embedded', plex_version.PLEX_MEDIA_PLAYER_EMBEDDED]
    ])

    PLATFORM_TEXT = ', '.join(PLATFORMS.keys())

    def __init__(self, module=None, command=None):
        if module is None:
            self.module = path.basename(path.dirname(__file__))
        else:
            self.module = module

        if command is None:
            self.command = self.module
        else:
            self.command = command

    def raw_message(self, message, *args, **kwargs):
        print(str(message).format(*args, **kwargs))

    def message(self, message, *args, **kwargs):
        message = str(message).format(*args, **kwargs)
        self.raw_message('{}: {}', self.module, message)

    def raw_error(self, message, *args, **kwargs):
        print(str(message).format(*args, **kwargs), file=sys.stderr)
        self.exit(1)

    def error(self, message, *args, **kwargs):
        message = str(message).format(*args, **kwargs)
        self.raw_error('{}: error: {}', self.module, message)

    def exit(self, code=0):
        sys.exit(code)

    def print_library_version(self):
        self.raw_message('{} (plex_version {})', plex_download.__version__,
                         plex_version.__version__)

    def _get_versions(self, platform, distro=None, build=None, username=None,
                      password=None, strict=True):
        client = plex_download.DownloadClient(username, password)

        versions = client.get(platform, distro, build, client.logged_in)

        if len(versions) == 0 and strict:
            self.error('no versions found')

        return versions

    def print_versions(self, platform, distro=None, build=None, username=None,
                       password=None, version_only=False):
        versions = self._get_versions(platform, distro, build, username,
                                      password)

        if version_only:
            versions = [version.version_string for version in versions]
        else:
            versions = [str(version) for version in versions]

        self.raw_message('\n'.join(versions))

    def download_version(self, platform, distro, build, username=None,
                         password=None, destination=None):
        versions = self._get_versions(platform, distro, build, username,
                                      password)

        if len(versions) > 1:
            self.error('found {} versions', len(versions))

        version = versions[0]

        if destination is None:
            destination = version.filename

        if path.isdir(destination):
            destination = path.join(destination, version.filename)

        if path.lexists(destination):
            self.error('file already exists')

        self.message('starting download...')

        version.download(destination)

        self.message('download complete')

    def _validate_platform(self, platform):
        if platform not in self.PLATFORMS:
            raise argparse.ArgumentTypeError('must be one of {}'.format(
                                              self.PLATFORM_TEXT))

        return self.PLATFORMS[platform]

    def _execute_arguments(self, arguments):
        if arguments['print_library_version']:
            return self.print_library_version()
        elif arguments['print_versions'] or arguments['print_versions_only']:
            return self.print_versions(
                platform=arguments['platform'],
                distro=arguments['distro'],
                build=arguments['build'],
                username=arguments['username'],
                password=arguments['password'],
                version_only=arguments['print_versions_only']
            )
        else:
            return self.download_version(
                platform=arguments['platform'],
                distro=arguments['distro'],
                build=arguments['build'],
                username=arguments['username'],
                password=arguments['password'],
                destination=arguments['destination'],
            )

    def execute(self, arguments=None):
        parser = _DownloaderArgumentParser(
            self,
            prog=self.command,
            description='Plex Version Downloader',
            epilog=self.HELP_EPILOG.format(filename=self.command),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        parser.add_argument('-v', '--version',
                            action='store_true',
                            help='print version information and exit',
                            dest='print_library_version')

        parser.add_argument('-s', '--show-versions',
                            action='store_true',
                            help='show server versions without downloading',
                            dest='print_versions')

        parser.add_argument('-S', '--show-versions-only',
                            action='store_true',
                            help='show server versions without downloading '
                                 'and without extra metadata',
                            dest='print_versions_only')

        parser.add_argument('-u', '--username',
                            help='set plex account username',
                            dest='username')

        parser.add_argument('-p', '--password',
                            help='set plex account password',
                            dest='password')

        parser.add_argument('-d', '--destination',
                            help='set download location',
                            dest='destination')

        parser.add_argument('platform',
                            nargs='?',
                            type=self._validate_platform,
                            help=('the platform of the version to download'
                                  ' (possible values: {})').format(
                                  self.PLATFORM_TEXT),
                            metavar='PLATFORM')

        parser.add_argument('distro',
                            nargs='?',
                            help='the distro of the version to download',
                            metavar='DISTRO')

        parser.add_argument('build',
                            nargs='?',
                            help='the build of the version to download',
                            metavar='BUILD')

        parsed_arguments = vars(parser.parse_args(arguments))
        required_arguments = []

        if not parsed_arguments['print_library_version']:
            if (parsed_arguments['print_versions'] and
                    parsed_arguments['print_versions_only']):
                parser.error('-s/--show-versions cannot be used with '
                             '-S/--show-versions-only')

            if parsed_arguments['platform'] is None:
                required_arguments.append('PLATFORM')

            if (not parsed_arguments['print_versions'] and
                    not parsed_arguments['print_versions_only']):
                if parsed_arguments['distro'] is None:
                    required_arguments.append('DISTRO')

                if parsed_arguments['build'] is None:
                    required_arguments.append('BUILD')

            if len(required_arguments) > 0:
                parser.error('the following arguments are required for '
                             'downloading: {}', ', '.join(required_arguments))

        result = self._execute_arguments(parsed_arguments)

        return result if result is not None else 0


def main():
    module = path.basename(path.dirname(__file__))
    command = None

    if path.samefile(__file__, sys.argv[0]):
        executable = path.basename(sys.executable)
        command = '{} -m {}'.format(executable, module)

    interface = DownloaderInterface(module, command)

    try:
        result = interface.execute()
        interface.exit(result)
    except Exception as exception:
        interface.error(exception)


if __name__ == '__main__':
    main()


__all__ = ()
