from collections import deque
import argparse

def pmin(words):
    if not words:
        return 0
    min = float('inf')
    for string in words:
        if len(string) < min:
            min = len(string)
    return min


def create_trie(words):
    trie = {0: {'links': {}, 'is_terminal': False}}
    node_count = 1
    for word in words:
        current_node = trie[0]
        word = word[::-1]
        for char in word:
            links = current_node['links']
            if char not in links:
                links[char] = node_count
                trie[node_count] = {'links': {}, 'is_terminal': False}
                node_count += 1
            current_node = trie[links[char]]
        current_node['is_terminal'] = True
    return trie


def CreateRtOccurrencesTable(p):
    rt = [(len(p)+1)] * 26
    m = len(p)
    for i in range(m):
        rt[(ord(p[i])-ord('a'))] = m - i
    return rt


def rt_final(words):
    final_rt =[]
    for word in words:
        rt_i = CreateRtOccurrencesTable(word)
        final_rt.append(rt_i)
    min_values = [min(column) for column in zip(*final_rt)]
    return min_values


def is_terminal(node):
    return trie[node]['is_terminal']


def find_parent(trie, node):
    for parent, data in trie.items():
        if node in data['links'].values():
            return parent
    return None


def build_failure_table(trie):
    failure = [0] * len(trie)
    for child in trie[0]['links'].values():
        failure[child] = 0
    queue = deque(trie[0]['links'].values())
    while queue:
        current = queue.popleft()
        for char, child in trie[current]['links'].items():
            queue.append(child)
            parent = failure[current]
            while parent != 0 and char not in trie[parent]['links']:
                parent = failure[parent]
            if char in trie[parent]['links']:
                failure[child] = trie[parent]['links'][char]
            else:
                failure[child] = 0
    return failure


def find_depth(node, trie):
    if not node:
        return 0
    queue = deque()
    queue.append((0, 0))
    while queue:
        current, depth = queue.popleft()
        if current == node:
            return depth
        if current in trie.keys():
            for child in trie[current]['links'].values():
                queue.append((child, depth + 1))
    return -1


def create_set1(failure):
    set1 = [[] for _ in range(len(trie))]
    for i, u in enumerate(trie.keys()):
        for j, f in enumerate(failure):
            if u == f:
                set1[i].append(j)
    return set1


def create_set2(set1, trie):
    set2 = [[] for _ in range(len(trie))]
    for u, sub_list in enumerate(set1):
        for v in sub_list:
            if is_terminal(v):
                set2[u].append(v)
    return set2



def construct_s1(set1, pmin, root):
    s1 = [0] * len(trie)
    s1[root] = 1
    for u, sub_list in enumerate(set1):
        if u!=root:
            s1[u] = pmin
        for u_new in sub_list:
            if u != root and u_new in set1[u]:
                k = find_depth(u_new, trie) - find_depth(u, trie)
                s1[u] = min(pmin, k)
    return s1


def construct_s2(set2, pmin, root):
    s2 = [0] * len(trie)
    s2[root] = pmin
    for u, sub_list in enumerate(set1):
        if u != root:
            s2[u] = s2[find_parent(trie, u)]
        for u_new in sub_list:
            if u != root and u_new in set2[u]:
                k = find_depth(u_new, trie) - find_depth(u, trie)
                s2[u] = min(s2[find_parent(trie, u)], k)
    return s2


def HasChild(trie, u, char):
    links = trie[u]['links']
    for edge_char in links.keys():
        if edge_char == char:
            return True
    return False


def GetChild(trie, u, char):
    link = trie[u]['links'].get(char, None)
    if link is not None:
        return link
    return None


def CommentzWalter(t, trie, pmin, rt, s1, s2):
    q = deque()
    i = pmin - 1
    j = 0
    u = 0
    m = ''
    while i < len(t):
        while HasChild(trie, u, t[i - j]):
            u = GetChild(trie, u, t[i - j])
            m += t[i - j]
            j += 1
            if is_terminal(u):
                q.append((m[::-1], i - j + 1))
        if j > i:
            j = i
        s = min(s2[u], max(s1[u], rt[(ord(t[i - j]) - ord('a'))] - j - 1))
        i += s
        j = 0
        u = 0
        m = ''
    return q


def read_text_from_file(input_filename):
    try:
        with open(input_filename, "r") as file:
            text = file.read()
            words = text.split()
    except FileNotFoundError:
        print(f"File '{input_filename}' not found.")
        words = []
    return words


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("kw", nargs="+")
    parser.add_argument("input_filename")
    args = parser.parse_args()
    t = read_text_from_file(args.input_filename)
    t = t[0].strip("[]'")
    words = args.kw
    trie = create_trie(words)
    pmin = pmin(words)
    rt = rt_final(words)
    failure = build_failure_table(trie)
    set1 = create_set1(failure)
    set2 = create_set2(set1, trie)
    s1 = construct_s1(set1, pmin, 0)
    s2 = construct_s2(set2, pmin, 0)
    cw = CommentzWalter(t, trie, pmin, rt, s1, s2)
    if args.verbose:
        for i, (x, y) in enumerate(zip(s1, s2), start=1):
            print(f"{i-1}: {x},{y}")
    for item in cw:
        print(f"{item[0]}: {item[1]}")

