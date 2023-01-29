from __future__ import annotations

from typing import Dict, List, Set, Tuple
import copy
import random
from pathlib import Path

from enums import Color, Direction, Connector
from connection import Connection
from tile import Tile

from puzzle_board_viewer import view_board


class Puzzle:
  class Move:
    def __init__(self, tile: Tile, rotation_count: int, coord: Tuple[int, int]):
      self._tile = tile
      self._rotation_count = rotation_count
      self._coord = coord

    @property
    def tile(self) -> Tile:
      return self._tile

    @property
    def rotation_count(self) -> int:
      return self._rotation_count

    @property
    def coord(self) -> Tuple[int, int]:
      return self._coord

    def __repr__(self):
      return f"{self._tile.__repr__()} 🌀 {self.rotation_count} @ {self.coord}"

    def __eq__(self, other: Puzzle.Move) -> bool:
      return self.tile == other.tile and self.rotation_count == other.rotation_count and self.coord == other.coord

    def __hash__(self):
      return hash((self.tile, self.rotation_count, self.coord))

  # NOTE: needs to model the coordinates of the Tile
  # NOTE: to correctly place a tile with multiple connections, e.g.
  #       need to track the coordinates of placed tiles (X) in order
  #       to calculate if O can be placed!
  #
  #          X O
  #          X X
  #

  FIRST_TILE_COORD = (20, 20)

  ROAD_ROAD_SCORE = 5
  HEAD_TAIL_SCORE = 3
  NONE_NONE_SCORE = 1

  @classmethod
  def neighboring_coords(cls, coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    coord_row = coord[0]
    coord_col = coord[1]

    # potential empty coords surrounding the tile in the placed coord
    north_coord = (coord_row - 1, coord_col)
    east_coord = (coord_row, coord_col + 1)
    south_coord = (coord_row + 1, coord_col)
    west_coord = (coord_row, coord_col - 1)

    return [north_coord, east_coord, south_coord, west_coord]

  def __init__(self, tiles: List[Tile] = None, placed: Dict[str, Tuple[int, int]] = None, board: List[List[Tile]] = None, filled_coords: Set[Tuple[int, int]] = None, allowed_coords: Set[Tuple[int, int]] = None):
    # tile repr: tile obj
    self._tiles = tiles or []
    self._tiles_index = {tile.__repr__(): tile for tile in tiles} if self._tiles else {}
    self._placed = placed or {}
    # board is 40 x 40
    self._board = board or [[None for _ in range(0, 41)] for _ in range(0, 41)]
    self._filled_coords = filled_coords or set()
    self._allowed_coords = allowed_coords or set()

  @property
  def tiles(self) -> List[Tile]:
    return self._tiles

  @property
  def placed_tiles(self) -> Dict[str, Tuple[int, int]]:
    return self._placed

  @property
  def board(self) -> List[List[Tile]]:
    return self._board

  @property
  def occupied_coords(self) -> Set[Tuple[int, int]]:
    return self._filled_coords

  @property
  def allowed_coords(self) -> Set[Tuple[int, int]]:
    return self._allowed_coords

  def _connection_score(self, connection_1: Connection, connection_2: Connection) -> int:
    if connection_1 is None or \
      connection_2 is None or \
      (connection_1.connector is None and connection_2.connector is None):
      return Puzzle.NONE_NONE_SCORE

    if connection_1.connector.value + connection_2.connector.value == 3:
      return Puzzle.HEAD_TAIL_SCORE

    if connection_1.connector == Connector.ROAD and connection_2.connector == Connector.ROAD:
      return Puzzle.ROAD_ROAD_SCORE

  def _update_allowed_coords(self, tile: Tile, coord: Tuple[int, int]) -> None:
    # potential empty coords surrounding the tile in the placed coord
    [north_coord, east_coord, south_coord, west_coord] = Puzzle.neighboring_coords(coord=coord)
    # check if all 4 potential coords are filled or still open
    if north_coord not in self._filled_coords and self.board_content(coord=north_coord) is None:
      self._allowed_coords.add(north_coord)

    if east_coord not in self._filled_coords and self.board_content(coord=east_coord) is None:
      self._allowed_coords.add(east_coord)

    if south_coord not in self._filled_coords and self.board_content(coord=south_coord) is None:
      self._allowed_coords.add(south_coord)

    if west_coord not in self._filled_coords and self.board_content(coord=west_coord) is None:
      self._allowed_coords.add(west_coord)

  def _place_first_tile(self, tile: Tile = None) -> None:
    first_tile = tile
    if first_tile is None:
      first_tile_idx = random.randrange(0, len(self._tiles), 1)
      first_tile = self._tiles[first_tile_idx]

    self._board[Puzzle.FIRST_TILE_COORD[0]][Puzzle.FIRST_TILE_COORD[1]] = first_tile
    self._placed[first_tile.__repr__()] = Puzzle.FIRST_TILE_COORD
    self._filled_coords.add(Puzzle.FIRST_TILE_COORD)
    self._update_allowed_coords(tile=first_tile, coord=Puzzle.FIRST_TILE_COORD)

  def add_tile(self, tile: Tile) -> None:
    self._tiles.append(tile)

  def board_content(self, coord: Tuple[int, int]) -> Tile:
    return self._board[coord[0]][coord[1]]

  def reset(self) -> None:
    self._placed.clear()
    # board is 40 x 40
    self._board = [[None for _ in range(0, 41)] for _ in range(0, 41)]
    self._filled_coords.clear()
    self._allowed_coords = {Puzzle.FIRST_TILE_COORD}

  def print_board(self) -> None:
    for row_idx, row in enumerate(self.board):
      row_content = []
      for item_idx, item in enumerate(row):
        if item is None:
          row_content.append('.')
        else:
          row_content.append('X')

      print(''.join(row_content))

    print(self.placed_tiles)

  def can_place_tile(self, tile: Tile, coord: Tuple[int, int]) -> Tuple[bool, int]:
    # check if the tile can be placed by ALL connections
    [north_coord, east_coord, south_coord, west_coord] = Puzzle.neighboring_coords(coord=coord)
    [north_score, east_score, south_score, west_score] = [0, 0, 0, 0]

    north_neighbor = self.board_content(coord=north_coord)
    can_connect_north = north_neighbor is None or north_neighbor.can_connect(self_edge=north_neighbor.south, tile=tile, tile_edge=tile.north)
    if can_connect_north:
      north_score = self._connection_score(connection_1=None if north_neighbor is None else north_neighbor.south, connection_2=tile.north)

    east_neighbor = self.board_content(coord=east_coord)
    can_connect_east = east_neighbor is None or east_neighbor.can_connect(self_edge=east_neighbor.west, tile=tile, tile_edge=tile.east)
    if can_connect_east:
      east_score = self._connection_score(connection_1=None if east_neighbor is None else east_neighbor.west, connection_2=tile.east)

    south_neighbor = self.board_content(coord=south_coord)
    can_connect_south = south_neighbor is None or south_neighbor.can_connect(self_edge=south_neighbor.north, tile=tile, tile_edge=tile.south)
    if can_connect_south:
      south_score = self._connection_score(connection_1=None if south_neighbor is None else south_neighbor.north, connection_2=tile.south)

    west_neighbor = self.board_content(coord=west_coord)
    can_connect_west = west_neighbor is None or west_neighbor.can_connect(self_edge=west_neighbor.east, tile=tile, tile_edge=tile.west)
    if can_connect_west:
      west_score = self._connection_score(connection_1=None if west_neighbor is None else west_neighbor.east, connection_2=tile.west)

    return (
      can_connect_north and can_connect_east and can_connect_south and can_connect_west,
      north_score * east_score * south_score * west_score,
    )

  def place_tile(self, tile: Tile, rotation_count: int, coord: Tuple[int, int]) -> bool:
    # make sure coord is one of the allowed moves
    coord_row = coord[0]
    coord_col = coord[1]

    if coord not in self._allowed_coords:
      print(f"cannot place tile at coordinate {coord}")
      return False
    elif coord in self._filled_coords:
      print(f"coordinate {coord} is already occupied")
      return False
    else:
      # the below assert should not fail if board and other indices are kept in sync
      assert self._board[coord_row][coord_col] is None
      # make sure the tile is in the right orientation
      tile.reset()
      for _ in range(0, rotation_count):
        tile.rotate()
      # check if the tile can be placed
      if self.can_place_tile(tile=tile, coord=coord)[0] is True:
        # update board
        self._board[coord_row][coord_col] = tile
        self._placed[tile.__repr__()] = coord
        # update indices
        if coord in self._allowed_coords:
          self._allowed_coords.remove(coord)

        self._filled_coords.add(coord)
        self._update_allowed_coords(tile=tile, coord=coord)

        return True

  def next_moves(self, allow_rotation: bool = False) -> Tuple[int, List[Move]]:
    tiles_remaining = len(self.tiles) - len(self.placed_tiles)
    print(f"🦀 remaining tiles {tiles_remaining}, allowed coords {len(self.allowed_coords)}")
    # successfully completed
    if tiles_remaining == 0:
      print(f"🏅 success! - {tiles_remaining}")
      return (-1, [])
    elif len(self.allowed_coords) == 0:
      print(f"👻 no more moves possible - {tiles_remaining}")
      return (-2, [])
    else:
      allowed_coords_copy = self.allowed_coords.copy()
      placed_copy = self.placed_tiles.copy()
      max_score_all_possible_coords = 0
      coord_scores = {}
      moves = []

      for possible_coord in allowed_coords_copy:
        # a list of tuple (tile, rotation_count)
        max_scoring_tiles: List[Tuple[Tile, int]] = []
        max_score = 0

        for tile in self.tiles:
          if tile.__repr__() not in placed_copy:
            spins = [0, 1, 2, 3] if allow_rotation else [0]
            for spin in spins:
              tile.reset()

              for _ in '.' * spin:
                tile.rotate()

              (possible, score) = self.can_place_tile(tile=tile, coord=possible_coord)
              if possible:
                if score == max_score:
                  max_scoring_tiles.append((tile, tile.rotation_count))
                elif score > max_score:
                  max_score = score
                  max_scoring_tiles = [(tile, tile.rotation_count)]

        print(f"📝 For coord {possible_coord}, max score: {max_score}. max scoring tiles: {max_scoring_tiles}")
        if max_score > max_score_all_possible_coords:
          # replace the score and moves
          max_score_all_possible_coords = max_score
          moves.clear()

          for max_scoring_tile, tile_rotation_count in max_scoring_tiles:
            # add to moves
            attempting_move = Puzzle.Move(tile=max_scoring_tile, rotation_count=tile_rotation_count, coord=possible_coord)
            moves.append(attempting_move)
        elif max_score == max_score_all_possible_coords:
          for max_scoring_tile, tile_rotation_count in max_scoring_tiles:
            # add to moves
            attempting_move = Puzzle.Move(tile=max_scoring_tile, rotation_count=tile_rotation_count, coord=possible_coord)
            moves.append(attempting_move)
        # debugging purposes
        coord_scores[possible_coord] = max_score

        if len(max_scoring_tiles) == 0:
          # no tiles can fit
          self.allowed_coords.remove(possible_coord)
          print(f"💀 dead coord {possible_coord}")

      return (max_score_all_possible_coords, moves)

  def solve(self, export_board: bool = False, allow_rotation: bool = False) -> None:
    solved_puzzles = []

    # place each tile as first
    for first_tile_idx, first_tile in enumerate(self._tiles):
      worker_puzzle = Puzzle(board=self.board, tiles=self.tiles)
      worker_puzzle.reset()
      puzzle_moves = [(1, [Puzzle.Move(tile=first_tile, rotation_count=0, coord=Puzzle.FIRST_TILE_COORD)])]
      max_move_score = 1
      has_more_moves = True

      while has_more_moves:
        next_puzzle_moves = []
        for (_, moves) in puzzle_moves:
          for move in moves:
            tile_in_move = move.tile
            rotation_count_in_move = move.rotation_count
            coord_in_move = move.coord

            if worker_puzzle.place_tile(tile=tile_in_move, rotation_count=rotation_count_in_move, coord=coord_in_move):
              # first made move wins
              print(f"  💋 Move made: {move}")

              next_possible_moves = (nm_score, _) = worker_puzzle.next_moves(allow_rotation=allow_rotation)

              if nm_score == -1:
                solved_puzzles.append(worker_puzzle)
                print(f"👌 => first tile index: {first_tile_idx}")
                view_board(board=worker_puzzle.board, output_file=f"{Path.home()}/Downloads/traffic-puzzle-board/solution-{first_tile_idx}.png" if export_board is True else None)
              elif nm_score == max_move_score:
                next_puzzle_moves.append(next_possible_moves)
              elif nm_score > max_move_score:
                max_move_score = nm_score
                next_puzzle_moves = [next_possible_moves]

              break

        puzzle_moves = next_puzzle_moves
        max_move_score = 1
        has_more_moves = len(puzzle_moves) != 0

    print('✅')


if __name__ == '__main__':
  def tests():
    puzzle = Puzzle()
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

    tile_5 = Tile(
      north=Connection(color=Color.GREEN, direction=Direction.NORTH, connector=Connector.TAIL),
      east=None,
      south=Connection(color=Color.BEIGE, direction=Direction.SOUTH, connector=Connector.ROAD),
      west=Connection(color=Color.ORANGE, direction=Direction.WEST, connector=Connector.HEAD)
    )

    tile_6 = Tile(
      north=None,
      east=Connection(color=Color.ORANGE, direction=Direction.EAST, connector=Connector.TAIL),
      south=None,
      west=Connection(color=Color.RED, direction=Direction.WEST, connector=Connector.HEAD)
    )

    for t in [tile_1, tile_2, tile_3, tile_4, tile_5, tile_6]:
      puzzle.add_tile(tile=t)

    assert puzzle.can_place_tile(tile=tile_1, coord=(28, 28)) == (True, 1)
    assert puzzle.can_place_tile(tile=tile_2, coord=(28, 28)) == (True, 1)
    assert puzzle.can_place_tile(tile=tile_3, coord=(28, 28)) == (True, 1)
    # place tile_1 as first
    puzzle._place_first_tile(tile=tile_1)
    assert [c for c in puzzle.occupied_coords] == [(20, 20)]
    assert [c for c in puzzle.allowed_coords] == [(21, 20), (19, 20), (20, 19), (20, 21)]
    # test next_moves
    (puzzle, score, next_moves) = puzzle.next_moves()
    assert type(puzzle) == Puzzle
    assert score == 3
    assert len(next_moves) == 3
    # test _can_place_tile
    assert puzzle.can_place_tile(tile=tile_2, coord=(19, 20)) == (False, 0)
    assert puzzle.can_place_tile(tile=tile_2, coord=(20, 21)) == (False, 0)
    assert puzzle.can_place_tile(tile=tile_2, coord=(21, 20)) == (True, 1)  # None - None connections
    assert puzzle.can_place_tile(tile=tile_2, coord=(20, 19)) == (False, 0)

    assert puzzle.can_place_tile(tile=tile_3, coord=(19, 20)) == (True, 1)  # None - None connections
    assert puzzle.can_place_tile(tile=tile_3, coord=(20, 21)) == (False, 0)
    assert puzzle.can_place_tile(tile=tile_3, coord=(21, 20)) == (True, 1)  # None - None connections
    assert puzzle.can_place_tile(tile=tile_3, coord=(20, 19)) == (True, 3)  # head - tail on purple
    # test place_tile
    puzzle.place_tile(tile=tile_3, rotation_count=0, coord=(20, 19))
    assert [c for c in puzzle._allowed_coords] == [(21, 20), (21, 19), (19, 20), (19, 19), (20, 18), (20, 21)]

    puzzle.place_tile(tile=tile_4, rotation_count=0, coord=(20, 21))    
    assert [c for c in puzzle.allowed_coords] == [(21, 20), (21, 19), (19, 20), (19, 19), (21, 21), (20, 22), (20, 18), (19, 21)]

    puzzle.place_tile(tile=tile_5, rotation_count=0, coord=(21, 21))
    assert [c for c in puzzle.allowed_coords] == [(21, 20), (22, 21), (21, 19), (19, 20), (21, 22), (19, 19), (20, 22), (20, 18), (19, 21)]

    puzzle.place_tile(tile=tile_6, rotation_count=0, coord=(21, 20))
    assert [c for c in puzzle.allowed_coords] == [(22, 21), (21, 19), (19, 20), (22, 20), (21, 22), (19, 19), (20, 22), (20, 18), (19, 21)]

  def test_solve():
    puzzle = Puzzle()
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

    tile_5 = Tile(
      north=Connection(color=Color.GREEN, direction=Direction.NORTH, connector=Connector.TAIL),
      east=None,
      south=Connection(color=Color.BEIGE, direction=Direction.SOUTH, connector=Connector.ROAD),
      west=Connection(color=Color.ORANGE, direction=Direction.WEST, connector=Connector.HEAD)
    )

    tile_6 = Tile(
      north=None,
      east=Connection(color=Color.ORANGE, direction=Direction.EAST, connector=Connector.TAIL),
      south=None,
      west=Connection(color=Color.RED, direction=Direction.WEST, connector=Connector.HEAD)
    )

    for t in [tile_1, tile_2, tile_3, tile_4, tile_5, tile_6]:
      puzzle.add_tile(tile=t)

    puzzle.solve()

  def test_solve_with_rotation():
    tile_1 = Tile(
      north=Connection(color=Color.BEIGE, direction=Direction.NORTH, connector=Connector.ROAD),
      east=None,
      south=None,
      west=Connection(color=Color.YELLOW, direction=Direction.WEST, connector=Connector.TAIL)
    )

    tile_2 = Tile(
      north=Connection(color=Color.BEIGE, direction=Direction.NORTH, connector=Connector.ROAD),
      east=Connection(color=Color.PURPLE, direction=Direction.EAST, connector=Connector.HEAD),
      south=None,
      west=None
    )

    tile_3 = Tile(
      north=None,
      east=Connection(color=Color.PURPLE, direction=Direction.EAST, connector=Connector.TAIL),
      south=None,
      west=Connection(color=Color.YELLOW, direction=Direction.WEST, connector=Connector.HEAD)
    )

    puzzle = Puzzle()
    for t in [tile_1, tile_2, tile_3]:
      puzzle.add_tile(tile=t)

    puzzle._place_first_tile(tile=tile_1)
    max_score_next_moves, moves = puzzle.next_moves(allow_rotation=True)
    assert max_score_next_moves == 5
    assert len(moves) == 1

    next_move = moves[0]
    assert next_move.rotation_count == 2
    assert next_move.tile.__repr__() == 'Tile [BEIGE ROAD @ NORTH,PURPLE HEAD @ EAST,None,None]'
    assert puzzle.place_tile(tile=next_move.tile, rotation_count=next_move.rotation_count, coord=next_move.coord) is True

    placed_tile = puzzle.board[19][20]
    assert placed_tile.__repr__() == 'Tile [BEIGE ROAD @ NORTH,PURPLE HEAD @ EAST,None,None]'
    assert placed_tile.rotation_count == 2
    assert placed_tile.__str__() == 'Tile<🌀2> [None, None, BEIGE ROAD @ SOUTH, PURPLE HEAD @ WEST]'

    # run solve with rotation
    puzzle.reset()
    puzzle.solve(allow_rotation=True)

  test_solve_with_rotation()
