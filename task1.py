import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    idx = 0

    n = int(data[idx]); idx += 1
    s = int(data[idx]); idx += 1
    t = int(data[idx]); idx += 1

    # adjacency list: для каждой вершины список (соседняя_вершина, вес)
    adj = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        a = int(data[idx]); idx += 1
        b = int(data[idx]); idx += 1
        w = int(data[idx]); idx += 1
        adj[a].append((b, w))
        adj[b].append((a, w))

    # BFS от s, накапливаем сумму весов (т.к. W = сумма w_i на пути, поскольку P = произведение exp(-w_i) = exp(-sum(w_i)))
    dist = [-1] * (n + 1)
    dist[s] = 0
    queue = deque([s])

    while queue:
        u = queue.popleft()
        if u == t:
            break
        for v, w in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                queue.append(v)

    print(dist[t])


if __name__ == "__main__":
    main()