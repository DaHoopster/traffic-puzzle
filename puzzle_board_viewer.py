from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

from enums import Color, Direction, Connector
from connection import Connection
from tile import Tile

TILE_SIZE_HALF_UNIT = 5
TILE_SIZE_UNIT = 10
TILE_SIZE = TILE_SIZE_UNIT * 4
IMAGE_BACKGROUND = 'whitesmoke'
VISUAL_COLORS = ['black', 'mediumblue', 'gold', 'lime', 'crimson', 'darkorange', 'darkviolet', 'khaki']
VISUAL_CONNECTORS = ['', 'H', 'T', '']
FONT = ImageFont.truetype(font='SFNSMono.ttf', size=10)
COORD_FONT = ImageFont.truetype(font='SFNSMono.ttf', size=8)


def _draw_connector(drawing: ImageDraw, rect_points: List[Tuple[int, int]], rect_fill: str, connector_text_point: Tuple[int, int], connector_text: str) -> None:
  drawing.rectangle(rect_points, fill=rect_fill)
  drawing.text(connector_text_point, connector_text, fill=VISUAL_COLORS[0], font=FONT)


def _draw_tile(top_left: Tuple[int, int], tile: Tile, drawing: ImageDraw, coord: Tuple[int, int]) -> None:
  xy = [
    top_left,
    (top_left[0] + TILE_SIZE, top_left[1] + TILE_SIZE)
  ]
  # draw the tile rectangle
  drawing.rectangle(xy, fill=IMAGE_BACKGROUND, outline=VISUAL_COLORS[0])
  # draw coord
  drawing.text(top_left, coord.__str__(), fill=VISUAL_COLORS[0], font=COORD_FONT)
  # draw connections
  connection_rect_top_left = None
  connection_rect_bottom_right = None
  connection_rect_fill = ''
  connector_text_x = 0
  connector_text_y = 0
  connector_text = ''

  north_connection = tile.north
  if north_connection is not None:
    connection_rect_top_left = (top_left[0] + TILE_SIZE_UNIT, top_left[1])
    connection_rect_bottom_right = (top_left[0] + TILE_SIZE_UNIT * 3, top_left[1] + TILE_SIZE_UNIT)
    connection_rect_fill = VISUAL_COLORS[north_connection.color.value]
    (connector_text_x, connector_text_y) = (connection_rect_top_left[0], connection_rect_top_left[1])
    connector_text = VISUAL_CONNECTORS[north_connection.connector.value]

    _draw_connector(
      drawing=drawing,
      rect_points=[connection_rect_top_left, connection_rect_bottom_right],
      rect_fill=connection_rect_fill,
      connector_text_point=(connector_text_x, connector_text_y),
      connector_text=connector_text
    )

  east_connection = tile.east
  if east_connection is not None:
    connection_rect_top_left = (top_left[0] + TILE_SIZE_UNIT * 3, top_left[1] + TILE_SIZE_UNIT)
    connection_rect_bottom_right = (top_left[0] + TILE_SIZE, top_left[1] + TILE_SIZE_UNIT * 3)
    connection_rect_fill = VISUAL_COLORS[east_connection.color.value]
    (connector_text_x, connector_text_y) = (connection_rect_top_left[0], connection_rect_top_left[1])
    connector_text = VISUAL_CONNECTORS[east_connection.connector.value]

    _draw_connector(
      drawing=drawing,
      rect_points=[connection_rect_top_left, connection_rect_bottom_right],
      rect_fill=connection_rect_fill,
      connector_text_point=(connector_text_x, connector_text_y),
      connector_text=connector_text
    )

  south_connection = tile.south
  if south_connection is not None:
    connection_rect_top_left = (top_left[0] + TILE_SIZE_UNIT, top_left[1] + TILE_SIZE_UNIT * 3)
    connection_rect_bottom_right = (top_left[0] + TILE_SIZE_UNIT * 3, top_left[1] + TILE_SIZE)
    connection_rect_fill = VISUAL_COLORS[south_connection.color.value]
    (connector_text_x, connector_text_y) = (connection_rect_top_left[0], connection_rect_top_left[1])
    connector_text = VISUAL_CONNECTORS[south_connection.connector.value]

    _draw_connector(
      drawing=drawing,
      rect_points=[connection_rect_top_left, connection_rect_bottom_right],
      rect_fill=connection_rect_fill,
      connector_text_point=(connector_text_x, connector_text_y),
      connector_text=connector_text
    )

  west_connection = tile.west
  if west_connection is not None:
    connection_rect_top_left = (top_left[0], top_left[1] + TILE_SIZE_UNIT)
    connection_rect_bottom_right = (top_left[0] + TILE_SIZE_UNIT, top_left[1] + TILE_SIZE_UNIT * 3)
    connection_rect_fill = VISUAL_COLORS[west_connection.color.value]
    (connector_text_x, connector_text_y) = (connection_rect_top_left[0], connection_rect_top_left[1])
    connector_text = VISUAL_CONNECTORS[west_connection.connector.value]

    _draw_connector(
      drawing=drawing,
      rect_points=[connection_rect_top_left, connection_rect_bottom_right],
      rect_fill=connection_rect_fill,
      connector_text_point=(connector_text_x, connector_text_y),
      connector_text=connector_text
    )


def view_board(board: List[List[Tile]], output_file: str = None) -> None:
  board_image = Image.new(
    mode='RGB',
    size=(len(board) * TILE_SIZE, len(board[0]) * TILE_SIZE),
    color=IMAGE_BACKGROUND
  )
  drawing = ImageDraw.Draw(board_image)
  # (0, 0) is the top left corner of the image
  for row_idx, row in enumerate(board):
    vertical_start = TILE_SIZE * row_idx
    for tile_idx, tile in enumerate(row):
      if tile is not None:
        horizontal_start = TILE_SIZE * tile_idx
        _draw_tile(top_left=(horizontal_start, vertical_start), tile=tile, drawing=drawing, coord=(row_idx, tile_idx))

  if output_file is None:
    board_image.show()
  else:
    board_image.save(output_file, compression_level=5)


if __name__ == '__main__':
  tile_1 = Tile(
    north=None,
    east=Connection(color=Color.RED, direction=Direction.EAST, connector=Connector.TAIL),
    south=None,
    west=Connection(color=Color.PURPLE, direction=Direction.WEST, connector=Connector.HEAD)
  )

  tile_2 = Tile(
    north=None,
    east=None,
    south=Connection(color=Color.GREEN, direction=Direction.SOUTH, connector=Connector.TAIL),
    west=Connection(color=Color.PURPLE, direction=Direction.WEST, connector=Connector.HEAD)
  )

  tile_3 = Tile(
    north=None,
    east=Connection(color=Color.PURPLE, direction=Direction.EAST, connector=Connector.TAIL),
    south=None,
    west=Connection(color=Color.YELLOW, direction=Direction.WEST, connector=Connector.HEAD)
  )

  tile_4 = Tile(
    north=None,
    east=Connection(color=Color.BEIGE, direction=Direction.EAST, connector=Connector.ROAD),
    south=Connection(color=Color.GREEN, direction=Direction.SOUTH, connector=Connector.HEAD),
    west=Connection(color=Color.RED, direction=Direction.WEST, connector=Connector.HEAD)
  )

  view_board(board=[[tile_1, tile_2], [tile_3, tile_4]])
