from flask import Flask, render_template, request
import subprocess
import sys
import os

app = Flask(__name__)


@app.route("/")
def home():
    daftar_tugas = [
        {"nomor": 1, "deskripsi": "Pengenalan Soft Computing"},
        {"nomor": 2, "deskripsi": "Algoritma Genetika – Knapsack Problem"},
        {
            "nomor": 3,
            "deskripsi": "Algoritma Genetika - Traveling Salesperson Problem (TSP)",
        },
        {"nomor": 4, "deskripsi": "Coming soon"},
        {"nomor": 5, "deskripsi": "Coming soon"},
    ]
    nama_mahasiswa = "MUHAMMAD RIZKY AKBAR"
    nim_mahasiswa = "2411016310005"
    return render_template(
        "index.html", daftar_tugas=daftar_tugas, nama=nama_mahasiswa, nim=nim_mahasiswa
    )


# --- TUGAS 2 ---
@app.route("/tugas/2")
def tugas2():
    show_toast = True if "kapasitas" in request.args else False
    kapasitas = request.args.get("kapasitas", "15")
    populasi = request.args.get("populasi", "10")
    generasi = request.args.get("generasi", "10")

    script_path = os.path.join(app.root_path, "knapsack.py")
    if not os.path.exists(script_path):
        return f"<h3>Error: File 'knapsack.py' tidak ditemukan.</h3>"

    result = subprocess.run(
        [sys.executable, script_path, kapasitas, populasi, generasi],
        capture_output=True,
        text=True,
    )

    output = result.stdout
    kode_konten = ""
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            kode_konten = f.read()
    except Exception:
        kode_konten = "Gagal baca file."

    return render_template(
        "tugas2.html",
        output=output,
        kode=kode_konten,
        kap_val=kapasitas,
        pop_val=populasi,
        gen_val=generasi,
        show_toast=show_toast,
    )


# --- TUGAS 3: TSP (Update Visualisasi) ---
@app.route("/tugas/3")
def tugas3():
    show_toast = True if "populasi" in request.args else False

    populasi = request.args.get("populasi", "100")
    generasi = request.args.get("generasi", "500")
    mutasi = request.args.get("mutasi", "0.2")

    filename = "TSP_from_array.py"
    script_path = os.path.join(app.root_path, filename)

    if not os.path.exists(script_path):
        return "ERROR: File TSP_from_array.py tidak ditemukan."

    # Jalankan script python
    result = subprocess.run(
        [sys.executable, script_path, populasi, generasi, mutasi],
        capture_output=True,
        text=True,
    )

    raw_output = result.stdout
    if result.stderr:
        raw_output += "\nERROR:\n" + result.stderr

    output_text = raw_output
    image_data = None  # Default kosong

    # --- LOGIKA PARSING GAMBAR ---
    if "###IMAGE_START###" in raw_output:
        parts = raw_output.split("###IMAGE_START###")
        output_text = parts[0]  # Teks Log Algoritma
        image_data = parts[1].strip()  # String Base64 Gambar
    # -----------------------------

    # Baca source code untuk ditampilkan
    kode_konten = ""
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            kode_konten = f.read()
    except Exception:
        kode_konten = "Gagal baca file."

    return render_template(
        "tugas3.html",
        output=output_text,
        image_data=image_data,  # Kirim data gambar ke HTML
        kode=kode_konten,
        pop_val=populasi,
        gen_val=generasi,
        mut_val=mutasi,
        show_toast=show_toast,
    )


@app.route("/tugas/<int:num>")
def tugas(num):
    return render_template(f"tugas{num}.html")

if __name__ == "__main__":
    app.run(debug=True)
