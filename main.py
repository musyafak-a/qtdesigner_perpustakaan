import sys
from PyQt5.QtWidgets import QApplication
from styles import STYLE
import database as db

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    db.init_db()

    from auth_window import LoginWindow
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())