import heapq

def heuristic(state, goal):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            gi = goal.index(state[i])
            r1, c1 = i//3, i%3
            r2, c2 = gi//3, gi%3
            distance += abs(r1-r2) + abs(c1-c2)
    return distance

def get_neighbors(state):
    neighbors = []
    blank = state.index(0)
    moves = [-3, 3, -1, 1]

    for move in moves:
        new_pos = blank + move
        if new_pos < 0 or new_pos > 8:
            continue
        if move == -1 and blank % 3 == 0:
            continue
        if move == 1 and blank % 3 == 2:
            continue

        new_state = list(state)
        new_state[blank], new_state[new_pos] = new_state[new_pos], new_state[blank]
        neighbors.append(tuple(new_state))
    return neighbors

def a_star(start, goal):
    pq = []
    heapq.heappush(pq, (0, start))
    came_from = {}
    g_cost = {start: 0}
    visited = set()

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            return reconstruct_path(came_from, current)

        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor in visited:
                continue

            new_g = g_cost[current] + 1

            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = new_g
                f = new_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (f, neighbor))

    return None

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

print("Enter initial state (use 0 for blank)")
start = tuple(map(int, input().split()))

print("Enter goal state (use 0 for blank)")
goal = tuple(map(int, input().split()))

solution = a_star(start, goal)

if solution:
    print("\nSolution found in", len(solution)-1, "moves\n")
    for step in solution:
        print_puzzle(step)
else:
    print("No solution found")


