from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
import qrcode
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret-key'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
QR_FOLDER = os.path.join(BASE_DIR, 'qr_codes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        country_code = request.form.get('country_code')
        phone = request.form.get('phone')
        email = request.form.get('email')
        major = request.form.get('major')
        stage = request.form.get('stage')
        university_type = request.form.get('university_type')
        mother_name = request.form.get('mother_name')
        # استقبال الملفات المنفصلة
        personal_photo = request.files.get('personal_photo')
        passport = request.files.get('passport')
        certificate = request.files.get('certificate')

        # حفظ كل ملف إذا تم رفعه
        saved_files = []
        if personal_photo and personal_photo.filename:
            filename = secure_filename(f"personal_{name}_{phone}_" + personal_photo.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            personal_photo.save(file_path)
            saved_files.append(filename)
        if passport and passport.filename:
            filename = secure_filename(f"passport_{name}_{phone}_" + passport.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            passport.save(file_path)
            saved_files.append(filename)
        if certificate and certificate.filename:
            filename = secure_filename(f"certificate_{name}_{phone}_" + certificate.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            certificate.save(file_path)
            saved_files.append(filename)

        qr_data = f"الاسم: {name}\nرقم الهاتف: +{country_code}{phone}\nالبريد: {email}\nالتخصص: {major}\nالمرحلة: {stage}\nنوع الجامعة: {university_type}\nاسم الأم: {mother_name}"
        qr_img = qrcode.make(qr_data)
        qr_filename = f"qr_{name}_{phone}.png"
        qr_path = os.path.join(QR_FOLDER, qr_filename)
        with open(qr_path, 'wb') as f:
            qr_img.save(f)

        return redirect(url_for('success', qr_filename=qr_filename))
    return render_template('index.html')

@app.route('/success')
def success():
    qr_filename = request.args.get('qr_filename')
    return render_template('success.html', qr_filename=qr_filename)

@app.route('/download_qr/<qr_filename>')
def download_qr(qr_filename):
    qr_path = os.path.join(QR_FOLDER, qr_filename)
    return send_file(qr_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
