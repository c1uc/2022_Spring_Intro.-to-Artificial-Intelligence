import csv
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    import queue
    nodes = dict()  # store data of all nodes
    queue = queue.PriorityQueue()  # ucs priority queue

    visited = set()  # visited nodes

    with open(edgeFile, newline='') as f:
        edges = csv.DictReader(f)  # read edge data
        for e in edges:  # for all edge
            if int(e['start']) not in nodes.keys():  # if the node is not observed before
                nodes[int(e['start'])] = list()  # then insert the node (list of adjacent edges)
            nodes[int(e['start'])].append((int(e['end']), float(e['distance'])))
            # insert edge data (end node, distance) to the existing list

    queue.put((0.0, start, []))
    # total cost, current node, path nodes
    # (total cost is stored in the front to be the priority key)

    while True:
        cur = queue.get()  # get first path in the queue
        cur[2].append(cur[1])  # add current node into current path
        visited.add(cur[1])  # mark current node as visited

        if cur[1] == end:  # if visiting the end node
            return cur[2], cur[0], len(visited)
            # return path nodes, total cost, visited node count

        if cur[1] not in nodes.keys():  # if the node data is not recorded
            continue

        for e in nodes[cur[1]]:  # for every edge coming out from current node
            if e[0] not in visited:  # if the node at the other side is not visited
                queue.put((cur[0] + e[1], e[0], list(cur[2])))
                # push (new path cost, next node, path nodes) tuple in the queue

    # raise NotImplementedError("To be implemented")
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(426882161, 1737223506)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
