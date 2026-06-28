from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QDialog, QGridLayout, QSpinBox,
    QComboBox, QDateEdit, QAbstractItemView, QSizePolicy, QStackedWidget
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import database as db


# ──────────────────────────────────────────────────────
#  Helper: buat QTableWidget siap pakai
# ──────────────────────────────────────────────────────
def make_table(headers):
    tbl = QTableWidget()
    tbl.setColumnCount(len(headers))
    tbl.setHorizontalHeaderLabels(headers)
    tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
    tbl.setAlternatingRowColors(True)
    tbl.horizontalHeader().setStretchLastSection(True)
    tbl.verticalHeader().setVisible(False)
    tbl.setSortingEnabled(False)
    return tbl


def cell(text):
    item = QTableWidgetItem(str(text) if text is not None else "")
    item.setTextAlignment(Qt.AlignCenter)
    return item


# ──────────────────────────────────────────────────────
#  Dialog Tambah / Edit Buku
# ──────────────────────────────────────────────────────
class DialogBuku(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data  # None = tambah, dict = edit
        self.setWindowTitle("Tambah Buku" if not data else "Edit Buku")
        self.setFixedSize(420, 340)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("TAMBAH BUKU" if not self.data else "EDIT BUKU")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(8)

        def lbl(t):
            l = QLabel(t)
            l.setFont(QFont("Segoe UI", 9, QFont.Bold))
            return l

        self.inp_kode = QLineEdit()
        self.inp_kode.setPlaceholderText("Contoh: BK006")
        self.inp_nama = QLineEdit()
        self.inp_nama.setPlaceholderText("Judul buku")
        self.inp_penulis = QLineEdit()
        self.inp_penulis.setPlaceholderText("Nama penulis")
        self.inp_genre = QLineEdit()
        self.inp_genre.setPlaceholderText("Novel, Sains, dsb.")
        self.inp_stok = QSpinBox()
        self.inp_stok.setMinimum(0)
        self.inp_stok.setMaximum(999)

        grid.addWidget(lbl("Kode Buku :"), 0, 0)
        grid.addWidget(self.inp_kode, 0, 1)
        grid.addWidget(lbl("Nama Buku :"), 1, 0)
        grid.addWidget(self.inp_nama, 1, 1)
        grid.addWidget(lbl("Penulis :"), 2, 0)
        grid.addWidget(self.inp_penulis, 2, 1)
        grid.addWidget(lbl("Genre :"), 3, 0)
        grid.addWidget(self.inp_genre, 3, 1)
        grid.addWidget(lbl("Stok :"), 4, 0)
        grid.addWidget(self.inp_stok, 4, 1)

        layout.addLayout(grid)

        if self.data:
            self.inp_kode.setText(self.data.get("kode_buku", ""))
            self.inp_nama.setText(self.data.get("nama_buku", ""))
            self.inp_penulis.setText(self.data.get("penulis", ""))
            self.inp_genre.setText(self.data.get("genre", ""))
            self.inp_stok.setValue(self.data.get("stok", 1))

        btn_row = QHBoxLayout()
        btn_save = QPushButton("💾  SIMPAN")
        btn_save.setFixedHeight(38)
        btn_save.clicked.connect(self.save)
        btn_cancel = QPushButton("✖  BATAL")
        btn_cancel.setObjectName("btn_secondary")
        btn_cancel.setFixedHeight(38)
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_save)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)

    def save(self):
        kode = self.inp_kode.text().strip()
        nama = self.inp_nama.text().strip()
        penulis = self.inp_penulis.text().strip()
        genre = self.inp_genre.text().strip()
        stok = self.inp_stok.value()

        if not all([kode, nama, penulis, genre]):
            QMessageBox.warning(self, "Peringatan", "Semua field harus diisi!")
            return

        self.result_data = dict(kode=kode, nama=nama, penulis=penulis, genre=genre, stok=stok)
        self.accept()


# ──────────────────────────────────────────────────────
#  Panel Kelola Buku
# ──────────────────────────────────────────────────────
class PanelKelolaBuku(QWidget):
    def __init__(self):
        super().__init__()
        self._build()
        self.load_data()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        # Header
        hdr = QHBoxLayout()
        title = QLabel("📚  KELOLA BUKU")
        title.setObjectName("title_label")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("🔍  Cari buku…")
        self.inp_search.setFixedWidth(220)
        self.inp_search.textChanged.connect(self.filter_table)

        btn_tambah = QPushButton("➕  Tambah Buku")
        btn_tambah.setFixedHeight(34)
        btn_tambah.clicked.connect(self.tambah_buku)

        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(self.inp_search)
        hdr.addWidget(btn_tambah)
        layout.addLayout(hdr)

        # Table
        self.tbl = make_table(["ID", "Kode", "Nama Buku", "Penulis", "Genre", "Stok", "Aksi"])
        self.tbl.setColumnWidth(0, 40)
        self.tbl.setColumnWidth(1, 70)
        self.tbl.setColumnWidth(2, 200)
        self.tbl.setColumnWidth(3, 150)
        self.tbl.setColumnWidth(4, 90)
        self.tbl.setColumnWidth(5, 55)
        layout.addWidget(self.tbl)

    def load_data(self):
        self.all_data = db.get_all_buku()
        self._render(self.all_data)

    def _render(self, data):
        self.tbl.setRowCount(0)
        for row_data in data:
            r = self.tbl.rowCount()
            self.tbl.insertRow(r)
            self.tbl.setItem(r, 0, cell(row_data["id"]))
            self.tbl.setItem(r, 1, cell(row_data["kode_buku"]))
            self.tbl.setItem(r, 2, cell(row_data["nama_buku"]))
            self.tbl.setItem(r, 3, cell(row_data["penulis"]))
            self.tbl.setItem(r, 4, cell(row_data["genre"]))
            self.tbl.setItem(r, 5, cell(row_data["stok"]))
            self.tbl.setItem(r, 6, QTableWidgetItem(""))

            aksi_widget = QWidget()
            aksi_layout = QHBoxLayout(aksi_widget)
            aksi_layout.setContentsMargins(4, 2, 4, 2)
            aksi_layout.setSpacing(4)

            btn_edit = QPushButton("✏ Edit")
            btn_edit.setObjectName("btn_warning")
            btn_edit.setFixedSize(64, 26)
            btn_edit.clicked.connect(lambda _, d=row_data: self.edit_buku(d))

            btn_del = QPushButton("🗑 Hapus")
            btn_del.setObjectName("btn_danger")
            btn_del.setFixedSize(70, 26)
            btn_del.clicked.connect(lambda _, bid=row_data["id"]: self.hapus_buku(bid))

            aksi_layout.addWidget(btn_edit)
            aksi_layout.addWidget(btn_del)
            self.tbl.setCellWidget(r, 6, aksi_widget)
            self.tbl.setRowHeight(r, 38)

    def filter_table(self, text):
        q = text.lower()
        filtered = [d for d in self.all_data if
                    q in d["nama_buku"].lower() or
                    q in d["kode_buku"].lower() or
                    q in d["penulis"].lower() or
                    q in d["genre"].lower()]
        self._render(filtered)

    def tambah_buku(self):
        dlg = DialogBuku(self)
        if dlg.exec_() == QDialog.Accepted:
            d = dlg.result_data
            ok, msg = db.tambah_buku(d["kode"], d["nama"], d["penulis"], d["genre"], d["stok"])
            if ok:
                QMessageBox.information(self, "Sukses", msg)
                self.load_data()
            else:
                QMessageBox.critical(self, "Gagal", msg)

    def edit_buku(self, data):
        dlg = DialogBuku(self, data)
        if dlg.exec_() == QDialog.Accepted:
            d = dlg.result_data
            db.update_buku(data["id"], d["kode"], d["nama"], d["penulis"], d["genre"], d["stok"])
            QMessageBox.information(self, "Sukses", "Buku berhasil diperbarui!")
            self.load_data()

    def hapus_buku(self, buku_id):
        ret = QMessageBox.question(self, "Konfirmasi", "Hapus buku ini?",
                                   QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            db.delete_buku(buku_id)
            self.load_data()


# ──────────────────────────────────────────────────────
#  Panel Kelola Visitor
# ──────────────────────────────────────────────────────
class PanelKelolaVisitor(QWidget):
    def __init__(self):
        super().__init__()
        self._build()
        self.load_data()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        hdr = QHBoxLayout()
        title = QLabel("👥  KELOLA VISITOR")
        title.setObjectName("title_label")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("🔍  Cari visitor…")
        self.inp_search.setFixedWidth(220)
        self.inp_search.textChanged.connect(self.filter_table)

        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(self.inp_search)
        layout.addLayout(hdr)

        self.tbl = make_table(["ID", "Username", "Email", "Gender", "Tgl Lahir", "Terdaftar", "Aksi"])
        self.tbl.setColumnWidth(0, 40)
        self.tbl.setColumnWidth(1, 120)
        self.tbl.setColumnWidth(2, 180)
        self.tbl.setColumnWidth(3, 80)
        self.tbl.setColumnWidth(4, 90)
        self.tbl.setColumnWidth(5, 90)
        layout.addWidget(self.tbl)

    def load_data(self):
        self.all_data = db.get_all_visitors()
        self._render(self.all_data)

    def _render(self, data):
        self.tbl.setRowCount(0)
        for row_data in data:
            r = self.tbl.rowCount()
            self.tbl.insertRow(r)
            self.tbl.setItem(r, 0, cell(row_data["id"]))
            self.tbl.setItem(r, 1, cell(row_data["username"]))
            self.tbl.setItem(r, 2, cell(row_data["email"]))
            self.tbl.setItem(r, 3, cell(row_data.get("gender", "-")))
            self.tbl.setItem(r, 4, cell(row_data.get("tanggal_lahir", "-")))
            self.tbl.setItem(r, 5, cell(row_data.get("created_at", "-")))

            aksi_widget = QWidget()
            aksi_layout = QHBoxLayout(aksi_widget)
            aksi_layout.setContentsMargins(4, 2, 4, 2)

            btn_del = QPushButton("🗑 Hapus")
            btn_del.setObjectName("btn_danger")
            btn_del.setFixedSize(70, 26)
            btn_del.clicked.connect(lambda _, uid=row_data["id"]: self.hapus_visitor(uid))

            aksi_layout.addWidget(btn_del)
            self.tbl.setCellWidget(r, 6, aksi_widget)
            self.tbl.setRowHeight(r, 38)

    def filter_table(self, text):
        q = text.lower()
        filtered = [d for d in self.all_data if
                    q in d["username"].lower() or q in d["email"].lower()]
        self._render(filtered)

    def hapus_visitor(self, user_id):
        ret = QMessageBox.question(self, "Konfirmasi", "Hapus visitor ini?",
                                   QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            db.delete_visitor(user_id)
            self.load_data()


# ──────────────────────────────────────────────────────
#  Panel Kelola Peminjaman
# ──────────────────────────────────────────────────────
class PanelKelolaPinjam(QWidget):
    def __init__(self):
        super().__init__()
        self._build()
        self.load_data()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        hdr = QHBoxLayout()
        title = QLabel("📋  KELOLA PEMINJAMAN")
        title.setObjectName("title_label")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("🔍  Cari…")
        self.inp_search.setFixedWidth(200)
        self.inp_search.textChanged.connect(self.filter_table)

        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["Semua", "dipinjam", "dikembalikan"])
        self.cmb_status.currentTextChanged.connect(self.filter_table)

        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(self.inp_search)
        hdr.addWidget(self.cmb_status)
        layout.addLayout(hdr)

        self.tbl = make_table(["ID", "Username", "Nama Buku", "Kode", "Tgl Pinjam", "Tgl Kembali", "Status", "Aksi"])
        self.tbl.setColumnWidth(0, 40)
        self.tbl.setColumnWidth(1, 100)
        self.tbl.setColumnWidth(2, 160)
        self.tbl.setColumnWidth(3, 65)
        self.tbl.setColumnWidth(4, 90)
        self.tbl.setColumnWidth(5, 90)
        self.tbl.setColumnWidth(6, 90)
        layout.addWidget(self.tbl)

    def load_data(self):
        self.all_data = db.get_all_peminjaman()
        self._render(self.all_data)

    def _render(self, data):
        self.tbl.setRowCount(0)
        for row_data in data:
            r = self.tbl.rowCount()
            self.tbl.insertRow(r)
            self.tbl.setItem(r, 0, cell(row_data["id"]))
            self.tbl.setItem(r, 1, cell(row_data["username"]))
            self.tbl.setItem(r, 2, cell(row_data["nama_buku"]))
            self.tbl.setItem(r, 3, cell(row_data["kode_buku"]))
            self.tbl.setItem(r, 4, cell(row_data["tgl_pinjam"]))
            self.tbl.setItem(r, 5, cell(row_data.get("tgl_kembali") or "-"))

            status = row_data["status"]
            status_item = cell(status)
            if status == "dipinjam":
                status_item.setForeground(Qt.darkRed)
            else:
                status_item.setForeground(Qt.darkGreen)
            self.tbl.setItem(r, 6, status_item)

            aksi_widget = QWidget()
            aksi_layout = QHBoxLayout(aksi_widget)
            aksi_layout.setContentsMargins(4, 2, 4, 2)

            if status == "dipinjam":
                btn_kembalikan = QPushButton("✔ Kembalikan")
                btn_kembalikan.setFixedSize(100, 26)
                btn_kembalikan.clicked.connect(
                    lambda _, pid=row_data["id"]: self.kembalikan(pid))
                aksi_layout.addWidget(btn_kembalikan)

            self.tbl.setCellWidget(r, 7, aksi_widget)
            self.tbl.setRowHeight(r, 38)

    def filter_table(self):
        q = self.inp_search.text().lower()
        status_filter = self.cmb_status.currentText()
        filtered = []
        for d in self.all_data:
            if q and q not in d["username"].lower() and q not in d["nama_buku"].lower():
                continue
            if status_filter != "Semua" and d["status"] != status_filter:
                continue
            filtered.append(d)
        self._render(filtered)

    def kembalikan(self, pinjam_id):
        ok, msg = db.kembalikan_buku(pinjam_id)
        if ok:
            QMessageBox.information(self, "Sukses", msg)
            self.load_data()
        else:
            QMessageBox.critical(self, "Gagal", msg)


# ──────────────────────────────────────────────────────
#  Panel Dashboard / Home Admin
# ──────────────────────────────────────────────────────
class PanelDashboard(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        welcome = QLabel(f"👋  Selamat datang, {self.user['username']}!")
        welcome.setObjectName("title_label")
        welcome.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(welcome)

        sub = QLabel("Panel Admin — Sistem Manajemen Perpustakaan Digital")
        sub.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(sub)

        layout.addSpacing(10)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        buku = db.get_all_buku()
        visitors = db.get_all_visitors()
        pinjaman = db.get_all_peminjaman()
        aktif = [p for p in pinjaman if p["status"] == "dipinjam"]

        for icon, label, val, color in [
            ("📚", "Total Buku", len(buku), "#607456"),
            ("👥", "Total Visitor", len(visitors), "#7B2525"),
            ("📋", "Total Pinjaman", len(pinjaman), "#BA6A4C"),
            ("⏳", "Sedang Dipinjam", len(aktif), "#5a7a9a"),
        ]:
            card = QFrame()
            card.setObjectName("card")
            card.setFixedSize(160, 110)
            card_layout = QVBoxLayout(card)
            card_layout.setAlignment(Qt.AlignCenter)

            ico = QLabel(icon)
            ico.setFont(QFont("Segoe UI Emoji", 22))
            ico.setAlignment(Qt.AlignCenter)

            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 11px; color: #666;")

            num = QLabel(str(val))
            num.setAlignment(Qt.AlignCenter)
            num.setFont(QFont("Segoe UI", 20, QFont.Bold))
            num.setStyleSheet(f"color: {color};")

            card_layout.addWidget(ico)
            card_layout.addWidget(lbl)
            card_layout.addWidget(num)
            cards_row.addWidget(card)

        cards_row.addStretch()
        layout.addLayout(cards_row)


# ──────────────────────────────────────────────────────
#  Admin Window (Main)
# ──────────────────────────────────────────────────────
class AdminWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Perpustakaan Digital — Admin")
        self.setMinimumSize(1000, 640)
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
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(6)

        logo = QLabel("📚")
        logo.setFont(QFont("Segoe UI Emoji", 28))
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("color: #EEE0CC;")

        app_title = QLabel("PERPUSTAKAAN\nDIGITAL")
        app_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        app_title.setAlignment(Qt.AlignCenter)
        app_title.setStyleSheet("color: #EEE0CC; margin-bottom: 8px;")

        user_lbl = QLabel(f"👤 {self.user['username']}")
        user_lbl.setAlignment(Qt.AlignCenter)
        user_lbl.setStyleSheet("color: #d0c9b8; font-size: 11px; margin-bottom: 12px;")

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: rgba(255,255,255,0.3);")

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(app_title)
        sidebar_layout.addWidget(user_lbl)
        sidebar_layout.addWidget(sep)
        sidebar_layout.addSpacing(8)

        self.menu_buttons = []
        menus = [
            ("🏠  Dashboard", 0),
            ("📚  Kelola Buku", 1),
            ("👥  Kelola Visitor", 2),
            ("📋  Kelola Pinjaman", 3),
        ]

        for label, idx in menus:
            btn = QPushButton(label)
            btn.setObjectName("menu_btn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, i=idx: self.switch_panel(i))
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        sidebar_layout.addStretch()

        btn_logout = QPushButton("🚪  LOGOUT")
        btn_logout.setObjectName("btn_logout")
        btn_logout.setFixedHeight(38)
        btn_logout.clicked.connect(self.logout)
        sidebar_layout.addWidget(btn_logout)

        # ── Content Area ──
        self.stack = QStackedWidget()
        self.panel_dashboard = PanelDashboard(self.user)
        self.panel_buku = PanelKelolaBuku()
        self.panel_visitor = PanelKelolaVisitor()
        self.panel_pinjam = PanelKelolaPinjam()

        self.stack.addWidget(self.panel_dashboard)
        self.stack.addWidget(self.panel_buku)
        self.stack.addWidget(self.panel_visitor)
        self.stack.addWidget(self.panel_pinjam)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack, 1)

        self.switch_panel(0)

    def switch_panel(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.menu_buttons):
            btn.setChecked(i == index)
        # Refresh data on switch
        if index == 1:
            self.panel_buku.load_data()
        elif index == 2:
            self.panel_visitor.load_data()
        elif index == 3:
            self.panel_pinjam.load_data()

    def logout(self):
        ret = QMessageBox.question(self, "Logout", "Yakin ingin logout?",
                                   QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            from auth_window import LoginWindow
            self.login_win = LoginWindow()
            self.login_win.show()
            self.close()