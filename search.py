import copy
import queue

import state
from queue import PriorityQueue, Queue

def BFS(start, goal, M, N):
    queue = []
    queue.append((start, ""))
    visited = set()
    visited.add(start)
    parent = {}
    checkFinish = False
    while len(queue) != 0:
        curr_state = queue.pop(0)
        if curr_state[0] == goal:
            print("Tim thay loi giai")
            checkFinish = True
            break
        # Lưu thêm cost với giá trị không đổi
        for neighbor in state.get_neighbor(curr_state[0], M, N):
            if neighbor[0] not in visited:
                queue.append(neighbor)
                visited.add(neighbor[0])
                parent[neighbor] = curr_state
    print("So dinh da duyet: ", len(visited))
    if not checkFinish:
        print("Không tìm thấy lời giải")
    path = []
    if checkFinish:
        while curr_state[0] != start:
            path.append(curr_state[1])
            curr_state = parent[curr_state]
    path.reverse()
    return ''.join(path), len(visited)

def search_cost(start, goal, M, N, fn, init_cost):
    pq = PriorityQueue()
    pq.put((init_cost, (start, "", 0)))
    visited = set()
    visited.add(start)
    parent = {}
    checkFinish = False
    while pq.qsize() != 0:
        curr_state = pq.get()
        if curr_state[1][0] == goal:
            print("Tim thay loi giai")
            checkFinish = True
            break
        for neighbor in state.get_neighbor_cost(curr_state[1][0], M, N, fn, curr_state[0], curr_state[1][2]):
            if neighbor[1][0] not in visited:
                pq.put(neighbor)
                visited.add(neighbor[1][0])
                parent[neighbor] = curr_state
    print("So dinh da duyet: ", len(visited))
    if not checkFinish:
        print("Không tìm thấy lời giải")
    path = []
    if checkFinish:
        while curr_state[1][0] != start:
            path.append(curr_state[1][1])
            curr_state = parent[curr_state]
    path.reverse()
    return ''.join(path), len(visited)

def UCS(start, goal, M, N):
    def fn(cost, curr_state, g):
        return cost+1
    return search_cost(start, goal, M, N, fn, 0)

def pos_2D(index, M, N):
    return index // M , index % N

def heu(curr_state, goal, M, N):
    h = 0
    for i in range(len(curr_state)):
        curr_x, curr_y = pos_2D(i, M, N)
        goal_x, goal_y = pos_2D(goal.index(curr_state[i]), M, N)
        h += abs(curr_x - goal_x) + abs(curr_y - goal_y)
    return h

def heu_missplaced(curr_state, goal, M, N):
    h = 0
    for i in range(len(curr_state)):
        curr_x, curr_y = pos_2D(i, M, N)
        goal_x, goal_y = pos_2D(goal.index(curr_state[i]), M, N)
        if curr_x != goal_x or curr_y != goal_y:
            h+=1
    return h

def AStar(start, goal, M, N):
    def fn(cost, curr_state, g):
        return g + heu_missplaced(curr_state, goal, M, N)
    return search_cost(start, goal, M, N, fn, heu_missplaced(start, goal, M, N))

def Greedy(start, goal, M, N):
    def fn(cost, curr_state, g):
        return heu(curr_state, goal, M, N)
    return search_cost(start, goal, M, N, fn, heu(start, goal, M, N))

def Hill_Climbing(start, goal, M, N):
    def fn(cost, curr_state, g):
        return heu_missplaced(curr_state, goal, M, N)
    q = []
    q.append((heu_missplaced(start, goal, M, N), (start, "", 0)))
    visited = set()
    visited.add(start)
    parent = {}
    checkFinish = False
    while len(q) != 0:
        curr_state = q.pop(0)
        if curr_state[1][0] == goal:
            print("Tim thay loi giai")
            checkFinish = True
            break
        pq = PriorityQueue()

        for neighbor in state.get_neighbor_cost(curr_state[1][0], M, N, fn, curr_state[0], curr_state[1][2]):
            print(curr_state[0], ">=" , neighbor[0], "and ", neighbor[1][0] not in visited)
            if neighbor[1][0] not in visited and neighbor[0] <= curr_state[0]:
                pq.put(neighbor)
        if(pq.qsize() != 0):
            nb = pq.get()
            print(nb[1][0])
            q.append(nb)
            visited.add(nb[1][0])
            parent[nb] = curr_state
    print("So dinh da duyet: ", len(visited))
    if not checkFinish:
        print("Không tìm thấy lời giải")
    path = []
    if checkFinish:
        while curr_state[1][0] != start:
            path.append(curr_state[1][1])
            curr_state = parent[curr_state]
    path.reverse()
    return ''.join(path), len(visited)

def DFS(start, goal, M, N, max_depth):
    def count_deep(deep, current_state, g):
        return deep + 1
    stack = []
    stack.append((0, (start, "", 0)))
    visited = set()
    visited.add(start)
    parent = {}
    checkFinish = False
    init_state = Queue()
    deep_count = 0
    while len(stack) != 0:
        curr_state = stack.pop()
        deep_count = max(deep_count, curr_state[0])
        if curr_state[0] >= max_depth:
            continue
        if curr_state[1][0] == goal:
            checkFinish = True
            break
        for neighbor in state.get_neighbor_cost(curr_state[1][0], M, N, count_deep, curr_state[0], 0):
            if neighbor[1][0] not in visited:
                stack.append(neighbor)
                visited.add(neighbor[1][0])
                parent[neighbor] = curr_state
    path = []
    while curr_state[1][0] != start:
        path.append(curr_state[1][1])
        curr_state = parent[curr_state]
    path.reverse()
    state_count = len(visited)
    return ''.join(path), checkFinish, deep_count, state_count

def IDFS(start, goal, M, N, max_depth):
    def count_deep(deep, current_state, g):
        return deep + 1
    qu = queue.Queue()
    qu.put((0, (start, "", 0)))
    visited = set()
    visited.add(start)
    parent = {}
    checkFinish = False
    while qu.qsize() != 0:
        if checkFinish:
            break
        curr_start = qu.get()
        depth = max_depth + curr_start[0]
        stack = []
        stack.append(curr_start)
        while len(stack) != 0:
            curr_state = stack.pop()
            if curr_state[0] >= depth:
                continue
            if curr_state[1][0] == goal:
                checkFinish = True
                break
            for neighbor in state.get_neighbor_cost(curr_state[1][0], M, N, count_deep, curr_state[0], 0):
                if neighbor[1][0] not in visited:
                    stack.append(neighbor)
                    visited.add(neighbor[1][0])
                    parent[neighbor] = curr_state
                    if neighbor[0] == depth:
                        qu.put(neighbor)
    path = []
    while curr_state[1][0] != start:
        path.append(curr_state[1][1])
        curr_state = parent[curr_state]
    path.reverse()
    return ''.join(path), checkFinish, len(visited)