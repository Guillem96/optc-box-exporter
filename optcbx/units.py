from typing import Any, List, NamedTuple


class Character(NamedTuple):
    name: str
    type_: str
    class_: List[str]
    stars: str
    number: int


def parse_unit(i: int, unit: List[Any]) -> Character:
    return Character(name=unit[0], type_=unit[1], class_=unit[2],
                     stars=unit[3], number=i)


def parse_units(units: List[List[Any]]) -> List[Character]:
    units = [viable_unit(o) for o in units]
    return [parse_unit(i, o) for i, o in enumerate(units, start=1) if o]


def viable_unit(unit: str) -> List[Any]:
    if all(o is not None for o in unit):
        return unit
    
    if all(unit[i] is not None for i in range(9, 15)):
        return unit

    return []