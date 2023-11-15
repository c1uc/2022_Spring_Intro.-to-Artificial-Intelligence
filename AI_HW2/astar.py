import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)
    import queue
    nodes = dict()  # store data of all nodes
    heuristicTable = dict()  # store all heuristic value
    queue = queue.PriorityQueue()  # ucs priority queue
    visited = set()  # visited nodes

    with open(edgeFile, newline='') as f:
        edges = csv.DictReader(f)  # read edge data
        for e in edges:  # for all edge
            if int(e['start']) not in nodes.keys():  # if the node is not observed before
                nodes[int(e['start'])] = list()  # then insert the node (list of adjacent edges)
            nodes[int(e['start'])].append((int(e['end']), float(e['distance'])))
            # insert edge data (end node, distance) to the existing list

    with open(heuristicFile, newline='') as f:
        heuristics = csv.DictReader(f)  # read heuristic data
        for n in heuristics:
            heuristicTable[int(n['node'])] = float(n[str(end)])
            # insert heuristic value of current end node for all nodes

    # h(x) + path cost, path cost, node, path
    # h(x) + path cost in the front to be the priority key
    queue.put((heuristicTable[start], 0.0, start, []))

    while True:
        cur = queue.get()  # get first path in the queue
        cur[3].append(cur[2])  # add current node into current path
        visited.add(cur[2])  # mark current node as visited

        if cur[2] == end:  # if visiting the end node
            return cur[3], cur[1], len(visited)
            # return path nodes, total cost, visited node count

        if cur[2] not in nodes.keys():  # if the node data is not recorded
            continue

        for e in nodes[cur[2]]:  # for every edge coming out from current node
            if e[0] not in visited:  # if the node at the other side is not visited
                queue.put((cur[1] + e[1] + heuristicTable[e[0]], cur[1] + e[1], e[0], list(cur[3])))
                # push (h(x) + new path cost, new path cost, next node, path nodes) tuple in the queue

    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(426882161, 1737223506)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
