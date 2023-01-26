from enum import Enum


class Connector(Enum):
  HEAD = 1
  TAIL = 2
  ROAD = 3


class Color(Enum):
  BLUE = 1
  YELLOW = 2
  GREEN = 3
  RED = 4
  ORANGE = 5
  PURPLE = 6
  BEIGE = 7


class Direction(Enum):
  NORTH = 1
  EAST = 2
  SOUTH = 3
  WEST = 4
