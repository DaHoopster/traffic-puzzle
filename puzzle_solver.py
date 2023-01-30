from typing import List

from enums import Color, Direction, Connector
from connection import Connection
from tile import Tile
from puzzle import Puzzle


def _tiles() -> List[Tile]:
  # init and return 28 tile pieces
  tile_pieces = []
  # checked
  tile_pieces.append(
    Tile(
      north=Connection(color=Color.BEIGE, direction=Direction.NORTH, connector=Connector.ROAD),
      east=Connection(color=Color.BEIGE, direction=Direction.EAST, connector=Connector.ROAD),
      south=Connection(color=Color.BEIGE, direction=Direction.SOUTH, connector=Connector.ROAD),
      west=Connection(color=Color.BEIGE, direction=Direction.WEST, connector=Connector.ROAD)
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=Connection(color=Color.BEIGE, direction=Direction.NORTH, connector=Connector.ROAD),
      east=None,
      south=None,
      west=Connection(color=Color.BLUE, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=Connection(color=Color.GREEN, direction=Direction.NORTH, connector=Connector.HEAD),
      east=Connection(color=Color.YELLOW, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=Connection(color=Color.BEIGE, direction=Direction.WEST, connector=Connector.ROAD)
    )
  )

  tile_pieces.append(
    Tile(
      north=None,
      east=None,
      south=Connection(color=Color.BEIGE, direction=Direction.SOUTH, connector=Connector.ROAD),
      west=Connection(color=Color.ORANGE, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )

  tile_pieces.append(
    Tile(
      north=Connection(color=Color.BEIGE, direction=Direction.NORTH, connector=Connector.ROAD),
      east=None,
      south=None,
      west=Connection(color=Color.BLUE, direction=Direction.WEST, connector=Connector.HEAD)
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=Connection(color=Color.BEIGE, direction=Direction.NORTH, connector=Connector.ROAD),
      east=Connection(color=Color.ORANGE, direction=Direction.EAST, connector=Connector.HEAD),
      south=Connection(color=Color.GREEN, direction=Direction.SOUTH, connector=Connector.TAIL),
      west=None
    )
  )
  # dupe piece - 1
  tile_pieces.append(
    Tile(
      north=Connection(color=Color.BEIGE, direction=Direction.NORTH, connector=Connector.ROAD),
      east=None,
      south=None,
      west=Connection(color=Color.YELLOW, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )
  # dupe piece - 2
  tile_pieces.append(
    Tile(
      north=Connection(color=Color.BEIGE, direction=Direction.NORTH, connector=Connector.ROAD),
      east=None,
      south=None,
      west=Connection(color=Color.YELLOW, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )

  # checked
  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.BLUE, direction=Direction.EAST, connector=Connector.HEAD),
      south=Connection(color=Color.BEIGE, direction=Direction.SOUTH, connector=Connector.ROAD),
      west=Connection(color=Color.BLUE, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )

  tile_pieces.append(
    Tile(
      north=Connection(color=Color.BEIGE, direction=Direction.NORTH, connector=Connector.ROAD),
      east=Connection(color=Color.PURPLE, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=None
    )
  )

  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.RED, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=Connection(color=Color.ORANGE, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )

  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.RED, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=Connection(color=Color.PURPLE, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )

  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.YELLOW, direction=Direction.EAST, connector=Connector.TAIL),
      south=None,
      west=Connection(color=Color.RED, direction=Direction.WEST, connector=Connector.HEAD)
    )
  )

  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.ORANGE, direction=Direction.WEST, connector=Connector.HEAD),
      south=None,
      west=Connection(color=Color.PURPLE, direction=Direction.WEST, connector=Connector.TAIL),
    )
  )

  tile_pieces.append(
    Tile(
      north=None,
      east=None,
      south=Connection(color=Color.GREEN, direction=Direction.SOUTH, connector=Connector.HEAD),
      west=Connection(color=Color.RED, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )

  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.PURPLE, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=Connection(color=Color.RED, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.YELLOW, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=Connection(color=Color.BLUE, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.BLUE, direction=Direction.EAST, connector=Connector.TAIL),
      south=None,
      west=Connection(color=Color.ORANGE, direction=Direction.WEST, connector=Connector.HEAD)
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=Connection(color=Color.GREEN, direction=Direction.NORTH, connector=Connector.TAIL),
      east=Connection(color=Color.BLUE, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=None
    )
  )

  tile_pieces.append(
    Tile(
      north=None,
      east=None,
      south=Connection(color=Color.GREEN, direction=Direction.SOUTH, connector=Connector.TAIL),
      west=Connection(color=Color.PURPLE, direction=Direction.WEST, connector=Connector.HEAD)
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=Connection(color=Color.GREEN, direction=Direction.NORTH, connector=Connector.HEAD),
      east=Connection(color=Color.ORANGE, direction=Direction.EAST, connector=Connector.TAIL),
      south=None,
      west=None
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.BLUE, direction=Direction.EAST, connector=Connector.HEAD),
      south=Connection(color=Color.GREEN, direction=Direction.SOUTH, connector=Connector.TAIL),
      west=None
    )
  )

  tile_pieces.append(
    Tile(
      north=Connection(color=Color.GREEN, direction=Direction.NORTH, connector=Connector.HEAD),
      east=Connection(color=Color.RED, direction=Direction.EAST, connector=Connector.TAIL),
      south=None,
      west=None
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.PURPLE, direction=Direction.EAST, connector=Connector.TAIL),
      south=None,
      west=Connection(color=Color.YELLOW, direction=Direction.WEST, connector=Connector.HEAD)
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.YELLOW, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=Connection(color=Color.PURPLE, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )

  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.ORANGE, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=Connection(color=Color.ORANGE, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )
  # checked
  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.PURPLE, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=Connection(color=Color.YELLOW, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )

  tile_pieces.append(
    Tile(
      north=None,
      east=Connection(color=Color.RED, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=Connection(color=Color.RED, direction=Direction.WEST, connector=Connector.TAIL)
    )
  )

  return tile_pieces


def run():
  puzzle = Puzzle()
  for tile in _tiles():
    puzzle.add_tile(tile=tile)

  puzzle.solve(export_board=True, allow_rotation=True)


if __name__ == '__main__':
  run()
