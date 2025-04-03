# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers

from .core import CellState, Coord, Direction, MoveAction
from .utils import render_board
from collections import deque

BOARD_N = 8

# recursively finds all jump moves starting from a certain coord and appends them to moves
def generate_jump_moves(coord: Coord, board: dict[Coord, CellState], visited: set[Coord], 
        path: list[Direction], start_coord: Coord, moves: list[(MoveAction, Coord)]):
    if coord in visited:
        return
    
    visited.add(coord)
    directions = [Direction.Down, Direction.DownLeft, Direction.DownRight, Direction.Left, Direction.Right]

    for direc in directions:
        try:
            next_square = coord + direc
            next_next_square = next_square + direc
        except:
            continue

        if next_square not in board or next_next_square not in board:
            continue

        if board[next_square] == CellState.BLUE and board[next_next_square] == CellState.LILY_PAD \
            and next_next_square not in visited:
            
            new_path = path + [direc]
            moves.append((MoveAction(coord=start_coord, _directions=new_path), next_next_square))
            generate_jump_moves(next_next_square, board, visited, new_path, start_coord, moves)


def generate_moves(coord: Coord, board: dict[Coord, CellState]) -> list[(MoveAction, Coord)]:
    directions = [Direction.Down, Direction.DownLeft, Direction.DownRight, Direction.Left, Direction.Right]
    moves = []
    for direc in directions:
        try:
            next_square = coord + direc
        except:
            continue

        if next_square not in board:
            continue

        if board[next_square] == CellState.LILY_PAD:
            moves.append( (MoveAction(coord=coord, _directions=[direc]), next_square) )
    
    generate_jump_moves(coord, board, set(), list(), coord, moves)

    return moves

def search(
    board: dict[Coord, CellState]
) -> list[MoveAction] | None:

    start = None
    for coord in board:
        if board[coord] == CellState.RED:
            start = coord
            break

    q = deque([start])
    visited = {start,}
    previous = {start: None}
    final_coord = None

    while len(q) > 0:
        current_coord = q.popleft()

        if current_coord.r == BOARD_N-1:
            final_coord = current_coord
            break
        
        for move, dest in generate_moves(current_coord, board):
            if dest not in visited:
                q.append(dest)
                visited.add(dest)
                previous[dest] = (current_coord, move)
    
    print(render_board(board, ansi=True))

    if not final_coord:
        return None

    L = [final_coord]
    final_moves = []
    while previous[L[-1]] != None:
        prev_coord, move = previous[L[-1]]
        L.append(prev_coord)
        final_moves.append(move)
    
    return list(reversed(final_moves))




    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.

