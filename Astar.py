from queue import PriorityQueue

def aStar(maze_matrix, start, goals):
    def h(cell, goals):
        # Calculate the Manhattan distance to the nearest goal
        return min(abs(cell[0] - goal[0]) + abs(cell[1] - goal[1]) for goal in goals)

    def get_cells(matrix):
        return {(i, j) for i, row in enumerate(matrix) for j, cell in enumerate(row)}

    def get_neighbors(cell, matrix):
        i, j = cell
        neighbors = []

        for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y] != 1:
                neighbors.append((x, y))

        return neighbors

    start = tuple(start[0])  # Convert start from list to tuple
    goals = [tuple(goal) for goal in goals]  # Convert goals from list to tuple

    g_score = {cell: float('inf') for cell in get_cells(maze_matrix)}
    g_score[start] = 0

    f_score = {cell: float('inf') for cell in get_cells(maze_matrix)}
    f_score[start] = h(start, goals)

    open_set = PriorityQueue()

    # Use a tie-breaking counter to maintain order for elements with the same priority
    tie_breaker = 0

    open_set.put((h(start, goals), tie_breaker, start))
    aPath = {}
    visited_cells = []

    while not open_set.empty():
        currCell = open_set.get()[2]

        if currCell in goals:
            break

        visited_cells.append(currCell)  # Mark the current cell as visited

        for neighbor in get_neighbors(currCell, maze_matrix):
            temp_g_score = g_score[currCell] + 1
            temp_f_score = temp_g_score + h(neighbor, goals)

            if temp_f_score < f_score[neighbor]:
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_f_score

                # Increment the tie-breaker counter to ensure consistent order
                tie_breaker += 1

                open_set.put((temp_f_score, tie_breaker, neighbor))
                aPath[neighbor] = currCell

    fwdPath = {}
    cell = min(goals, key=lambda goal: f_score[goal])  # Update goal to use the nearest goal
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    reversed_path = {v: k for k, v in fwdPath.items()}
    PathList = []
    for key in list(fwdPath.keys()):
        PathList.append(key)
    PathList.reverse()

    return visited_cells, PathList

numeric_matrix = [
    [0, 0, 3],
    [0, 0, 0],
    [2, 0, 3]
]

start_point = [(2, 0)]
end_points = [(0, 2), (2, 2)]
visited_nodes, correct_path = aStar(numeric_matrix, start_point, end_points)

print("Visited Nodes:", visited_nodes)
print("Correct Path:", correct_path)