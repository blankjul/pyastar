
def evaluate_path(problem, path):
    is_scalar = problem.n_costs is None
    if is_scalar:
        costs = 0
        for k in range(len(path) - 1):
            costs += problem.get_costs(path[k], path[k + 1])
    else:
        costs = [0 for _ in range(problem.n_costs)]
        for k in range(len(path) - 1):
            c = problem.get_costs(path[k], path[k + 1])
            costs = [costs[m] + c[m] for m in range(problem.n_costs)]
    return costs
