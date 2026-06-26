import sqlite3
import hashlib
from datetime import date

DB_NAME = "perpustakaan.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Tabel users (admin & visitor)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            gender TEXT CHECK(gender IN ('laki-laki', 'perempuan')),
            tanggal_lahir TEXT,
            role TEXT DEFAULT 'visitor' CHECK(role IN ('admin', 'visitor')),
            created_at TEXT DEFAULT (date('now'))
        )
    """)

    # Tabel buku
    cur.execute("""
        CREATE TABLE IF NOT EXISTS buku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode_buku TEXT UNIQUE NOT NULL,
            nama_buku TEXT NOT NULL,
            penulis TEXT NOT NULL,
            genre TEXT NOT NULL,
            stok INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (date('now'))
        )
    """)

    # Tabel peminjaman
    cur.execute("""
        CREATE TABLE IF NOT EXISTS peminjaman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            buku_id INTEGER NOT NULL,
            tgl_pinjam TEXT NOT NULL,
            tgl_kembali TEXT,
            status TEXT DEFAULT 'dipinjam' CHECK(status IN ('dipinjam', 'dikembalikan')),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (buku_id) REFERENCES buku(id)
        )
    """)

    # Seed admin default
    cur.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO users (username, email, password, gender, tanggal_lahir, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("admin", "admin@perpus.com", hash_password("admin123"), "laki-laki", "2000-01-01", "admin"))

    # Seed beberapa buku contoh
    cur.execute("SELECT COUNT(*) FROM buku")
    if cur.fetchone()[0] == 0:
        buku_data = [
            ("BK001", "Laskar Pelangi", "Andrea Hirata", "Novel", 3),
            ("BK002", "Bumi Manusia", "Pramoedya Ananta Toer", "Sejarah", 2),
            ("BK003", "Filosofi Teras", "Henry Manampiring", "Filsafat", 4),
            ("BK004", "Atomic Habits", "James Clear", "Self-Help", 2),
            ("BK005", "Negeri 5 Menara", "A. Fuadi", "Novel", 3),
        ]
        cur.executemany("""
            INSERT INTO buku (kode_buku, nama_buku, penulis, genre, stok)
            VALUES (?, ?, ?, ?, ?)
        """, buku_data)

    conn.commit()
    conn.close()

# ─── USER ───────────────────────────────────────────────
def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hash_password(password)))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def register_user(username, email, password, gender, tanggal_lahir):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, email, password, gender, tanggal_lahir, role)
            VALUES (?, ?, ?, ?, ?, 'visitor')
        """, (username, email, hash_password(password), gender, tanggal_lahir))
        conn.commit()
        conn.close()
        return True, "Registrasi berhasil!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username sudah digunakan."
        return False, "Email sudah terdaftar."

def get_all_visitors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, gender, tanggal_lahir, created_at FROM users WHERE role='visitor'")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def delete_visitor(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=? AND role='visitor'", (user_id,))
    conn.commit()
    conn.close()

# ─── BUKU ────────────────────────────────────────────────
def get_all_buku():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM buku ORDER BY id")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def get_buku_tersedia():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM buku WHERE stok > 0 ORDER BY id")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def tambah_buku(kode, nama, penulis, genre, stok):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO buku (kode_buku, nama_buku, penulis, genre, stok)
            VALUES (?, ?, ?, ?, ?)
        """, (kode, nama, penulis, genre, stok))
        conn.commit()
        conn.close()
        return True, "Buku berhasil ditambahkan!"
    except sqlite3.IntegrityError:
        return False, "Kode buku sudah ada."

def update_buku(buku_id, kode, nama, penulis, genre, stok):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE buku SET kode_buku=?, nama_buku=?, penulis=?, genre=?, stok=?
        WHERE id=?
    """, (kode, nama, penulis, genre, stok, buku_id))
    conn.commit()
    conn.close()

def delete_buku(buku_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM buku WHERE id=?", (buku_id,))
    conn.commit()
    conn.close()

# ─── PEMINJAMAN ──────────────────────────────────────────
def get_all_peminjaman():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, u.username, b.nama_buku, b.kode_buku,
               p.tgl_pinjam, p.tgl_kembali, p.status
        FROM peminjaman p
        JOIN users u ON p.user_id = u.id
        JOIN buku b ON p.buku_id = b.id
        ORDER BY p.id DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def get_peminjaman_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, b.kode_buku, b.nama_buku, b.penulis, b.genre,
               p.tgl_pinjam, p.tgl_kembali, p.status
        FROM peminjaman p
        JOIN buku b ON p.buku_id = b.id
        WHERE p.user_id = ?
        ORDER BY p.id DESC
    """, (user_id,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def get_peminjaman_aktif_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, b.kode_buku, b.nama_buku, p.tgl_pinjam
        FROM peminjaman p
        JOIN buku b ON p.buku_id = b.id
        WHERE p.user_id = ? AND p.status='dipinjam'
        ORDER BY p.id DESC
    """, (user_id,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def pinjam_buku(user_id, buku_id, tgl_kembali):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT stok FROM buku WHERE id=?", (buku_id,))
    row = cur.fetchone()
    if not row or row["stok"] < 1:
        conn.close()
        return False, "Stok buku tidak tersedia."
    cur.execute("""
        INSERT INTO peminjaman (user_id, buku_id, tgl_pinjam, tgl_kembali, status)
        VALUES (?, ?, ?, ?, 'dipinjam')
    """, (user_id, buku_id, str(date.today()), tgl_kembali))
    cur.execute("UPDATE buku SET stok = stok - 1 WHERE id=?", (buku_id,))
    conn.commit()
    conn.close()
    return True, "Buku berhasil dipinjam!"

def kembalikan_buku(pinjam_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT buku_id, status FROM peminjaman WHERE id=?", (pinjam_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False, "Data tidak ditemukan."
    if row["status"] == "dikembalikan":
        conn.close()
        return False, "Buku sudah dikembalikan."
    cur.execute("UPDATE peminjaman SET status='dikembalikan', tgl_kembali=? WHERE id=?",
                (str(date.today()), pinjam_id))
    cur.execute("UPDATE buku SET stok = stok + 1 WHERE id=?", (row["buku_id"],))
    conn.commit()
    conn.close()
    return True, "Buku berhasil dikembalikan!"

def update_status_pinjam(pinjam_id, status):
    conn = get_connection()
    cur = conn.cursor()
    if status == "dikembalikan":
        cur.execute("SELECT buku_id, status FROM peminjaman WHERE id=?", (pinjam_id,))
        row = cur.fetchone()
        if row and row["status"] == "dipinjam":
            cur.execute("UPDATE buku SET stok = stok + 1 WHERE id=?", (row["buku_id"],))
    cur.execute("UPDATE peminjaman SET status=? WHERE id=?", (status, pinjam_id))
    conn.commit()
    conn.close()
