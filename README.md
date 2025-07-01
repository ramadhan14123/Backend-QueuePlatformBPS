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




## API Reference

#### Register Guest & Create Visit

```http
  POST /api/guest/form
```

| Parameter         | Type         | Description                      |
|------------------|--------------|----------------------------------|
| `email`          | String(255)  | **Required**. Email tamu             |
| `guest_name`     | String(100)  | **Required**. Nama tamu              |
| `gender`         | Enum('L','P')| **Required**. Jenis kelamin (L/P)    |
| `identity_type`  | String(50)   | **Required**. Jenis identitas (KTP,NIP, dan lainnya)        |
| `identity_number`| String(50)   | **Required**. Nomor identitas        |
| `institution`    | String(100)  | **Required**. Instansi  asal             |
| `phone`          | String(20)   | **Required**. Nomor telepon          |

Contoh Request
```json
{
  "email": "user@email.com",
  "guest_name": "Nama Tamu",
  "gender": "L",
  "identity_type": "KTP",
  "identity_number": "123456789",
  "institution": "Nama Instansi",
  "phone": "08123456789",
  "purpose": "Keperluan",
  "target_service": "pelayanan statistik terpadu"
}
```

Contoh Response
```json
{
  "message": "Guest and visit created successfully",
  "guest_id": 1,
  "visit_id": 1,
  "queue_number": 1
}
```
----
#### MEMANGGIL SEMUA FUNGSI VISIT

```http
  GET /api/visit/visits
```
Contoh Response

```json
[
  {
    "visit_id": 1,
    "guest_id": 1,
    "purpose": "Keperluan",
    "target_service": "pelayanan statistik terpadu",
    "timestamp": "2024-06-10T10:00:00",
    "queue_number": 1,
    "mark": "hadir"
  }
  ...
]
```
#### CREATE VISIT

```http
  POST /api/visit/visits
```
| Parameter        | Tipe Data                       | Keterangan                                                                      |
| ---------------- | ------------------------------- | ------------------------------------------------------------------------------- |
| `visit_id`       | `int`                           | Primary key. ID unik untuk setiap kunjungan                                     |
| `guest_id`       | `int`                           | **Required.** ID tamu yang melakukan kunjungan (foreign key dari tabel `guest`) |
| `purpose`        | `Text`                 | **Required.** Keperluan kunjungan                                               |
| `target_service` | `string(100)`                   | **Required.** Tujuan layanan yang dituju                                        |
| `timestamp`      | `datetime`                      | Waktu kunjungan (otomatis terisi saat data dibuat)                              |
| `queue_number`   | `int`                           | Optional. Nomor antrian kunjungan                                               |
| `mark`           | `enum` ('hadir', 'tidak hadir') | Optional. Status kehadiran, default `tidak hadir`                               |

Contoh Request
```json
{
  "guest_id": 1,
  "purpose": "Keperluan",
  "target_service": "pelayanan statistik terpadu",
  "queue_number": 1,
  "mark": "hadir"
}
```

Contoh Response
```json
{
  "message": "Visit created",
  "visit_id": 2
}
```
#### UPDATE VISIT
```http
PUT /api/visit/visits/{visit_id}
```
| Parameter        | Type     | Description                                             |
| ---------------- | -------- | ------------------------------------------------------- |
| `visit_id`       | `int`    | **Required.** ID kunjungan (primary key)                |
| `mark`           | `enum` | Optional. Status kehadiran (`hadir` atau `tidak hadir`) |
| `purpose`        | `Text` | Optional. Keperluan kunjungan                           |
| `target_service` | `string(100)` | Optional. Tujuan layanan yang dituju                    |

Contoh Request
```json
{
  "mark": "hadir",
  "purpose": "Keperluan baru",
  "target_service": "pelayanan statistik terpadu"
}
```
Contoh Response
```json
{
  "message": "Visit updated",
  "visit_id": 1
}
```
#### MELIHAT VISIT MENGGUNAKAN KATEGORI
```http
GET /api/visit/category
```
Contoh Response
```json
{
  "Pelayanan Statistik Terpadu": [ ... ],
  "Kunjungan Dinas": [ ... ],
  "Lainnya": [ ... ]
}
```
- Membagi 3 kategori, untuk PST dan Kunjungan Dinas gunakan value ditentukan 
---
#### CS LOGIN
```http
POST /api/cs/login
```

| Parameter  | Type     | Description                               |
| ---------- | -------- | ----------------------------------------- |
| `admin`    | `string (100)` | **Required.** Username admin (harus unik) |
| `password` | `string (100)` | **Required.** Password admin              |

Contoh Request
```json
{
  "admin": "adminname",
  "password": "adminpass"
}
```
Contoh Response
```json
{
  "token": "JWT_TOKEN"
}
```
#### CS CONFIRM
```json
POST /api/cs/confirm
```
**Header:**
`Authorization: Bearer <JWT_TOKEN>`
| Parameter  | Type     | Description                               |
| ---------- | -------- | ----------------------------------------- |
| `visit_id`    | `int` | **Required.** Visit id |

Contoh Request
```json
{
  "visit_id": 1
}
```

Contoh Response
```json
{
  "message": "Visit confirmed successfully"
}
```
- Mark pada visit_id akan otomatis berubah ke `hadir`

#### CS RESET QUEUE NUMBER
```json
POST /api/cs/reset
```
**Header:** `Authorization: Bearer <JWT_TOKEN>`

Contoh Response
```json
{
  "message": "Queue number reset successfully"
}
```

#### CS MANUAL RESET DATABASE
```json
POST /api/cs/resetdb
```
**Header:** `Authorization: Bearer <JWT_TOKEN>`

Contoh Response
```json
{
  "message": "Database reset successfully, exported to visits_20240610_100000.xlsx"
}
```

#### CS MANUAL RESET COUNTDOWN
```json
GET /api/cs/reset-countdown
```
Contoh Response
```json
{
  "next_reset": "2024-06-17 00:00:00",
  "hours": 23,
  "minutes": 59,
  "seconds": 59,
  "raw": "6 days, 23:59:59"
}
```

#### CS GET LOGS
```json
GET /api/cs/actlogs
```
**Header:** `Authorization: Bearer <JWT_TOKEN>`

Contoh Response
```json
[
  {
    "log_id": 1,
    "admin_id": 1,
    "action": "Confirm Visit 1",
    "timestamp": "2024-06-10T10:00:00"
  }
]
```
---
#### EXPORT GUEST DATA
```json
GET /api/export/guest
```
**Response** : File Download `Excel`
#### EXPORT VISIT DATA
```json
GET /api/export/guest
```
**Response** : File Download `Excel`

#### EXPORT LOGS DATA
```json
GET /api/export/guest
```
**Response** : File Download `Excel`
## Catatan

- Endpoint yang membutuhkan autentikasi JWT harus mengirim header `Authorization: Bearer <JWT_TOKEN>`.
- Semua respons error akan diberikan dalam format `JSON` dengan field `error` dan/atau `message`.
