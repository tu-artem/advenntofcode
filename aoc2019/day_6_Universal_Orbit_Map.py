from typing import NamedTuple, Optional

orbit_map = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""


class SpaceObject(NamedTuple):
    name: str
    orbits: Optional['SpaceObject']
