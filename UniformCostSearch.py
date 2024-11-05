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

def uniform_cost_search(stores, start):
    # Priority queue to store (cost, -rating, node)
    priority_queue = [(0, -start.rating, start)]
    visited = []
    type_visited = set()

    while priority_queue:
        cost, neg_rating, Store = heapq.heappop(priority_queue)

        if Store in visited or Store.type in type_visited:
            continue
        
        visited.append(Store)
        type_visited.add(Store.type)
        priority_queue.clear()

        if len(type_visited) == len(store_types):
            return visited, cost
        
        for store in stores:
            if store not in visited and store.type not in type_visited:
                heapq.heappush(priority_queue, (cost + get_distance(Store, store), -store.rating, store))

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
visited, cost = uniform_cost_search(stores, start)
end_time = time.time()

path = " - ".join([f"{store[0]}({store[1]})" for store in visited])
print(f"Path: {path}")
print(f"Cost: {cost}")
print(f"Execution Time: {end_time - start_time} seconds")
