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
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += get_distance(path[i], path[i + 1])
    return total_distance

def simulated_annealing(stores, start_store, initial_temperature, cooling_rate, iterations):
    initial_path = [start_store]
    for store_type in store_types:
        type_stores = [store for store in stores if store.type == store_type and store != start_store]
        if type_stores:
            initial_path.append(random.choice(type_stores))
    current_path = initial_path[:]
    current_cost = calculate_total_distance(current_path)
    best_path = current_path[:]
    best_cost = current_cost
    temperature = initial_temperature
    for i in range(iterations):
        new_path = current_path[:]
        idx1, idx2 = random.sample(range(1, len(new_path)), 2)  # Ensure start_store remains at the beginning
        new_path[idx1], new_path[idx2] = new_path[idx2], new_path[idx1]
        new_cost = calculate_total_distance(new_path)
        if new_cost < current_cost:
            current_path, current_cost = new_path, new_cost
        else:
            probability = math.exp((current_cost - new_cost) / temperature)
            if random.random() < probability:
                current_path, current_cost = new_path, new_cost
        if current_cost < best_cost:
            best_path, best_cost = current_path[:], current_cost
        temperature *= cooling_rate
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
cooling_rate = 0.995
iterations = 10000

start_time = time.time()
best_path, best_cost = simulated_annealing(stores, start_store, initial_temperature, cooling_rate, iterations)
end_time = time.time()

path = " - ".join([f"{store.name}({store.type})" for store in best_path])
print(f"Path: {path}")
print(f"Cost: {best_cost}")
print(f"Execution Time: {end_time - start_time} seconds")
