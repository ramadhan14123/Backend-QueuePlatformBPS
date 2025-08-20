# API DOCUMENTATION
Panduan menggunakan dan memanggil API pada backed queue platform BPS


## INSTALASI

1. Clone repository
```bash
git clone https://github.com/ramadhan14123/Backend-QueuePlatformBps.git
```
2. Buat Virtual Environment
- Membuat environment 
```bash
python -m venv env
```
- Aktivasi environment
``` bash
env\Script\activate
```
3. Install library dari requirements
```bash
pip install -r requirements.txt
```
4. Migrasi Database
- Inisialisasi Migration Folder
```bash
flask db init
```
- Generate Migration Script
```bash
flask db migrate -m "Inisialisasi Pertama"
```
- Apply Migration ke Database
```bash
flask db upgrade
```
5. Membuat Admin Database
Karena tidak ada fungsi register atau penambahan admin dari superuser(Admin Environment)
- Masuk ke flask shell
```bash
flask shell #harus sudah ada file .env
```
- Import yang dibutuhkan
```python
from app.extensions import db, bcrypt
from app.models.cs import CustomerService
```
- Hash password dan buat admin baru
```python
hashed_pw = bcrypt.generate_password_hash("admin123").decode('utf-8')
admin = CustomerService(admin="admin1", password=hashed_pw)
db.session.add(admin)
db.session.commit()
```

6. Menjalankan Server
```bash
python server.py
```