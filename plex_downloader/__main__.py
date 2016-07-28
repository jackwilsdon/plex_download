from __future__ import print_function as _print_function

from os import path as _path
import collections as _collections
import sys as _sys
import argparse as _argparse

import plex_version as _plex_version
import plex_downloader as _plex_downloader


if _sys.argv[0].endswith('__main__.py'):
    _executable = _path.basename(_sys.executable)
    _PROGRAM_NAME = _sys.argv[0] = '{} -m plex_downloader'.format(_executable)
else:
    _PROGRAM_NAME = _path.basename(_sys.argv[0])


_HELP_EPILOG = '''
showing a list of the latest normal server versions:
  {filename} -t server -s

showing a list of the latest plex pass server versions:
  {filename} -t server -s -u "Joe Bloggs" -p "hunter123"

downloading non plex pass server version:
  {filename} -t server ubuntu linux-ubuntu-x86_64

downloading plex pass server version:
  {filename} -t server -u "Joe Bloggs" -p "hunter123" ubuntu \
linux-ubuntu-x86_64

downloading to a specific directory:
  {filename} -t server -d ~/downloads ubuntu linux-ubuntu-x86_64

downloading to a specific path:
  {filename} -t server -d ~/downloads/plex.deb ubuntu linux-ubuntu-x86_64
'''.format(filename=_PROGRAM_NAME)

_PLATFORMS = _collections.OrderedDict([
    ['server', _plex_version.version.PLEX_MEDIA_SERVER],
    ['theater', _plex_version.version.PLEX_HOME_THEATER],
    ['player', _plex_version.version.PLEX_MEDIA_PLAYER],
    ['player_embedded', _plex_version.version.PLEX_MEDIA_PLAYER_EMBEDDED]
])

_PLATFORM_TEXT = ', '.join(_PLATFORMS.keys())


def _error(message, *args, **kwargs):
    message = message.format(*args, **kwargs)

    print('{}: error: {}'.format(_PROGRAM_NAME, message), file=_sys.stderr)

    _sys.exit(1)


def _message(message, *args, **kwargs):
    message = message.format(*args, **kwargs)

    print('{}: {}'.format(_PROGRAM_NAME, message))


def _validate_platform(platform):
    if platform not in _PLATFORM_TEXT:
        raise _argparse.ArgumentTypeError('must be one of {}'.format(
                                          _PLATFORM_TEXT))

    return _PLATFORMS[platform]


def _parse_arguments():
    parser = _argparse.ArgumentParser(
        formatter_class=_argparse.RawDescriptionHelpFormatter,
        description='Plex Version Downloader',
        epilog=_HELP_EPILOG)

    parser.add_argument('-t', '--platform',
                        type=_validate_platform,
                        help='type of plex software to download (possible '
                        'values: {})'.format(_PLATFORM_TEXT),
                        dest='platform',
                        required=True)

    parser.add_argument('-s', '--show-latest',
                        action='store_true',
                        help='show latest server versions',
                        dest='print_versions')

    parser.add_argument('-r', '--version-only',
                        action='store_true',
                        help='only print version (use with -s)',
                        dest='print_version_only')

    parser.add_argument('-u', '--username',
                        help='set plex account username',
                        dest='username')

    parser.add_argument('-p', '--password',
                        help='set plex account password',
                        dest='password')

    parser.add_argument('-d', '--destination',
                        help='set download location',
                        dest='destination')

    parser.add_argument('-v', '--version',
                        action='store_true',
                        help='print version information and exit',
                        dest='print_version')

    parser.add_argument('distro',
                        metavar='DISTRO',
                        nargs='?',
                        help='the distro of the version to download')

    parser.add_argument('build',
                        metavar='BUILD',
                        nargs='?',
                        help='the build of the version to download')

    return parser.parse_args()


def _raw_main(print_version, print_versions, print_version_only, username,
              password, platform, distro, build, destination):
    if print_version:
        print(_plex_downloader.__version__)
        return

    if not print_versions:
        if print_version_only:
            _error('-s/--show-latest is required to use -r/--version-only')

        if distro is None:
            _error('missing distro')

        if build is None:
            _error('missing build')

    client = _plex_downloader.client.DownloadClient(username, password)

    versions = client.get(platform, distro, build,
                          username is not None and password is not None)

    if len(versions) == 0:
        _error('no versions found')

    if print_versions:
        for version in versions:
            if print_version_only:
                print(version.version_string)
            else:
                print(str(version))
    else:
        if len(versions) > 1:
            _error('multiple versions found')

        version = versions[0]

        if destination is None:
            destination = version.filename

        if _path.isdir(destination):
            destination = _path.join(destination, version.filename)

        _message('starting download for "{}" to "{}"', version,
                 _path.relpath(destination))

        if _path.lexists(destination):
            _error('destination file already exists')

        version.download(destination)

        _message('download completed successfully')


def main():
    args = _parse_arguments()
    return main(**vars(args))


if __name__ == '__main__':
    main()
