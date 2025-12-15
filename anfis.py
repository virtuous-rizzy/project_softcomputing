import numpy as np
import sys

# --------------------------------------------------------
# 1. Fungsi keanggotaan bell-shaped (generalized bell)
#   µ(x) = 1 / (1 + |(x - c) / a |^(2b))
# --------------------------------------------------------
def gbell_mf(x, a, b, c):
    # Menghindari pembagian dengan nol jika x == c
    if x == c:
        return 1.0
    return 1 / (1 + abs((x - c) / a) ** (2 * b))

# --------------------------------------------------------
# 2. Aturan Sugeno :
#   Rule 1: f1 = 0.1x + 0.1y + 0.1
#   Rule 2: f2 = 10x + 10y + 10
# --------------------------------------------------------
def f1(x, y):
    return 0.1 * x + 0.1 * y + 0.1

def f2(x, y):
    return 10 * x + 10 * y + 10

# --------------------------------------------------------
# 3. Hitung ANFIS untuk input (x, y)
# --------------------------------------------------------
def anfis(x, y):
    # Parameter premis (Sesuai contoh soal/hardcoded model)
    # Misal kita anggap parameter gbell untuk A1, B1, A2, B2 sudah fix
    # Namun di kode asli Anda, nilai miu (derajat keanggotaan) langsung diset angka.
    # Agar dinamis, sebaiknya nilai derajat keanggotaan dihitung, 
    # tapi karena codingan asli Anda menetapkan nilai fix untuk A1, B1 dll, 
    # saya akan tetap menggunakan logika asli Anda untuk struktur outputnya,
    # namun nilai x dan y akan mempengaruhi f1 dan f2.
    
    # Catatan: Dalam ANFIS sebenarnya, A1 dll adalah hasil fungsi keanggotaan gbell_mf(x,...)
    # Tapi mengikuti snippet Anda:
    A1 = 0.5
    B1 = 0.1
    A2 = 0.25
    B2 = 0.039

    # Layer 2 - firing strength
    w1 = A1 * B1
    w2 = A2 * B2

    # Normalisasi firing strength
    w_sum = w1 + w2
    # Hindari pembagian nol
    if w_sum == 0:
        W1 = 0
        W2 = 0
    else:
        W1 = w1 / w_sum
        W2 = w2 / w_sum

    # Layer 4 - weighted output (INI YANG BERUBAH SESUAI INPUT X, Y)
    out1 = W1 * f1(x, y)
    out2 = W2 * f2(x, y)

    # Layer 5 - output total
    output = out1 + out2

    return {
        "Input X": x, "Input Y": y,
        "A1": A1, "B1": B1,
        "A2": A2, "B2": B2,
        "w1 (Fire Strength 1)": w1, 
        "w2 (Fire Strength 2)": w2,
        "W1 (Norm. Strength 1)": W1, 
        "W2 (Norm. Strength 2)": W2,
        "out1 (Defuzzikasi 1)": out1, 
        "out2 (Defuzzikasi 2)": out2,
        "FINAL OUTPUT": output
    }

# --------------------------------------------------------
# 4. Main Execution (Menerima Argumen Sistem)
# --------------------------------------------------------
if __name__ == "__main__":
    # Default values jika tidak ada input
    x_val = 3.0
    y_val = 4.0

    # Cek apakah ada argumen dari command line (sys.argv)
    # Format: python anfis.py <x> <y>
    if len(sys.argv) > 2:
        try:
            x_val = float(sys.argv[1])
            y_val = float(sys.argv[2])
        except ValueError:
            print("Error: Input harus berupa angka.")
            sys.exit(1)

    print(f"--- ANFIS CALCULATION (x={x_val}, y={y_val}) ---\n")
    
    result = anfis(x_val, y_val)

    # Cetak hasil secara rapi
    print(f"{'PARAMETER':<25} {'VALUE':<15}")
    print("-" * 40)
    for k, v in result.items():
        if isinstance(v, float):
            print(f"{k:<25} = {v:.6f}")
        else:
            print(f"{k:<25} = {v}")