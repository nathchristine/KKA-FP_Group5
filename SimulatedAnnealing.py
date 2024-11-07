import pandas as pd
import random
import math
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

def get_distance(store1, store2):
    return ((store1.coordinateX - store2.coordinateX) ** 2 + (store1.coordinateY - store2.coordinateY) ** 2) ** 0.5

def calculate_total_distance(path):
    return sum(get_distance(path[i], path[i + 1]) for i in range(len(path) - 1))

def nearest_neighbor_path(start_store, store_types):
    initial_path = [start_store]
    remaining_types = set(store_types) - {start_store.type}
    current_store = start_store

    while remaining_types:
        nearest_store = min(
            [store for store in stores if store.type in remaining_types],
            key=lambda s: get_distance(current_store, s)
        )
        initial_path.append(nearest_store)
        remaining_types.remove(nearest_store.type)
        current_store = nearest_store
    
    return initial_path

def simulated_annealing(stores, start_store, initial_temperature, min_temperature, cooling_rate, max_iterations):
    current_path = nearest_neighbor_path(start_store, store_types)
    current_cost = calculate_total_distance(current_path)
    best_path, best_cost = current_path[:], current_cost

    temperature = initial_temperature
    improvement_threshold = 1e-3 
    
    for i in range(max_iterations):
        new_path = current_path[:]
        if random.random() < 0.5: 
            idx1 = random.randint(1, len(new_path) - 2)
            new_path[idx1], new_path[idx1 + 1] = new_path[idx1 + 1], new_path[idx1]
        else:  
            idx1, idx2 = random.sample(range(1, len(new_path)), 2)
            new_path[idx1], new_path[idx2] = new_path[idx2], new_path[idx1]
        
        new_cost = calculate_total_distance(new_path)

        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
            current_path, current_cost = new_path, new_cost
        if current_cost < best_cost:
            best_path, best_cost = current_path[:], current_cost
        
        temperature *= cooling_rate
        if temperature < min_temperature or abs(best_cost - current_cost) < improvement_threshold:
            break

    return best_path, best_cost

print("Please choose a store type (Start): ")
print(store_types)
store_type = input("Enter store type: ")
print("Please choose a starting store (index): ")
for i, store in enumerate(stores):
    if store.type == store_type:
        print(f"{i}: {store.name}")
store_index = int(input())
start_store = stores[store_index]

initial_temperature = 1000
min_temperature = 0.01 
cooling_rate = 0.999  
max_iterations = 50000

start_time = time.time()
best_path, best_cost = simulated_annealing(stores, start_store, initial_temperature, min_temperature, cooling_rate, max_iterations)
end_time = time.time()

path = " - ".join([f"{store.name}({store.type})" for store in best_path])
print(f"Path: {path}")
print(f"Cost: {best_cost}")
print(f"Execution Time: {end_time - start_time} seconds")
