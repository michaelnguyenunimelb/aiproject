# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers

from .core import CellState, Coord, Direction, MoveAction
from .utils import render_board
from collections import deque


def generate_jump_moves(coord: Coord, board: dict[Coord, CellState], moves):
    directions = [Direction.Down, Direction.DownLeft, Direction.DownRight, Direction.Left, Direction.Right]

    for direc in directions:
        next_square = coord + direc
        next_next_square = next_square + direc
        
        # if abs(next_square.c - coord.c) > 1 or next_square not in board:
        #     continue
        # if abs(next_next_square.c - next_square.c) > 1 or \
        #     abs(next_next_square.r - next_square.r) > 1 or \
        #     next_next_square not in board:
        #     continue

        if next_square not in board or next_next_square not in board:
            continue

        if board[next_square] == CellState.BLUE and board[next_next_square] == CellState.LILY_PAD:
            if MoveAction(coord, ) not in moves:
                moves.append(MoveAction(coord, new))

                generate_jump_moves(next_next_square, board, moves)


def generate_moves(coord: Coord, board: dict[Coord, CellState]):
    directions = [Direction.Down, Direction.DownLeft, Direction.DownRight, Direction.Left, Direction.Right]
    moves = []
    for direc in directions:
        next_square = coord + direc
        if abs(next_square.c - coord.c) > 1 or next_square not in board:
            continue

        if board[next_square] == CellState.LILY_PAD:
            moves.append(MoveAction(coord, direc))
    
    generate_jump_moves(coord, board, moves)

    return moves

def search(
    board: dict[Coord, CellState]
) -> list[MoveAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `CellState` instances which can be one of
            `CellState.RED`, `CellState.BLUE`, or `CellState.LILY_PAD`.
    
    Returns:
        A list of "move actions" as MoveAction instances, or `None` if no
        solution is possible.
    """
    start = None
    for coord in board:
        if board[coord] == CellState.RED:
            start = coord
            break

    q = deque([start])
    visited = {start,}
    dist = {start: 0}
    previous = {start: None}
    final_coord = None

    while len(q) > 0:
        current_coord = q.popleft()
        board_copy = board.copy()
        del board_copy[start]
        board_copy[current_coord] = CellState.RED
        # print(render_board(board_copy, ansi=True))
        # print(dist[current_coord])


        if current_coord.r == 7:
            final_coord = current_coord
            break
        
        for move in generate_moves(current_coord, board):
            next_square = current_coord + move._directions
            if next_square not in visited:
                q.append(next_square)
                visited.add(next_square)
                dist[next_square] = dist[current_coord] + 1
                previous[next_square] = current_coord
        
    L = [final_coord]
    while previous[L[-1]] != None:
        L.append(previous[L[-1]])

    for current_coord in L[::-1]:
        board_copy = board.copy()
        del board_copy[start]
        board_copy[current_coord] = CellState.RED
        print(render_board(board_copy, ansi=True))
        print(dist[current_coord])

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, ansi=True))

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    
    
    
    return [
        MoveAction(Coord(0, 5), [Direction.Down]),
        MoveAction(Coord(1, 5), [Direction.DownLeft]),
        MoveAction(Coord(3, 3), [Direction.Left]),
        MoveAction(Coord(3, 2), [Direction.Down, Direction.Right]),
        MoveAction(Coord(5, 4), [Direction.Down]),
        MoveAction(Coord(6, 4), [Direction.Down]),
    ]
