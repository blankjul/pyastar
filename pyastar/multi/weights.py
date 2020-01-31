

def uniform_weights(n_dim, n_partitions):
    if n_partitions == 0:
        return [1 / n_dim for _ in range(n_dim)]
    else:
        weights = []
        uniform_weights_rec(weights, [], n_dim, n_partitions, n_partitions, 0)
        return weights


def uniform_weights_rec(weights, w, n_dim, n_partitions, beta, depth):
    if depth == n_dim - 1:
        w.append(beta / (1.0 * n_partitions))
        weights.append(w)
    else:
        for i in range(beta + 1):
            _w = list(w)
            _w.append(1.0 * i / (1.0 * n_partitions))
            uniform_weights_rec(weights, _w, n_dim, n_partitions, beta - i, depth + 1)

