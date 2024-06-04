import sys

from .project_info import get_version


def main() -> None:
    sys.stdout.write(f"{get_version()}\n")


if __name__ == "__main__":
    main()
