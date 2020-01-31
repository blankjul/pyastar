from pyastar.interface import GraphProblem


def find(problem):
    start, n_costs = problem.start, problem.n_costs

    s = [{"node": start, "closed": set([start]), "g": [0.0 for _ in range(n_costs)], "path": [start]}]

    while len(s) > 0:
        entry = s.pop()
        node, closed, g, path = entry["node"], entry["closed"], entry["g"], entry["path"]

        if problem.is_goal(node):
            yield entry
        else:
            for neighbor in problem.get_neighbors(node):
                if neighbor in closed:
                    continue

                costs = problem.get_costs(node, neighbor)
                neighbor_g = [g[k] + costs[k] for k in range(len(g))]

                neighbor_closed = set(closed)
                neighbor_closed.add(neighbor)

                neighbor_path = list(path) + [neighbor]

                entry = {"node": neighbor, "closed": neighbor_closed, "g": neighbor_g, "path": neighbor_path}
                s.append(entry)

                # print(entry)


def exhaustive(G, s, g):
    ret = []
    problem = GraphProblem(G, s, g)
    for entry in find(problem):
        ret.append(entry)
    return ret