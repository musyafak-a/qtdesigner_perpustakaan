import pymysql
import pymysql.cursors
import hashlib
from datetime import date

# ─── KONFIGURASI KONEKSI MySQL ───────────────────────────────
# Sesuaikan dengan pengaturan MySQL / Laragon kamu
DB_CONFIG = {
    "host":        "localhost",
    "port":        3306,
    "user":        "root",
    "password":    "",           # kosong jika pakai Laragon/XAMPP default
    "database":    "perpustakaan",
    "charset":     "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,   # hasil query langsung dict
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ─── INIT DB (cek koneksi saja, tabel dibuat via .sql) ───────
def init_db():
    try:
        conn = get_connection()
        conn.close()
    except pymysql.Error as e:
        raise ConnectionError(
            f"Gagal terhubung ke MySQL!\n\n"
            f"Error: {e}\n\n"
            f"Pastikan:\n"
            f"  1. Laragon / MySQL sudah berjalan\n"
            f"  2. Database 'perpustakaan' sudah dibuat\n"
            f"  3. Konfigurasi DB_CONFIG di database.py sudah benar"
        )


# ─── USER ────────────────────────────────────────────────────
def login_user(email, password):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, hash_password(password))
        )
        row = cur.fetchone()
    conn.close()
    return row  # sudah dict karena DictCursor


def register_user(username, email, password, gender, tanggal_lahir):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (username, email, password, gender, tanggal_lahir, role)
                VALUES (%s, %s, %s, %s, %s, 'visitor')
                """,
                (username, email, hash_password(password), gender, tanggal_lahir)
            )
        conn.commit()
        conn.close()
        return True, "Registrasi berhasil!"
    except pymysql.IntegrityError as e:
        if "username" in str(e).lower():
            return False, "Username sudah digunakan."
        return False, "Email sudah terdaftar."


def get_all_visitors():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, username, email, gender, tanggal_lahir, created_at "
            "FROM users WHERE role = 'visitor'"
        )
        rows = cur.fetchall()
    conn.close()
    return rows


def delete_visitor(user_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM users WHERE id = %s AND role = 'visitor'",
            (user_id,)
        )
    conn.commit()
    conn.close()


# ─── BUKU ────────────────────────────────────────────────────
def get_all_buku():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM buku ORDER BY id")
        rows = cur.fetchall()
    conn.close()
    return rows


def get_buku_tersedia():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM buku WHERE stok > 0 ORDER BY id")
        rows = cur.fetchall()
    conn.close()
    return rows


def tambah_buku(kode, nama, penulis, genre, stok):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO buku (kode_buku, nama_buku, penulis, genre, stok)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (kode, nama, penulis, genre, stok)
            )
        conn.commit()
        conn.close()
        return True, "Buku berhasil ditambahkan!"
    except pymysql.IntegrityError:
        return False, "Kode buku sudah ada."


def update_buku(buku_id, kode, nama, penulis, genre, stok):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE buku
            SET kode_buku = %s, nama_buku = %s, penulis = %s, genre = %s, stok = %s
            WHERE id = %s
            """,
            (kode, nama, penulis, genre, stok, buku_id)
        )
    conn.commit()
    conn.close()


def delete_buku(buku_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM buku WHERE id = %s", (buku_id,))
    conn.commit()
    conn.close()


# ─── PEMINJAMAN ──────────────────────────────────────────────
def get_all_peminjaman():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.id, u.username, b.nama_buku, b.kode_buku,
                   p.tgl_pinjam, p.tgl_kembali, p.status
            FROM peminjaman p
            JOIN users u ON p.user_id = u.id
            JOIN buku  b ON p.buku_id = b.id
            ORDER BY p.id DESC
            """
        )
        rows = cur.fetchall()
    conn.close()
    return rows


def get_peminjaman_by_user(user_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.id, b.kode_buku, b.nama_buku, b.penulis, b.genre,
                   p.tgl_pinjam, p.tgl_kembali, p.status
            FROM peminjaman p
            JOIN buku b ON p.buku_id = b.id
            WHERE p.user_id = %s
            ORDER BY p.id DESC
            """,
            (user_id,)
        )
        rows = cur.fetchall()
    conn.close()
    return rows


def get_peminjaman_aktif_by_user(user_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.id, b.kode_buku, b.nama_buku, p.tgl_pinjam
            FROM peminjaman p
            JOIN buku b ON p.buku_id = b.id
            WHERE p.user_id = %s AND p.status = 'dipinjam'
            ORDER BY p.id DESC
            """,
            (user_id,)
        )
        rows = cur.fetchall()
    conn.close()
    return rows


def pinjam_buku(user_id, buku_id, tgl_kembali):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT stok FROM buku WHERE id = %s", (buku_id,))
        row = cur.fetchone()
        if not row or row["stok"] < 1:
            conn.close()
            return False, "Stok buku tidak tersedia."
        cur.execute(
            """
            INSERT INTO peminjaman (user_id, buku_id, tgl_pinjam, tgl_kembali, status)
            VALUES (%s, %s, %s, %s, 'dipinjam')
            """,
            (user_id, buku_id, str(date.today()), tgl_kembali)
        )
        cur.execute("UPDATE buku SET stok = stok - 1 WHERE id = %s", (buku_id,))
    conn.commit()
    conn.close()
    return True, "Buku berhasil dipinjam!"


def kembalikan_buku(pinjam_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT buku_id, status FROM peminjaman WHERE id = %s",
            (pinjam_id,)
        )
        row = cur.fetchone()
        if not row:
            conn.close()
            return False, "Data tidak ditemukan."
        if row["status"] == "dikembalikan":
            conn.close()
            return False, "Buku sudah dikembalikan."
        cur.execute(
            "UPDATE peminjaman SET status = 'dikembalikan', tgl_kembali = %s WHERE id = %s",
            (str(date.today()), pinjam_id)
        )
        cur.execute("UPDATE buku SET stok = stok + 1 WHERE id = %s", (row["buku_id"],))
    conn.commit()
    conn.close()
    return True, "Buku berhasil dikembalikan!"


def update_status_pinjam(pinjam_id, status):
    conn = get_connection()
    with conn.cursor() as cur:
        if status == "dikembalikan":
            cur.execute(
                "SELECT buku_id, status FROM peminjaman WHERE id = %s",
                (pinjam_id,)
            )
            row = cur.fetchone()
            if row and row["status"] == "dipinjam":
                cur.execute(
                    "UPDATE buku SET stok = stok + 1 WHERE id = %s",
                    (row["buku_id"],)
                )
        cur.execute(
            "UPDATE peminjaman SET status = %s WHERE id = %s",
            (status, pinjam_id)
        )
    conn.commit()
    conn.close()