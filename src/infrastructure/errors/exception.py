class WrongIPError(Exception):
    """Wrong IP"""


class PersonNotFoundError(Exception):
    """Person not found."""

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Person {name} not found")
