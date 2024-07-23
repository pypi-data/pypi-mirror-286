def a_star_search(graph, start, goal, heuristic):
    visited = set()
    open_list = [(heuristic[start], start)]
    came_from = {}
    cost_so_far = {start: 0}

    while open_list:
        open_list.sort()  # Sort based on heuristic value
        _, current = open_list.pop(0)
        visited.add(current)

        if current == goal:
            print("Goal found!")
            return

        print("Current node:", current)
        for neighbour, cost in graph[current].items():
            new_cost = cost_so_far[current] + cost
            if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_cost
                priority = new_cost + heuristic[neighbour]
                open_list.append((priority, neighbour))
                came_from[neighbour] = current

    print("Goal not found!")

# Example graph
graph = {
    'A': {'B': 2, 'C': 4},
    'B': {'A': 2, 'D': 5},
    'C': {'A': 4, 'D': 3},
    'D': {'B': 5, 'C': 3}
}

# Example heuristic values
heuristic_values = {
    'A': 5,
    'B': 4,
    'C': 2,
    'D': 0
}

# Perform search
a_star_search(graph, 'A', 'D', heuristic_values)