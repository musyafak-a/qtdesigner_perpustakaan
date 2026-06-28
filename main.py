import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from styles import STYLE
import database as db

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    # Cek koneksi MySQL sebelum buka jendela
    try:
        db.init_db()
    except ConnectionError as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Koneksi Database Gagal")
        msg.setText(str(e))
        msg.exec_()
        sys.exit(1)

    from auth_window import LoginWindow
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())