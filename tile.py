from __future__ import annotations

from typing import Tuple
import copy
from enums import Color, Connector, Direction
from connection import Connection


class Tile:
  def __init__(self, north: Connection, east: Connection, south: Connection, west: Connection):
    self._north = north
    self._east = east
    self._south = south
    self._west = west
    self._rotation_count = 0
    self._original_orientation = (copy.deepcopy(self._north), copy.deepcopy(self._east), copy.deepcopy(self._south), copy.deepcopy(self._west))

  @property
  def north(self) -> Connection:
    return self._north

  @property
  def east(self) -> Connection:
    return self._east

  @property
  def south(self) -> Connection:
    return self._south

  @property
  def west(self) -> Connection:
    return self._west

  @property
  def original_orientation(self) -> Tuple[Connection, Connection, Connection, Connection]:
    return self._original_orientation

  @property
  def rotation_count(self) -> int:
    return self._rotation_count

  def __eq__(self, other: Tile) -> bool:
    return self._north.__eq__(other.north) and \
      self._east.__eq__(other.east) and \
      self._south.__eq__(other.south) and \
      self._west.__eq__(other.west)

  def __hash__(self):
    return hash((self._north, self._east, self._south, self._west))

  def __repr__(self) -> str:
    return f"Tile [{self._north.__repr__()},{self._east.__repr__()},{self._south.__repr__()},{self._west.__repr__()}]"

  def can_connect(self, self_edge: Connection, tile: Tile, tile_edge: Connection) -> bool:
    return self_edge is not None and \
      self_edge.is_color_matching(conn=tile_edge) and \
      self_edge.is_connector_matching(conn=tile_edge) and \
      self_edge.is_direction_matching(conn=tile_edge) or (self_edge is None and tile_edge is None)

  def rotate(self) -> None:
    # rotate 90 degrees clockwise each time
    temp_east = self.east
    if self._north is not None:
      self._north.rotate()
    self._east = self._north

    temp_south = self.south
    if temp_east is not None:
      temp_east.rotate()
    self._south = temp_east

    temp_west = self.west
    if temp_south is not None:
      temp_south.rotate()
    self._west = temp_south

    if temp_west is not None:
      temp_west.rotate()
    self._north = temp_west


if __name__ == '__main__':
  tile_1 = Tile(
    north=Connection(color=Color.GREEN, connector=Connector.HEAD, direction=Direction.NORTH),
    east=Connection(color=Color.ORANGE, connector=Connector.TAIL, direction=Direction.EAST),
    south=None,
    west=None
  )

  tile_2 = Tile(
    north=Connection(color=Color.GREEN, connector=Connector.HEAD, direction=Direction.NORTH),
    east=Connection(color=Color.ORANGE, connector=Connector.TAIL, direction=Direction.EAST),
    south=None,
    west=None
  )

  tile_3 = Tile(
    north=None,
    east=Connection(color=Color.ORANGE, connector=Connector.HEAD, direction=Direction.EAST),
    south=Connection(color=Color.GREEN, connector=Connector.TAIL, direction=Direction.SOUTH),
    west=None
  )

  print(tile_1)
  # check for equality
  assert tile_1 == tile_2
  # check for can_connect
  assert tile_1.can_connect(self_edge=tile_1.north, tile=tile_2, tile_edge=tile_2.north) is False
  assert tile_1.can_connect(self_edge=tile_1.north, tile=tile_2, tile_edge=tile_2.south) is False
  assert tile_1.can_connect(self_edge=tile_1.north, tile=tile_3, tile_edge=tile_3.south) is True
  assert tile_1.can_connect(self_edge=tile_1.north, tile=tile_3, tile_edge=tile_3.north) is False
  assert tile_1.can_connect(self_edge=tile_1.north, tile=tile_3, tile_edge=tile_3.east) is False
  assert tile_1.can_connect(self_edge=tile_1.north, tile=tile_3, tile_edge=tile_3.west) is False
  assert tile_2.can_connect(self_edge=tile_2.south, tile=tile_3, tile_edge=tile_3.north) is True
  # check for rotate
  tile_1.rotate()
  assert tile_1.north is None
  assert tile_1.east.direction == Direction.EAST
  assert tile_1.east.color == Color.GREEN
  assert tile_1.east.connector == Connector.HEAD
  assert tile_1.south.direction == Direction.SOUTH
  assert tile_1.south.color == Color.ORANGE
  assert tile_1.south.connector == Connector.TAIL
  assert tile_1.west is None
  # check for original state
  assert tile_1.original_orientation[0].color == Color.GREEN
  assert tile_1.original_orientation[0].connector == Connector.HEAD
  assert tile_1.original_orientation[0].direction == Direction.NORTH
