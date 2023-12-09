from typing import List, Any


def read_input(day: int, part:int = 1) -> List[Any]:
    filename = f"day{day}_{part}.txt"

    with open(f"data/{filename}") as f:
        lines = f.readlines()

    return [line.strip() for line in lines]
