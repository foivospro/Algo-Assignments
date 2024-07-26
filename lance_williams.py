import argparse


def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            row = [int(x) for x in line.split()]
            for num in row:
                data.append([num])
    return data


def merge_clusters(clusters, distances, i, j, method):
    new_cluster = clusters[i] + clusters[j]
    clusters_temp = deep_copy(clusters)
    distances_temp = deep_copy(distances)
    clusters_temp.pop(j)
    clusters_temp[i] = new_cluster
    for k in range(len(distances)):
        if k != i:
            distances_temp[i][k] = get_distance(i, j, k, method, distances, clusters)
            distances_temp[k][i] = distances_temp[i][k]
    distances_temp.pop(j)
    for row in distances_temp:
        row.pop(j)
    return clusters_temp, distances_temp


def deep_copy(original):
    if isinstance(original, list):
        return [deep_copy(item) for item in original]
    else:
        return original

def get_distance(s, t, v, method, distances, clusters):
    alpha_i, alpha_j, beta, gamma = 0.5, 0.5, 0, 0
    if method == 'single':
        gamma = -0.5
    elif method == 'complete':
        gamma = 0.5
    elif method == 'average':
        alpha_i = len(clusters[s]) / (len(clusters[s]) + len(clusters[t]))
        alpha_j = len(clusters[t]) / (len(clusters[s]) + len(clusters[t]))
    elif method == 'ward':
        alpha_i = (len(clusters[s]) + len(clusters[v])) / (len(clusters[s]) + len(clusters[v]) + len(clusters[t]))
        alpha_j = (len(clusters[t]) + len(clusters[v])) / (len(clusters[s]) + len(clusters[v]) + len(clusters[t]))
        beta = -len(clusters[v])/(len(clusters[s]) + len(clusters[v]) + len(clusters[t]))
    return alpha_i * distances[s][v] + alpha_j * distances[t][v] + beta * distances[s][t] + gamma * abs(distances[s][v] - distances[t][v])


def get_nearest_clusters(distances):
    min_distance = float("inf")
    for i in range(len(distances)):
        for j in range(i+1, len(distances)):
            if distances[i][j] < min_distance and distances[i][j] != 0:
                min_distance = distances[i][j]
                min_i, min_j = i, j
    return min_i, min_j, min_distance


def lance_williams(clusters, method):
    distances = [[abs(clusters[i][0] - clusters[j][0]) for j in range(len(clusters))] for i in range(len(clusters))]
    while len(clusters) > 1:
        i, j, min_distance = get_nearest_clusters(distances)
        print(f'({str(clusters[i]).replace("[","").replace("]","").replace(",","")}) ({str(clusters[j]).replace("[","").replace("]","").replace(",","")}) {min_distance:.2f} {len(clusters[i]) + len(clusters[j])}')
        clusters, distances = merge_clusters(clusters, distances, i, j, method)
    return clusters


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('method', choices=['single', 'complete', 'average', 'ward'])
    parser.add_argument('input_filename')
    args = parser.parse_args()
    clusters = lance_williams(sorted(read_data(args.input_filename)), args.method)
