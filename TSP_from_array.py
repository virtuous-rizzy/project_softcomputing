import numpy as np
import random
import sys
import matplotlib
import matplotlib.pyplot as plt
import io
import base64

# Menggunakan backend 'Agg' agar tidak error saat dijalankan via Flask (headless)
matplotlib.use('Agg')

# -------------------------
# 1. Data Kota & Jarak
# -------------------------
cities = ["A", "B", "C", "D", "E"]

# Koordinat Kota (X, Y) untuk visualisasi
coords = {
    "A": (0, 0),
    "B": (2, 6),
    "C": (5, 3),
    "D": (8, 7),
    "E": (7, 0)
}

# Matriks Jarak (Sesuai soal awal)
dist_matriks = np.array([
    [0, 7, 5, 9, 9],
    [7, 0, 7, 2, 8],
    [5, 7, 0, 4, 3],
    [9, 2, 4, 0, 6],
    [9, 8, 3, 6, 0],
])

# -------------------------
# 2. Parameter Algoritma
# -------------------------
POP_SIZE = 100
GENERATIONS = 500
PM = 0.2
TOURNAMENT_K = 5
PC = 0.9
ELITE_SIZE = 1

if len(sys.argv) > 1:
    try:
        POP_SIZE = int(sys.argv[1])
        GENERATIONS = int(sys.argv[2])
        PM = float(sys.argv[3])
    except ValueError:
        pass

# -------------------------
# 3. Fungsi GA
# -------------------------
def route_distance(route):
    # Menghitung total jarak berdasarkan urutan index kota
    d = sum([dist_matriks[route[i], route[(i + 1) % len(route)]] for i in range(len(route))])
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
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[a : b + 1] = p1[a : b + 1]
    
    p2_idx = 0
    for i in range(size):
        if child[i] == -1:
            while p2[p2_idx] in child:
                p2_idx += 1
            child[i] = p2[p2_idx]
    return child

def swap_mutation(ind):
    a, b = random.sample(range(len(ind)), 2)
    ind[a], ind[b] = ind[b], ind[a]

# -------------------------
# 4. Main Loop
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
            print(f"Gen {g}: Best Distance = {best_dist}")

    # --- Output Teks ---
    best_route_names = [cities[i] for i in best]
    print("\n=== HASIL AKHIR ===")
    print("Rute terbaik:", " -> ".join(best_route_names + [best_route_names[0]]))
    print("Jarak total:", best_dist)

    # -------------------------
    # 5. Visualisasi (Plotting)
    # -------------------------
    
    # Urutkan koordinat berdasarkan rute terbaik
    x_coords = [coords[cities[i]][0] for i in best]
    y_coords = [coords[cities[i]][1] for i in best]
    
    # Tambahkan titik awal di akhir agar garis menutup (kembali ke awal)
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])

    plt.figure(figsize=(8, 5))
    
    # Gambar garis rute
    plt.plot(x_coords, y_coords, 'b-', marker='o', markersize=10, linewidth=2, label='Rute')
    
    # Gambar panah arah (opsional, agar terlihat urutannya)
    for i in range(len(best)):
        plt.annotate("", xy=(x_coords[i+1], y_coords[i+1]), xytext=(x_coords[i], y_coords[i]),
                     arrowprops=dict(arrowstyle="->", color='blue', lw=1.5))

    # Label Kota
    for city, (x, y) in coords.items():
        plt.text(x + 0.2, y + 0.2, city, fontsize=12, fontweight='bold', color='red')

    plt.title(f"Visualisasi Rute Terbaik TSP (Jarak: {best_dist})")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # --- Simpan ke Buffer (Bukan File Fisik) ---
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    
    # Encode ke Base64 string
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # --- Print Delimiter Khusus agar ditangkap Flask ---
    print("\n###IMAGE_START###")
    print(img_base64)