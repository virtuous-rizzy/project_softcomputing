import numpy as np
import pandas as pd
import random
import sys  

# -------------------------
# 1. Baca Matriks Jarak
# -------------------------
cities = ["A", "B", "C", "D", "E"]

dist_matriks = np.array(
    [
        [0, 7, 5, 9, 9],
        [7, 0, 7, 2, 8],
        [5, 7, 0, 4, 3],
        [9, 2, 4, 0, 6],
        [9, 8, 3, 6, 0],
    ]
)

# -------------------------
# 2. Parameter Algoritma (DINAMIS)
# -------------------------
# Default values
POP_SIZE = 100
GENERATIONS = 500
PM = 0.2  # Probabilitas Mutasi
TOURNAMENT_K = 5
PC = 0.9  # Probabilitas Crossover
ELITE_SIZE = 1

if len(sys.argv) > 1:
    try:
        POP_SIZE = int(sys.argv[1])
        GENERATIONS = int(sys.argv[2])
        PM = float(sys.argv[3])
    except ValueError:
        pass

# -------------------------
# 3. Fungsi bantu
# -------------------------
def route_distance(route):
    d = sum(
        [dist_matriks[route[i], route[(i + 1) % len(route)]] for i in range(len(route))]
    )
    return d

def create_individual(n):
    ind = list(range(n))
    random.shuffle(ind)
    return ind

def initial_population(size, n):
    return [create_individual(n) for _ in range(size)]

def tournament_selection(pop):
    k = random.sample(pop, TOURNAMENT_K)
    return min(k, key=lambda ind: route_distance(ind))

def ordered_crossover(p1, p2):
    a, b = sorted(random.sample(range(len(p1)), 2))
    child = [-1] * len(p1)
    child[a : b + 1] = p1[a : b + 1]
    p2_idx = 0
    for i in range(len(p1)):
        if child[i] == -1:
            while p2[p2_idx] in child:
                p2_idx += 1
            child[i] = p2[p2_idx]
    return child

def swap_mutation(ind):
    a, b = random.sample(range(len(ind)), 2)
    ind[a], ind[b] = ind[b], ind[a]

# -------------------------
# 4. Main GA Loop
# -------------------------
if __name__ == "__main__":
    print(f"--- Parameter: Populasi={POP_SIZE}, Generasi={GENERATIONS}, Mutasi Rate={PM} ---\n")

    pop = initial_population(POP_SIZE, len(cities))
    best = min(pop, key=lambda ind: route_distance(ind))
    best_dist = route_distance(best)
    
    for g in range(GENERATIONS):
        new_pop = []
        pop = sorted(pop, key=lambda ind: route_distance(ind))

        if route_distance(pop[0]) < best_dist:
            best = pop[0]
            best_dist = route_distance(best)

        new_pop.extend(pop[:ELITE_SIZE])

        while len(new_pop) < POP_SIZE:
            p1 = tournament_selection(pop)
            p2 = tournament_selection(pop)
            child = ordered_crossover(p1, p2) if random.random() < PC else p1[:]
            if random.random() < PM:
                swap_mutation(child)
            new_pop.append(child)
        pop = new_pop
        
        log_interval = max(1, GENERATIONS // 10)
        if g % log_interval == 0:
            print(f"Gen {g}: Best Distance = {best_dist:.4f}")

    # -------------------------
    # 5. Output Hasil
    # -------------------------
    best_route = [cities[i] for i in best]
    print("\n=== HASIL AKHIR ===")
    print("Rute terbaik:", " -> ".join(best_route + [best_route[0]]))
    print("Jarak total:", best_dist)

    # --- MODIFIKASI UNTUK DOWNLOAD BROWSER ---
    print("\n###CSV_START###") 
    print(pd.DataFrame({"city": best_route}).to_csv(index=False))