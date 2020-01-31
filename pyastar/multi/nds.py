def get_relation(a, b):
    val = 0
    for i in range(len(a)):
        if a[i] < b[i]:
            # indifferent because once better and once worse
            if val == -1:
                return 0
            val = 1
        elif b[i] < a[i]:
            # indifferent because once better and once worse
            if val == 1:
                return 0
            val = -1
    return val


def non_dominated_sort(F):
    fronts = []
    remaining = set(range(len(F)))

    while len(remaining) > 0:

        front = []

        for i in remaining:

            is_dominated = False
            dominating = set()

            for j in front:
                rel = get_relation(F[i], F[j])
                if rel == 1:
                    dominating.add(j)
                elif rel == -1:
                    is_dominated = True
                    break

            if is_dominated:
                continue
            else:
                front = [x for x in front if x not in dominating]
                front.append(i)

        [remaining.remove(e) for e in front]
        fronts.append(front)

    return fronts


class Archive:

    def __init__(self) -> None:
        super().__init__()
        self.F = []

    def add(self, f, data):
        is_dominating = set()

        for k, (_f, _) in enumerate(self.F):
            rel = get_relation(f, _f)

            if rel == -1:
                return
            elif rel == 1:
                is_dominating.add(k)

        self.F = [self.F[k] for k in range(len(self.F)) if k not in is_dominating]
        self.F.append((f, data))

    def get(self):
        return [elem for (_, elem) in self.F]

    def size(self):
        return len(self.F)


def nds(F):
    nds = Archive()
    for k, f in enumerate(F):
        nds.add(f, k)
    return nds.get()




