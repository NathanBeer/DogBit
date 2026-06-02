from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def get_path(start_pos, end_pos):
    matrix = [[1 for _ in range(10)] for _ in range(10)]
    grid = Grid(matrix=matrix)
    start = grid.node(start_pos[0], start_pos[1])
    end = grid.node(end_pos[0], end_pos[1])
    finder = AStarFinder()
    path, _ = finder.find_path(start, end, grid)
    return path