from __future__ import annotations
from enums import Connector, Color, Direction


class Connection:
  def __init__(self, connector: Connector, color: Color, direction: Direction):
    self._connector = connector
    self._color = color
    self._direction = direction

  @property
  def connector(self) -> Connector:
    return self._connector

  @property
  def color(self) -> Color:
    return self._color

  @property
  def direction(self) -> Direction:
    return self._direction

  def __eq__(self, other: Connection) -> bool:
    return self._connector.value == other.connector.value and \
      self._color.value == other.color.value and \
      self._direction.value == other.direction.value

  def __hash__(self):
    return hash((self._connector, self._color, self._direction))

  def __repr__(self) -> str:
    return f"{self.color.name} {self.connector.name} @ {self.direction.name}"

  def is_color_matching(self, conn: Connection) -> bool:
    return conn is not None and self.color == conn.color

  def is_direction_matching(self, conn: Connection) -> bool:
    return conn is not None and abs(self.direction.value - conn.direction.value) == 2

  def is_connector_matching(self, conn: Connection) -> bool:
    return conn is not None and (self.connector.value + conn.connector.value) % 3 == 0


# test
if __name__ == '__main__':
  conn_1 = Connection(connector=Connector.HEAD, color=Color.GREEN, direction=Direction.NORTH)
  conn_2 = Connection(connector=Connector.HEAD, color=Color.ORANGE, direction=Direction.SOUTH)
  conn_3 = Connection(connector=Connector.TAIL, color=Color.GREEN, direction=Direction.EAST)
  conn_4 = Connection(connector=Connector.ROAD, color=Color.BEIGE, direction=Direction.WEST)
  conn_5 = Connection(connector=Connector.ROAD, color=Color.BEIGE, direction=Direction.EAST)

  # test color matching
  assert conn_1.is_color_matching(conn=conn_2) is False
  assert conn_1.is_color_matching(conn=conn_3) is True
  # test connector matching
  assert conn_1.is_connector_matching(conn=conn_4) is False
  assert conn_1.is_connector_matching(conn=conn_2) is False
  assert conn_1.is_connector_matching(conn=conn_3) is True
  # test direction matching
  assert conn_1.is_direction_matching(conn=conn_2) is True
  assert conn_1.is_direction_matching(conn=conn_3) is False
  assert conn_1.is_direction_matching(conn=conn_4) is False
  assert conn_3.is_direction_matching(conn=conn_5) is False
  # show string representation
  print(conn_1)
