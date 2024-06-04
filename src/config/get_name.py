import sys

from .project_info import get_name


def main() -> None:
    sys.stdout.write(f"{get_name()}\n")


if __name__ == "__main__":
    main()
