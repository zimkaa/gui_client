class WrongIPError(Exception): ...


class NoCookiesFolderError(Exception): ...


class PersonNotFoundError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Person {name} not found")
