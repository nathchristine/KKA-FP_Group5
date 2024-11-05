import pandas as pd
import heapq
import time
from collections import namedtuple


df = pd.read_csv('data.csv')

store_types = df['Store Type'].unique()

Store = namedtuple('Store', ['name', 'type', 'floor', 'rating', 'coordinateX', 'coordinateY'])

stores = [
    Store(name, type, floor, rating, coordinateX, coordinateY)
    for name, type, floor, rating, coordinateX, coordinateY in zip(
        df['Store Names'], df['Store Type'], df['Location'], df['Rating'], df['Coordinate X'], df['Coordinate Y']
    )
]

def heuristic(store1, store2):
    return ((store1.coordinateX - store2.coordinateX) ** 2 + (store1.coordinateY - store2.coordinateY) ** 2) ** 0.5

def a_star_search(stores, start):
    priority_queue = [(0, 0, -start.rating, start)]
    visited = set()
    type_visited = set()

    while priority_queue:
        estimated_cost, actual_cost, neg_rating, node = heapq.heappop(priority_queue)

        store_key = (node.name, node.type, node.coordinateX, node.coordinateY)

        if store_key in visited or node.type in type_visited:
            continue

        visited.add(store_key)
        type_visited.add(node.type)

        if len(type_visited) == len(store_types):
            return visited, actual_cost

        for store in stores:
            store_key = (store.name, store.type, store.coordinateX, store.coordinateY)
            if store_key not in visited and store.type not in type_visited:
                distance = get_distance(node, store)
                new_cost = actual_cost + distance
                estimated_total_cost = new_cost + heuristic(store, stores[0])  # A* f(n) = g(n) + h(n)
                heapq.heappush(priority_queue, (estimated_total_cost, new_cost, -store.rating, store))

    return None, float('inf')


def get_distance(store1, store2):
    return ((store1.coordinateX - store2.coordinateX) ** 2 + (store1.coordinateY - store2.coordinateY) ** 2) ** 0.5

print("Please choose a store type (Start): ")
print(store_types)
store_type = input()
print("Please choose a store (index): ")
for i, store in enumerate(stores):
    if store.type == store_type:
        print(f"{i}: {store.name}")

store_index = int(input())
start = stores[store_index]

start_time = time.time()
visited, cost = a_star_search(stores, start)
end_time = time.time()

path = " - ".join([f"{store[0]}({store[1]})" for store in visited])
print(f"Path: {path}")
print(f"Cost: {cost}")
print(f"Execution Time: {end_time - start_time} seconds")
