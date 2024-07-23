import math
from collections import deque
import sys


# Простой поиск для любого списка
def l_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return None


# Бинарный поиск для сортированного (по возрастанию) списка
def b_search(arr, target):
    border = [0, len(arr)-1]

    while border[0] <= border[1]:
        mid = int((sum(border)) / 2)

        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            border[1] = mid - 1
        else:
            border[0] = mid + 1
    return None


# Быстрая сортировка
def q_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[int(len(arr) / 2)]
        less_than_pivot = [x for x in arr[1:] if x <= pivot]
        greater_than_pivot = [x for x in arr[1:] if x > pivot]
        return q_sort(less_than_pivot) + [pivot] + q_sort(greater_than_pivot)


#Динамическое программирование
def knapsack(capacity, items):
    n = len(items)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            weight, value = items[i - 1]
            if weight <= j:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - weight] + value)
            else:
                dp[i][j] = dp[i - 1][j]

    max_value = dp[n][capacity]
    selected_items = []
    i = n
    j = capacity
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            selected_items.append(items[i - 1])
            j -= items[i - 1][0]
        i -= 1

    return max_value, selected_items


# Алгоритм k-ближайших соседей
def knn(items, test, k=1):
    dist = []
    for el in items:
        c_l = min(len(test), len(el))
        d = math.sqrt(sum(((test[i] - el[i]) ** 2) for i in range(c_l)))
        dist.append((d, el))

    dist.sort()
    res = [item for _, item in dist[:k]]
    return res

def search_in_width(graph, start):
    map = {}
    visited = set()
    queue = deque([start])
    level = 0

    while queue:
        map[level] = []
        for _ in range(len(queue)):
            current = queue.popleft()
            if current not in visited:
                map[level].append(current)
                visited.add(current)
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        level += 1
    return map


#Алгоритм Дейкстера
def dijkstra(graph, start):
    distances = {node: sys.maxsize for node in graph}
    distances[start] = 0
    visited = set()
    unvisited = set(graph.keys())

    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])
        unvisited.remove(current)
        visited.add(current)

        for neighbor, weight in graph[current].items():
            if neighbor not in visited:
                new_distance = distances[current] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

    return distances