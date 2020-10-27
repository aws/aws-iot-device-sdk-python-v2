import argparse
import subprocess
import sys
import time

DEFAULT_TIMEOUT = 60 * 30 # 30 min
DEFAULT_INTERVAL = 5
DEFAULT_INDEX_URL = 'https://pypi.python.org/pypi'


def wait(package, version, index_url=DEFAULT_INDEX_URL, timeout=DEFAULT_TIMEOUT, interval=DEFAULT_INTERVAL):
    give_up_time = time.time() + timeout
    while True:
        output = subprocess.check_output([sys.executable, '-m', 'pip', 'search',
                                          '--no-cache-dir', '--index', index_url, package])
        output = output.decode()

        # output looks like: 'awscrt (0.3.1)  - A common runtime for AWS Python projects\n...'
        if output.startswith('{} ({})'.format(package, version)):
            return True

        if time.time() >= give_up_time:
            return False

        time.sleep(interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('package', help="Packet name")
    parser.add_argument('version', help="Package version")
    parser.add_argument('--index', default=DEFAULT_INDEX_URL, metavar='<url>',
                        help="Base URL of Python Package Index. (default {})".format(DEFAULT_INDEX_URL))
    parser.add_argument('--timeout', type=float, default=DEFAULT_TIMEOUT, metavar='<sec>',
                        help="Give up after N seconds.")
    parser.add_argument('--interval', type=float, default=DEFAULT_INTERVAL, metavar='<sec>',
                        help="Query PyPI every N seconds")
    args = parser.parse_args()

    if wait(args.package, args.version, args.index, args.timeout, args.interval):
        print('{} {} is available in pypi'.format(args.package, args.version))
    else:
        exit("Timed out waiting for pypi to report {} {} as latest".format(args.package, args.version))
