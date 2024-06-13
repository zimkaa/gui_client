import re
from collections import defaultdict
from pathlib import Path


def get_stats() -> None:
    damage_persons = defaultdict(int)  # type: ignore[var-annotated]

    with Path("./INFO/fight/564819006.txt").open() as file:
        for line in file:
            if "130000" in line:
                pattern = r"<B>(?:<font color=#CC0000>)?-(\d+)(?:</font>)?</B>"
                matches = re.findall(pattern, line)
                damage = 0
                for match in matches:
                    damage += int(match)

                new_line = line.replace("Кхалганский Налетчик 29", "")
                pattern = r" ([^<|>|.|,]{,30}) \d{2} "
                matches = re.findall(pattern, new_line)
                name = matches[0]
                if matches[0].startswith("но "):
                    name = matches[0].replace("но ", "")

                if "удар  от" in matches[0]:
                    index = matches[0].find("от ")
                    if index != -1:
                        name = matches[0][index:].replace("от ", "")

                damage_persons[name] += damage

    sorted_dict = dict(sorted(damage_persons.items(), key=lambda item: item[1], reverse=True))
    print(f"{sorted_dict=}")  # noqa: T201
    print(f"{len(sorted_dict)=}")  # noqa: T201
    print(f"{sum(sorted_dict.values())=}")  # noqa: T201
