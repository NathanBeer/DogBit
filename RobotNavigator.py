from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def get_path(start_pos, end_pos, obstacle_list=None):
    # 1. Create a map (1 = walkable, 0 = obstacle)
    # For now, let's make a simple 10x10 empty room
    matrix = [[1 for _ in range(10)] for _ in range(10)]
    
    # 2. Add obstacles (if YOLO sees a 'chair' or 'wall')
    if obstacle_list:
        for (obs_x, obs_y) in obstacle_list:
            matrix[obs_y][obs_x] = 0

    grid = Grid(matrix=matrix)
    
    start = grid.node(start_pos[0], start_pos[1])
    end = grid.node(end_pos[0], end_pos[1])

    # 3. Use A* (A-Star) algorithm to find the path
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)

    # Returns a list of coordinates: [(0,0), (1,1), (2,2)...]
    return path