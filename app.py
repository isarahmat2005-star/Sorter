from flask import Flask, render_template, request, jsonify
import os
import shutil

app = Flask(__name__)

@app.route('/')
def home():
    # Ini akan memanggil desain HTML kamu
    return render_template('index.html')

@app.route('/proses_file', methods=['POST'])
def proses_file():
    data = request.json
    folder_sumber = data.get('source')
    folder_tujuan = data.get('destination')
    max_size_mb = float(data.get('maxSize', 0))
    
    # Validasi folder
    if not os.path.exists(folder_sumber):
        return jsonify({"status": "error", "pesan": "Folder sumber tidak ditemukan!"})
    if not os.path.exists(folder_tujuan):
        os.makedirs(folder_tujuan) # Buat folder tujuan jika belum ada

    berhasil_dipindah = 0
    
    try:
        # Pindai file di folder sumber
        for filename in os.listdir(folder_sumber):
            filepath = os.path.join(folder_sumber, filename)
            
            if os.path.isfile(filepath):
                # Cek ukuran file dalam MB
                ukuran_mb = os.path.getsize(filepath) / (1024 * 1024)
                
                # Logika penyortiran (Bisa dikembangkan nanti untuk resolusi/ekstensi)
                if ukuran_mb > max_size_mb:
                    shutil.move(filepath, os.path.join(folder_tujuan, filename))
                    berhasil_dipindah += 1
                    
        return jsonify({
            "status": "success", 
            "pesan": f"{berhasil_dipindah} file berhasil dipindahkan ke {folder_tujuan}"
        })
    except Exception as e:
        return jsonify({"status": "error", "pesan": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
