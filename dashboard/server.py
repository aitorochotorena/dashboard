import sys
from .utils import log
from .app import Dashboard


def main():
    d = Dashboard()
    d.parse_command_line(sys.argv)
    try:
        d.start()
    except KeyboardInterrupt:
        log.critical('Exiting...')


if __name__ == "__main__":
    main()
