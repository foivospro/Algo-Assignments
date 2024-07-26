import argparse
from collections import deque


def lex_bfs(graph):
    S = [list(graph.keys())]
    visited = []
    while S:
        u = S[0].pop(0)
        visited.append(u)
        if len(S[0]) == 0:
            S.pop(0)
        for v in graph[u]:
            if v not in visited:
                found = False
                for i, sv in enumerate(S):
                    if v in sv:
                        found = True
                        sv_new = [x for x in sv if x in graph[u]]
                        sv[:] = [x for x in sv if x not in graph[u]]
                        S.insert(i, sv_new)
                        break
                if not found:
                    S.append([v])
        S = [s for s in S if s]
    return visited


def is_chordal(rev_order, graph):
    for u in rev_order:
        RN_u, RN_n = set(), set()
        flag = 0
        for i in rev_order[rev_order.index(u)+1:]:
            if i in graph[u]:
                RN_u.add(i)
                if flag == 0:
                    fist_n = i
                    flag = flag + 1
        for k in rev_order[rev_order.index(fist_n)+1:]:
            if k in graph[fist_n]:
                RN_n.add(k)
        if not ((RN_u-{fist_n}).issubset(RN_n)):
            return False
    return True


def is_interval(graph, is_chordal):
    if not is_chordal:
        return False
    k = 1
    n = len(graph)
    C = [[0] * n for _ in range(n)]
    for node in graph:
        G = graph.copy()
        neighbors = G[node]
        G.pop(node)
        for neighbor in neighbors:
            G.pop(neighbor)
        for key, value in G.items():
            G[key] = [x for x in value if x in G]
        not_vis = set()
        if G.keys():
            components = bfs(G, min(G.keys()))
            not_vis = set(G.keys()) - components
            for c in components:
                C[node][c] = k
            k = k + 1
        while not_vis:
            components = bfs(G, min(not_vis))
            for c in components:
                C[node][c] = k
            k = k + 1
            not_vis = not_vis - components
    for u in range(n):
        for nn in range(n):
            for w in range(n):
                if C[u][nn] != 0 and C[u][w] != 0 and C[nn][u] != 0 and C[nn][w] != 0 and C[w][u] != 0 and C[w][nn] !=0:
                    if C[u][nn] == C[u][w] and C[nn][u] == C[nn][w] and C[w][u] == C[w][nn]:
                        return False
    return True


def bfs(graph, start_node):
    visited = set()
    queue = deque([start_node])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(set(graph[node]) - visited)
    return visited


def read_data(filename):
    graph = {}
    with open(filename) as f:
        for line in f:
            node1, node2 = map(int, line.strip().split())
            if node1 not in graph:
                graph[node1] = []
            if node2 not in graph:
                graph[node2] = []
            graph[node1].append(node2)
            graph[node2].append(node1)
    for key in graph:
        graph[key].sort()
    return dict(sorted(graph.items()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('task', choices=['lexbfs', 'chordal', 'interval'])
    parser.add_argument('input_filename')
    args = parser.parse_args()
    graph = read_data(args.input_filename)
    if args.task == 'lexbfs':
        a = lex_bfs(graph)
        print(a)
    elif args.task == "chordal":
        a = lex_bfs(graph)
        b = a[::-1]
        print(is_chordal(b, graph))
    elif args.task == "interval":
        a = lex_bfs(graph)
        b = a[::-1]
        print(is_interval(graph, is_chordal(b, graph)))

