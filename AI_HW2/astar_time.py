import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
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
            nodes[int(e['start'])].append((int(e['end']), float(e['distance']) / float(e['speed limit']) * 3.6))
            # insert edge data (end node, path cost) to the existing list
            # new path cost is distance / speed limit (remember to change km/hr into m/s)

    with open(heuristicFile, newline='') as f:
        heuristics = csv.DictReader(f)  # read heuristic data
        for n in heuristics:
            heuristicTable[int(n['node'])] = float(n[str(end)]) / 60.0 * 3.6
            # set heuristic value to straight distance / 60(km/hr)
            # to change the heuristic value unit to s

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
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
