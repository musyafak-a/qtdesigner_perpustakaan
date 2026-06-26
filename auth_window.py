from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFrame,
    QRadioButton, QButtonGroup, QMessageBox, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor
import database as db


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perpustakaan - Login")
        self.setFixedSize(800, 600)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Left Banner ──
        banner = QFrame()
        banner.setFixedWidth(340)
        banner.setStyleSheet("background-color: #607456;")
        banner_layout = QVBoxLayout(banner)
        banner_layout.setAlignment(Qt.AlignCenter)
        banner_layout.setSpacing(12)

        icon_lbl = QLabel("📚")
        icon_lbl.setFont(QFont("Segoe UI Emoji", 48))
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("color: #EEE0CC;")

        app_name = QLabel("PERPUSTAKAAN\nDIGITAL")
        app_name.setFont(QFont("Segoe UI", 18, QFont.Bold))
        app_name.setAlignment(Qt.AlignCenter)
        app_name.setStyleSheet("color: #EEE0CC; line-height: 1.5;")

        tagline = QLabel("Sistem Manajemen\nPeminjaman Buku")
        tagline.setFont(QFont("Segoe UI", 10))
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet("color: #d0c9b8;")

        banner_layout.addWidget(icon_lbl)
        banner_layout.addWidget(app_name)
        banner_layout.addWidget(tagline)

        # ── Right Form ──
        form_area = QFrame()
        form_area.setStyleSheet("background-color: #EEE0CC;")
        form_layout = QVBoxLayout(form_area)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setContentsMargins(50, 40, 50, 40)
        form_layout.setSpacing(16)

        title = QLabel("LOGIN")
        title.setObjectName("title_label")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Masuk ke akun Anda")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #888; font-size: 12px;")

        # Email
        lbl_email = QLabel("Email")
        lbl_email.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("contoh@email.com")

        # Password
        lbl_pwd = QLabel("Password")
        lbl_pwd.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.input_pwd = QLineEdit()
        self.input_pwd.setPlaceholderText("••••••••")
        self.input_pwd.setEchoMode(QLineEdit.Password)

        # Buttons
        btn_login = QPushButton("  🔐  LOGIN")
        btn_login.setFixedHeight(42)
        btn_login.clicked.connect(self.do_login)
        btn_login.setCursor(Qt.PointingHandCursor)

        btn_register = QPushButton("  📝  DAFTAR AKUN BARU")
        btn_register.setObjectName("btn_secondary")
        btn_register.setFixedHeight(42)
        btn_register.clicked.connect(self.open_register)
        btn_register.setCursor(Qt.PointingHandCursor)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #d0c4b0;")

        hint = QLabel("Demo: admin@perpus.com / admin123")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #aaa; font-size: 11px;")

        form_layout.addWidget(title)
        form_layout.addWidget(subtitle)
        form_layout.addSpacing(10)
        form_layout.addWidget(lbl_email)
        form_layout.addWidget(self.input_email)
        form_layout.addWidget(lbl_pwd)
        form_layout.addWidget(self.input_pwd)
        form_layout.addSpacing(6)
        form_layout.addWidget(btn_login)
        form_layout.addWidget(sep)
        form_layout.addWidget(btn_register)
        form_layout.addWidget(hint)

        main_layout.addWidget(banner)
        main_layout.addWidget(form_area, 1)

        # Enter key shortcut
        self.input_pwd.returnPressed.connect(self.do_login)

    def do_login(self):
        email = self.input_email.text().strip()
        pwd = self.input_pwd.text()
        if not email or not pwd:
            QMessageBox.warning(self, "Peringatan", "Email dan password harus diisi!")
            return
        user = db.login_user(email, pwd)
        if user:
            self.current_user = user
            self._open_dashboard(user)
        else:
            QMessageBox.critical(self, "Login Gagal", "Email atau password salah!")
            self.input_pwd.clear()

    def _open_dashboard(self, user):
        if user["role"] == "admin":
            from admin_window import AdminWindow
            self.admin_win = AdminWindow(user)
            self.admin_win.show()
        else:
            from visitor_window import VisitorWindow
            self.visitor_win = VisitorWindow(user)
            self.visitor_win.show()
        self.close()

    def open_register(self):
        self.reg_win = RegisterWindow(self)
        self.reg_win.show()


class RegisterWindow(QMainWindow):
    def __init__(self, login_win):
        super().__init__()
        self.login_win = login_win
        self.setWindowTitle("Perpustakaan - Register")
        self.setFixedSize(800, 600)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Left Banner ──
        banner = QFrame()
        banner.setFixedWidth(300)
        banner.setStyleSheet("background-color: #7B2525;")
        bl = QVBoxLayout(banner)
        bl.setAlignment(Qt.AlignCenter)
        bl.setSpacing(12)

        icon = QLabel("📝")
        icon.setFont(QFont("Segoe UI Emoji", 40))
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("color: #EEE0CC;")

        ttl = QLabel("DAFTAR\nAKUN BARU")
        ttl.setFont(QFont("Segoe UI", 17, QFont.Bold))
        ttl.setAlignment(Qt.AlignCenter)
        ttl.setStyleSheet("color: #EEE0CC;")

        desc = QLabel("Buat akun untuk mulai\nmeminjam buku")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #d0b0b0; font-size: 10px;")

        bl.addWidget(icon)
        bl.addWidget(ttl)
        bl.addWidget(desc)

        # ── Right Form ──
        form_area = QFrame()
        form_area.setStyleSheet("background-color: #EEE0CC;")
        fl = QVBoxLayout(form_area)
        fl.setAlignment(Qt.AlignVCenter)
        fl.setContentsMargins(40, 20, 40, 20)
        fl.setSpacing(10)

        title = QLabel("REGISTER")
        title.setObjectName("title_label")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()
        grid.setSpacing(8)

        def lbl(text):
            l = QLabel(text)
            l.setFont(QFont("Segoe UI", 9, QFont.Bold))
            return l

        self.inp_username = QLineEdit()
        self.inp_username.setPlaceholderText("Username unik Anda")
        self.inp_email = QLineEdit()
        self.inp_email.setPlaceholderText("email@contoh.com")
        self.inp_pwd = QLineEdit()
        self.inp_pwd.setPlaceholderText("Minimal 6 karakter")
        self.inp_pwd.setEchoMode(QLineEdit.Password)
        self.inp_tgl = QDateEdit()
        self.inp_tgl.setCalendarPopup(True)
        self.inp_tgl.setDate(QDate(2000, 1, 1))
        self.inp_tgl.setDisplayFormat("dd-MM-yyyy")

        # Gender
        self.rb_laki = QRadioButton("Laki-laki")
        self.rb_perempuan = QRadioButton("Perempuan")
        self.rb_laki.setChecked(True)
        gender_grp = QButtonGroup(self)
        gender_grp.addButton(self.rb_laki)
        gender_grp.addButton(self.rb_perempuan)
        gender_frame = QFrame()
        gfl = QHBoxLayout(gender_frame)
        gfl.setContentsMargins(0, 0, 0, 0)
        gfl.addWidget(self.rb_laki)
        gfl.addWidget(self.rb_perempuan)
        gfl.addStretch()

        grid.addWidget(lbl("Username :"), 0, 0)
        grid.addWidget(self.inp_username, 0, 1)
        grid.addWidget(lbl("Email :"), 1, 0)
        grid.addWidget(self.inp_email, 1, 1)
        grid.addWidget(lbl("Password :"), 2, 0)
        grid.addWidget(self.inp_pwd, 2, 1)
        grid.addWidget(lbl("Tanggal Lahir :"), 3, 0)
        grid.addWidget(self.inp_tgl, 3, 1)
        grid.addWidget(lbl("Jenis Kelamin :"), 4, 0)
        grid.addWidget(gender_frame, 4, 1)

        btn_daftar = QPushButton("  ✅  DAFTAR SEKARANG")
        btn_daftar.setFixedHeight(40)
        btn_daftar.clicked.connect(self.do_register)
        btn_daftar.setCursor(Qt.PointingHandCursor)

        btn_kembali = QPushButton("  ◀  KEMBALI KE LOGIN")
        btn_kembali.setObjectName("btn_secondary")
        btn_kembali.setFixedHeight(40)
        btn_kembali.clicked.connect(self.kembali)
        btn_kembali.setCursor(Qt.PointingHandCursor)

        fl.addWidget(title)
        fl.addSpacing(8)
        fl.addLayout(grid)
        fl.addSpacing(10)
        fl.addWidget(btn_daftar)
        fl.addWidget(btn_kembali)

        main_layout.addWidget(banner)
        main_layout.addWidget(form_area, 1)

    def do_register(self):
        username = self.inp_username.text().strip()
        email = self.inp_email.text().strip()
        pwd = self.inp_pwd.text()
        tgl = self.inp_tgl.date().toString("yyyy-MM-dd")
        gender = "laki-laki" if self.rb_laki.isChecked() else "perempuan"

        if not all([username, email, pwd]):
            QMessageBox.warning(self, "Peringatan", "Semua field harus diisi!")
            return
        if len(pwd) < 6:
            QMessageBox.warning(self, "Peringatan", "Password minimal 6 karakter!")
            return

        ok, msg = db.register_user(username, email, pwd, gender, tgl)
        if ok:
            QMessageBox.information(self, "Sukses", msg)
            self.close()
            self.login_win.show()
        else:
            QMessageBox.critical(self, "Gagal", msg)

    def kembali(self):
        self.close()
        self.login_win.show()
