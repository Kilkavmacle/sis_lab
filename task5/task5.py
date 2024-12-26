import numpy
import json


def r_js(js_file):
    with open(js_file, 'r') as file:
        data = json.load(file)
        return data['data']


def w_json(core_AB, out_file):
    with open(out_file, 'w') as file:
        json.dump({"core_AB": core_AB}, file, indent=4)


def creat_matrix(ranking, n):
    Y = numpy.zeros((n, n), dtype=int)
    numpy.fill_diagonal(Y, 1)

    for idx, cluster in enumerate(ranking):
        if isinstance(cluster, int):
            cluster = [cluster]

        for i in cluster:
            for j in cluster:
                Y[i - 1][j - 1] = 1

        for i in cluster:
            for prev_cluster in ranking[:idx]:
                if isinstance(prev_cluster, int):
                    prev_cluster = [prev_cluster]
                for j in prev_cluster:
                    Y[j - 1][i - 1] = 1

    return Y


def find_disc(YA, YB):
    n = YA.shape[0]
    disc = []
    for i in range(n):
        for j in range(n):
            if YA[i, j] == 1 and YB[i, j] == 0 and YA[j, i] == 0 and YB[j, i] == 1:
                disc.append((i + 1, j + 1)) 
            elif YA[i, j] == 0 and YB[i, j] == 1 and YA[j, i] == 1 and YB[j, i] == 0:
                disc.append((j + 1, i + 1))
    return disc


def find_core(disc):
    core_AB = []
    added = set()

    for x, y in disc:
        if any(x in group or y in group for group in core_AB):
            for group in core_AB:
                if x in group or y in group:
                    if x not in group:
                        group.append(x)
                    if y not in group:
                        group.append(y)
                    break
        else:
            core_AB.append([x, y])

        added.update([x, y])

    return core_AB


def main(A, B, out_file):
    ranking_A = r_js(A)
    ranking_B = r_js(B)

    n_A = sum(len(item) if isinstance(item, list) else 1 for item in ranking_A)
    n_B = sum(len(item) if isinstance(item, list) else 1 for item in ranking_B)
    n = max(n_A, n_B)

    YA = creat_matrix(ranking_A, n)
    YB = creat_matrix(ranking_B, n)
    disc = find_disc(YA, YB)
    print(f"Contradictions: {disc}")
    core_AB = find_core(disc)
    print(f"Core AB: {core_AB}")
    w_json(core_AB, out_file)


if __name__ == "__main__":

    A = './a.json'
    B = './b.json'
    out_file = './core_AB.json'

    main(A, B, out_file)