
Claude finished the response

1782483114022_kelola_buku.ui
ui


1782483114024_kelola_pinjam.ui
ui


1782483114025_kelola_visitor.ui
ui


1782483114026_login.ui
ui


1782483114028_menu(admin).ui
ui


1782483114029_register.ui
ui


1782483114018_styles.py
213 lines

py


1782483114019_auth_window.py
296 lines

py


1782483114021_database.py
265 lines

py

tadi kan aku sudah prompt ini diakun lain
tolong buatkan proyek aplikasi dengan qt designer python yaitu aplikasi manajemen peminjaman buku perpustakaan dengan ui dan fungsi-fungsi admin seperti ini, buatkan dari databasenya juga menyesuaikan dengan fungsi dan kolom yang ada di ui dan kebutuhan sistem. dan berikut halaman yanga ada di admin dan membernya user(admin, visitor) halaman login, admin: halaman menu, kelola buku, kelola visitor, kelola pinjam visitor: lihat buku, lihat peminjaman, lakukan pinjam, lihat history pinjam
untuk tampilannya memakai color pallate 
#607456(primer gelap), 
#EEE0CC (background), 
#7B2525(sekunder), 
#BA6A4C (tersier)

lanjutkan progres ini sekarang

21:05

Viewed a file, ran a command
Viewed a file, ran a command
Sekarang saya sudah punya semua info yang dibutuhkan. Mari buat semua file Python lengkap. Saya akan buat: main.py, admin_window.py, dan visitor_window.py berdasarkan UI files dan kode yang sudah ada.


Created 3 files, ran a command
Created 3 files, ran a command

Copy existing files to working directory
bash

cp /mnt/user-data/uploads/1782483114018_styles.py /home/claude/styles.py
cp /mnt/user-data/uploads/1782483114019_auth_window.py /home/claude/auth_window.py
cp /mnt/user-data/uploads/1782483114021_database.py /home/claude/database.py
echo "Files copied"
Output

Files copied

Main entry point
main.py

Admin window with sidebar navigation - kelola buku, visitor, pinjam
admin_window.py

Visitor window - lihat buku, pinjam, lihat peminjaman, history
visitor_window.py
Done

You are out of free messages until 2:00 AM




Claude is AI and can make mistakes. Please double-check responses.
Visitor window · PY
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QGridLayout, QComboBox, QDateEdit,
    QAbstractItemView, QStackedWidget, QLineEdit
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import database as db
 
 
def make_table(headers):
    tbl = QTableWidget()
    tbl.setColumnCount(len(headers))
    tbl.setHorizontalHeaderLabels(headers)
    tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
    tbl.setAlternatingRowColors(True)
    tbl.horizontalHeader().setStretchLastSection(True)
    tbl.verticalHeader().setVisible(False)
    return tbl
 
 
def cell(text):
    item = QTableWidgetItem(str(text) if text is not None else "")
    item.setTextAlignment(Qt.AlignCenter)
    return item
 
 
# ──────────────────────────────────────────────────────
#  Dialog Pinjam Buku
# ──────────────────────────────────────────────────────
class DialogPinjam(QDialog):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("Pinjam Buku")
        self.setFixedSize(400, 280)
        self._build()
 
    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)
 
        title = QLabel("📖  PINJAM BUKU")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
 
        grid = QGridLayout()
        grid.setSpacing(8)
 
        def lbl(t):
            l = QLabel(t)
            l.setFont(QFont("Segoe UI", 9, QFont.Bold))
            return l
 
        self.cmb_buku = QComboBox()
        self.buku_list = db.get_buku_tersedia()
        if not self.buku_list:
            self.cmb_buku.addItem("— Tidak ada buku tersedia —")
        else:
            for b in self.buku_list:
                self.cmb_buku.addItem(f"{b['kode_buku']} — {b['nama_buku']} (stok: {b['stok']})")
 
        self.inp_tgl_kembali = QDateEdit()
        self.inp_tgl_kembali.setCalendarPopup(True)
        self.inp_tgl_kembali.setMinimumDate(QDate.currentDate().addDays(1))
        self.inp_tgl_kembali.setDate(QDate.currentDate().addDays(7))
        self.inp_tgl_kembali.setDisplayFormat("dd-MM-yyyy")
 
        grid.addWidget(lbl("Pilih Buku :"), 0, 0)
        grid.addWidget(self.cmb_buku, 0, 1)
        grid.addWidget(lbl("Tgl Kembali :"), 1, 0)
        grid.addWidget(self.inp_tgl_kembali, 1, 1)
 
        layout.addLayout(grid)
        layout.addSpacing(8)
 
        btn_row = QHBoxLayout()
        btn_pinjam = QPushButton("📖  PINJAM")
        btn_pinjam.setFixedHeight(38)
        btn_pinjam.clicked.connect(self.do_pinjam)
        btn_batal = QPushButton("✖  BATAL")
        btn_batal.setObjectName("btn_secondary")
        btn_batal.setFixedHeight(38)
        btn_batal.clicked.connect(self.reject)
        btn_row.addWidget(btn_pinjam)
        btn_row.addWidget(btn_batal)
        layout.addLayout(btn_row)
 
    def do_pinjam(self):
        if not self.buku_list:
            QMessageBox.warning(self, "Info", "Tidak ada buku tersedia.")
            return
        idx = self.cmb_buku.currentIndex()
        buku = self.buku_list[idx]
        tgl_kembali = self.inp_tgl_kembali.date().toString("yyyy-MM-dd")
        ok, msg = db.pinjam_buku(self.user_id, buku["id"], tgl_kembali)
        if ok:
            QMessageBox.information(self, "Sukses", msg)
            self.accept()
        else:
            QMessageBox.critical(self, "Gagal", msg)
 
 
# ──────────────────────────────────────────────────────
#  Panel Lihat Buku
# ──────────────────────────────────────────────────────
class PanelLihatBuku(QWidget):
    def __init__(self):
        super().__init__()
        self._build()
        self.load_data()
 
    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
 
        hdr = QHBoxLayout()
        title = QLabel("📚  DAFTAR BUKU")
        title.setObjectName("title_label")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
 
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("🔍  Cari buku…")
        self.inp_search.setFixedWidth(220)
        self.inp_search.textChanged.connect(self.filter_table)
 
        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(self.inp_search)
        layout.addLayout(hdr)
 
        self.tbl = make_table(["Kode", "Nama Buku", "Penulis", "Genre", "Stok"])
        self.tbl.setColumnWidth(0, 70)
        self.tbl.setColumnWidth(1, 250)
        self.tbl.setColumnWidth(2, 180)
        self.tbl.setColumnWidth(3, 100)
        layout.addWidget(self.tbl)
 
    def load_data(self):
        self.all_data = db.get_all_buku()
        self._render(self.all_data)
 
    def _render(self, data):
        self.tbl.setRowCount(0)
        for d in data:
            r = self.tbl.rowCount()
            self.tbl.insertRow(r)
            self.tbl.setItem(r, 0, cell(d["kode_buku"]))
            self.tbl.setItem(r, 1, cell(d["nama_buku"]))
            self.tbl.setItem(r, 2, cell(d["penulis"]))
            self.tbl.setItem(r, 3, cell(d["genre"]))
            stok_item = cell(d["stok"])
            if d["stok"] == 0:
                stok_item.setForeground(Qt.red)
            else:
                stok_item.setForeground(Qt.darkGreen)
            self.tbl.setItem(r, 4, stok_item)
            self.tbl.setRowHeight(r, 36)
 
    def filter_table(self, text):
        q = text.lower()
        filtered = [d for d in self.all_data if
                    q in d["nama_buku"].lower() or
                    q in d["penulis"].lower() or
                    q in d["genre"].lower() or
                    q in d["kode_buku"].lower()]
        self._render(filtered)
 
 
# ──────────────────────────────────────────────────────
#  Panel Pinjam Buku
# ──────────────────────────────────────────────────────
class PanelPinjam(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self._build()
        self.load_data()
 
    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
 
        hdr = QHBoxLayout()
        title = QLabel("📖  PINJAM BUKU")
        title.setObjectName("title_label")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
 
        btn_pinjam = QPushButton("➕  Pinjam Buku Baru")
        btn_pinjam.setFixedHeight(34)
        btn_pinjam.clicked.connect(self.buka_dialog_pinjam)
 
        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(btn_pinjam)
        layout.addLayout(hdr)
 
        info = QLabel("Buku yang sedang Anda pinjam:")
        info.setStyleSheet("color: #607456; font-weight: bold; font-size: 12px;")
        layout.addWidget(info)
 
        self.tbl = make_table(["Kode", "Nama Buku", "Tgl Pinjam", "Aksi"])
        self.tbl.setColumnWidth(0, 70)
        self.tbl.setColumnWidth(1, 280)
        self.tbl.setColumnWidth(2, 110)
        layout.addWidget(self.tbl)
 
    def load_data(self):
        data = db.get_peminjaman_aktif_by_user(self.user["id"])
        self.tbl.setRowCount(0)
        for d in data:
            r = self.tbl.rowCount()
            self.tbl.insertRow(r)
            self.tbl.setItem(r, 0, cell(d["kode_buku"]))
            self.tbl.setItem(r, 1, cell(d["nama_buku"]))
            self.tbl.setItem(r, 2, cell(d["tgl_pinjam"]))
 
            aksi_widget = QWidget()
            aksi_layout = QHBoxLayout(aksi_widget)
            aksi_layout.setContentsMargins(4, 2, 4, 2)
 
            btn_kembalikan = QPushButton("✔ Kembalikan")
            btn_kembalikan.setFixedSize(100, 26)
            btn_kembalikan.clicked.connect(lambda _, pid=d["id"]: self.kembalikan(pid))
            aksi_layout.addWidget(btn_kembalikan)
 
            self.tbl.setCellWidget(r, 3, aksi_widget)
            self.tbl.setRowHeight(r, 38)
 
    def buka_dialog_pinjam(self):
        dlg = DialogPinjam(self, self.user["id"])
        if dlg.exec_() == QDialog.Accepted:
            self.load_data()
 
    def kembalikan(self, pinjam_id):
        ret = QMessageBox.question(self, "Konfirmasi", "Kembalikan buku ini?",
                                   QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            ok, msg = db.kembalikan_buku(pinjam_id)
            if ok:
                QMessageBox.information(self, "Sukses", msg)
                self.load_data()
            else:
                QMessageBox.critical(self, "Gagal", msg)
 
 
# ──────────────────────────────────────────────────────
#  Panel History Peminjaman
# ──────────────────────────────────────────────────────
class PanelHistory(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self._build()
        self.load_data()
 
    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
 
        hdr = QHBoxLayout()
        title = QLabel("📜  HISTORY PEMINJAMAN")
        title.setObjectName("title_label")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
 
        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["Semua", "dipinjam", "dikembalikan"])
        self.cmb_status.currentTextChanged.connect(self.filter_table)
 
        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(QLabel("Filter:"))
        hdr.addWidget(self.cmb_status)
        layout.addLayout(hdr)
 
        self.tbl = make_table(["Kode", "Nama Buku", "Penulis", "Genre", "Tgl Pinjam", "Tgl Kembali", "Status"])
        self.tbl.setColumnWidth(0, 65)
        self.tbl.setColumnWidth(1, 180)
        self.tbl.setColumnWidth(2, 130)
        self.tbl.setColumnWidth(3, 80)
        self.tbl.setColumnWidth(4, 95)
        self.tbl.setColumnWidth(5, 95)
        layout.addWidget(self.tbl)
 
    def load_data(self):
        self.all_data = db.get_peminjaman_by_user(self.user["id"])
        self._render(self.all_data)
 
    def _render(self, data):
        self.tbl.setRowCount(0)
        for d in data:
            r = self.tbl.rowCount()
            self.tbl.insertRow(r)
            self.tbl.setItem(r, 0, cell(d["kode_buku"]))
            self.tbl.setItem(r, 1, cell(d["nama_buku"]))
            self.tbl.setItem(r, 2, cell(d["penulis"]))
            self.tbl.setItem(r, 3, cell(d["genre"]))
            self.tbl.setItem(r, 4, cell(d["tgl_pinjam"]))
            self.tbl.setItem(r, 5, cell(d.get("tgl_kembali") or "-"))
            status_item = cell(d["status"])
            if d["status"] == "dipinjam":
                status_item.setForeground(Qt.darkRed)
            else:
                status_item.setForeground(Qt.darkGreen)
            self.tbl.setItem(r, 6, status_item)
            self.tbl.setRowHeight(r, 36)
 
    def filter_table(self):
        status_filter = self.cmb_status.currentText()
        if status_filter == "Semua":
            self._render(self.all_data)
        else:
            self._render([d for d in self.all_data if d["status"] == status_filter])
 
 
# ──────────────────────────────────────────────────────
#  Visitor Window (Main)
# ──────────────────────────────────────────────────────
class VisitorWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Perpustakaan Digital — Visitor")
        self.setMinimumSize(960, 620)
        self._build_ui()
 
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
 
        # ── Sidebar ──
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)
        sl = QVBoxLayout(sidebar)
        sl.setContentsMargins(10, 20, 10, 20)
        sl.setSpacing(6)
 
        logo = QLabel("📖")
        logo.setFont(QFont("Segoe UI Emoji", 28))
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("color: #EEE0CC;")
 
        app_title = QLabel("PERPUSTAKAAN\nDIGITAL")
        app_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        app_title.setAlignment(Qt.AlignCenter)
        app_title.setStyleSheet("color: #EEE0CC; margin-bottom: 6px;")
 
        user_lbl = QLabel(f"👤 {self.user['username']}")
        user_lbl.setAlignment(Qt.AlignCenter)
        user_lbl.setStyleSheet("color: #d0c9b8; font-size: 11px; margin-bottom: 10px;")
 
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: rgba(255,255,255,0.3);")
 
        sl.addWidget(logo)
        sl.addWidget(app_title)
        sl.addWidget(user_lbl)
        sl.addWidget(sep)
        sl.addSpacing(8)
 
        self.menu_buttons = []
        menus = [
            ("📚  Daftar Buku", 0),
            ("📖  Pinjam Buku", 1),
            ("📜  History Pinjam", 2),
        ]
 
        for label, idx in menus:
            btn = QPushButton(label)
            btn.setObjectName("menu_btn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, i=idx: self.switch_panel(i))
            sl.addWidget(btn)
            self.menu_buttons.append(btn)
 
        sl.addStretch()
 
        btn_logout = QPushButton("🚪  LOGOUT")
        btn_logout.setObjectName("btn_logout")
        btn_logout.setFixedHeight(38)
        btn_logout.clicked.connect(self.logout)
        sl.addWidget(btn_logout)
 
        # ── Content ──
        self.stack = QStackedWidget()
        self.panel_buku = PanelLihatBuku()
        self.panel_pinjam = PanelPinjam(self.user)
        self.panel_history = PanelHistory(self.user)
 
        self.stack.addWidget(self.panel_buku)
        self.stack.addWidget(self.panel_pinjam)
        self.stack.addWidget(self.panel_history)
 
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack, 1)
 
        self.switch_panel(0)
 
    def switch_panel(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.menu_buttons):
            btn.setChecked(i == index)
        if index == 0:
            self.panel_buku.load_data()
        elif index == 1:
            self.panel_pinjam.load_data()
        elif index == 2:
            self.panel_history.load_data()
 
    def logout(self):
        ret = QMessageBox.question(self, "Logout", "Yakin ingin logout?",
                                   QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            from auth_window import LoginWindow
            self.login_win = LoginWindow()
            self.login_win.show()
            self.close()
 
