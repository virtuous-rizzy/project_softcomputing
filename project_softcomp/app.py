from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    daftar_tugas = [
        {"nomor": 1, "deskripsi": "Pengenalan Soft Computing"},
        {"nomor": 2, "deskripsi": "Coming soon"},
        {"nomor": 3, "deskripsi": "Coming soon"},
        {"nomor": 4, "deskripsi": "Coming soon"},
        {"nomor": 5, "deskripsi": "Coming soon"},
    ]
    return render_template('index.html', daftar_tugas=daftar_tugas)

@app.route('/tugas/<int:num>')
def tugas(num):
    return render_template(f'tugas{num}.html')

if __name__ == '__main__':
    app.run(debug=True)
