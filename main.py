from flask import Flask, render_template, session, request, redirect, url_for
from sklearn.metrics import accuracy_score, classification_report
import pickle

app = Flask(__name__)
app.secret_key = "secret key"

@app.route("/")
def index():
    return render_template("index.html", title="index")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form["name"]
        session["phone"] = request.form["phone"]
        session["address"] = request.form["address"]
        return redirect(url_for("classify"))
    return render_template("login.html", title="login")

@app.route("/classify", methods=["GET", "POST"])
def classify():
    if not session:
        return redirect(url_for("index"))
    if request.method == "POST":
        symptom_values = [int(request.form.get(symptom, '0')) for symptom in [
            "Pertumbuhan Tanaman Yang Tidak Normal",
            "Daun Berubah Warna Menjadi Hijau Pucat",
            "Tanaman Menjadi Lemah Dan Terjadi Nekrosis",
            "Daun Yang Terdapat Bercak Bercak Lonjong Berwarna Kuning",
            "Daun Berubah Warna Dari Hijau Menjadi Kuning",
            "Pertumbuhan Menjadi Kerdil",
            "Pangkal Batang Menghitam",
            "Pelepah Kecil Kecil Sobek Atau Tidak Ada Sama Sekali",
            "Pelepah Banyak Yang Patah Dan Menggantung Pada Batang",
            "Terdapat Getah Atau Lendir Yang Keluar Pada Batang Sawit Yang Terinfeksi Jamur Ganoderma",
            "Tanaman Menjadi Kuncup Melengkung",
            "Daun Bercak Bercak Kuning Ditengah Daun terdapat Bercak Berwarna Coklat",
            "Terlihat Adanya Warna Coklat Pada Ujung Daun",
            "Adanya Rizomorf Jamur Berwarna Putih Pada Permukaan Buah",
            "Tandan Buah Rusak Atau Membusuk",
            "Daun Tajuk Yang Tumbuh Lebih kecil Bukan Tambah Besar"
        ]]

        with open("ml.pkl", "rb") as f:
            model = pickle.load(f)
            result = model.predict([symptom_values])[0]
        
        return redirect(url_for("result", result=result))
    return render_template("classify.html", title="klasifikasi")

@app.route("/result/<string:result>")
def result(result):
    nama = {
        "busuk pangkal batang": {
            "explanation": "Penyakit busuk pangkal batang disebabkan oleh jamur Phytophthora capsici.",
            "sample_image": "https://example.com/rust-image.jpg",
            "indonesian_name": "busuk pangkal batang",
            "solution": "1. Menjaga kebersihan kebun dari sisa-sisa tanaman.\n2. Menggunakan fungisida yang sesuai.\n3. Melakukan sanitasi dan pembersihan batang yang terinfeksi."
        },
        "busuk kuncup": {
            "explanation": "Busuk kuncup disebabkan oleh cendawan Choanosearum sp.",
            "sample_image": "https://example.com/blight-image.jpg",
            "indonesian_name": "busuk kuncup",
            "solution": "1. Memotong dan membakar bagian tanaman yang terinfeksi.\n2. Menggunakan fungisida yang efektif.\n3. Meningkatkan sirkulasi udara di sekitar tanaman."
        },
        "anthracnose": {
            "explanation": "Antraknosa adalah jenis penyakit tumbuhan yang ditemukan pada berbagai tanaman pohon dan semak, awal gejala yang ditunjukan berupa bercak pada daun atau bagian lain berbentuk bulat panjang berwana hitam yang akan berlanjut hingga kematian jaringan..",
            "sample_image": "https://example.com/powdery-mildew-image.jpg",
            "indonesian_name": "bercak daun",
            "solution": "1. Membuang dan menghancurkan daun yang terinfeksi.\n2. Menggunakan fungisida yang sesuai.\n3. Menjaga kebersihan lingkungan sekitar tanaman."
        },
        "daun mengecil": {
            "explanation": "daun mengecil disebabkan karena adanya masalah perakaran.",
            "sample_image": "https://example.com/downy-mildew-image.jpg",
            "indonesian_name": "daun mengecil",
            "solution": "1. Memperbaiki sistem drainase di sekitar tanaman.\n2. Menggunakan pupuk yang seimbang.\n3. Memastikan pasokan air yang cukup."
        },
        "busuk buah": {
            "explanation": "busuk buah disebabkan karena kelembapan udara, curah hujan dan cara bercocok tanam.",
            "sample_image": "https://example.com/leaf-spot-image.jpg",
            "indonesian_name": "busuk buah",
            "solution": "1. Mengatur jarak tanam yang ideal untuk sirkulasi udara.\n2. Menggunakan fungisida yang efektif.\n3. Memanen buah secara tepat waktu."
        },
        "garis kuning": {
            "explanation": "Penyakit ini disebut juga sebagai penyakit fusarium karena disebabkan oleh jamur Fusarium Oxiysporum.",
            "sample_image": "https://example.com/leaf-spot-image.jpg",
            "indonesian_name": "garis kuning",
            "solution": "1. Menggunakan varietas tanaman yang tahan penyakit.\n2. Menggunakan fungisida sistemik.\n3. Menjaga kebersihan lingkungan sekitar tanaman."
        },
        "tajuk": {
            "explanation": "Penyakit tajuk atau penyakit Crown disease adalah penyakit pada tanaman kelapa sawit yang disebabkan oleh gen keturunan tanaman induk.",
            "sample_image": "https://example.com/leaf-spot-image.jpg",
            "indonesian_name": "tajuk",
            "solution": "1. Memilih bibit yang bebas penyakit.\n2. Melakukan pemangkasan secara teratur.\n3. Menggunakan pupuk yang sesuai."
        },
        "busuk akar sawit": {
            "explanation": "Penyakit akar atau disebut juga Blast disease disebabkan oleh cendawan/jamur Rhizoctonia lamellifera dan Phytium sp.",
            "sample_image": "https://example.com/leaf-spot-image.jpg",
            "indonesian_name": "busuk akar sawit",
            "solution": "1. Meningkatkan sistem drainase kebun.\n2. Menggunakan fungisida sistemik.\n3. Melakukan sanitasi kebun secara berkala."
        }
        
    }
    with open("ml.pkl", "rb") as f:
        model = pickle.load(f)
        metrics = pickle.load(f)
    return render_template("result.html",title="Hasil",result=nama[result],metrics=metrics)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
