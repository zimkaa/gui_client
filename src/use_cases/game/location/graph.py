from enum import Enum


oktal_graph = {
    "city2_1": ["city2_2", "city2_3"],
    "city2_3": ["city2_1", "city2_6", "city2_4"],
    "city2_6": ["city2_3", "city2_9", "city2_7"],
    "city2_9": ["city2_6"],
    "city2_7": ["city2_6", "city2_4", "city2_8"],
    "city2_8": ["city2_7", "city2_5"],
    "city2_5": ["city2_8", "city2_4"],
    "city2_4": ["city2_5", "city2_7", "city2_3", "city2_2"],
    "city2_2": ["city2_4", "city2_1"],
}


class CitiesGraph(Enum):
    FP = 1
    OKTAL = oktal_graph
    PODGORN = 3
    OKREST_FEIDANA = 4
    OKREST_OKTAL = 5
    OKREST_ERINGARD = 6
    OKREST_FP = 7
    SAMYM_BEYT = 8
    NORTHERN_TRACT = 9
    EASTERN_FORESTS = 10
    OKREST_KENGI = 11
    GORGE_EL_TER = 12
