import csv
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
    import queue
    nodes = dict()  # store data of all nodes
    queue = queue.Queue()  # bfs queue

    visited = set()  # visited nodes

    with open(edgeFile, newline='') as f:
        edges = csv.DictReader(f)  # read edge data
        for e in edges:  # for all edge
            if int(e['start']) not in nodes.keys():  # if the node is not observed before
                nodes[int(e['start'])] = list()  # then insert the node (list of adjacent edges)
            nodes[int(e['start'])].append((int(e['end']), float(e['distance'])))
            # insert edge data (end node, distance) to the existing list

    queue.put((start, [], 0.0))
    # current node, path nodes, total cost

    while True:
        cur = queue.get()  # get first path in the queue
        cur[1].append(cur[0])  # add current node into current path
        visited.add(cur[0])  # mark current node as visited

        if cur[0] == end:  # if visiting the end node
            return cur[1], cur[2], len(visited)
            # return path nodes, total cost, visited node count

        if cur[0] not in nodes.keys():  # if the node data is not recorded
            continue

        for e in nodes[cur[0]]:  # for every edge coming out from current node
            if e[0] not in visited:  # if the node at the other side is not visited
                queue.put((e[0], list(cur[1]), cur[2] + e[1]))
                # push (next node, path nodes, new path cost) tuple in the queue

    # raise NotImplementedError("To be implemented")
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
