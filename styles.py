STYLE = """
/* ─── Global ─────────────────────────────── */
QMainWindow, QDialog, QWidget {
    background-color: #F5F5F5;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: #2d2d2d;
}

/* ─── Labels ─────────────────────────────── */
QLabel {
    color: #2d2d2d;
}
QLabel#title_label {
    font-size: 20px;
    font-weight: bold;
    color: #607456;
    padding: 6px 0;
}
QLabel#subtitle_label {
    font-size: 13px;
    color: #7B2525;
    font-weight: bold;
}

/* ─── Input Fields ───────────────────────── */
QLineEdit, QComboBox, QDateEdit, QSpinBox {
    background-color: #ffffff;
    border: 1.5px solid #607456;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 13px;
    color: #2d2d2d;
    min-height: 28px;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus {
    border: 2px solid #BA6A4C;
}
QLineEdit[echoMode="2"] {
    lineedit-password-character: 9679;
}

/* ─── Buttons ────────────────────────────── */
QPushButton {
    background-color: #607456;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: bold;
    min-height: 32px;
}
QPushButton:hover {
    background-color: #4e5f46;
}
QPushButton:pressed {
    background-color: #3a4733;
}

QPushButton#btn_danger {
    background-color: #7B2525;
}
QPushButton#btn_danger:hover {
    background-color: #5e1a1a;
}

QPushButton#btn_warning {
    background-color: #BA6A4C;
}
QPushButton#btn_warning:hover {
    background-color: #9b5640;
}

QPushButton#btn_secondary {
    background-color: #F5F5F5;
    color: #607456;
    border: 2px solid #607456;
}
QPushButton#btn_secondary:hover {
    background-color: #ddd0bb;
}

QPushButton#btn_logout {
    background-color: #7B2525;
}
QPushButton#btn_logout:hover {
    background-color: #5e1a1a;
}

/* ─── Table ──────────────────────────────── */
QTableWidget {
    background-color: #ffffff;
    gridline-color: #d0c4b0;
    border: 1.5px solid #607456;
    border-radius: 6px;
    alternate-background-color: #f7f0e8;
    selection-background-color: #BA6A4C;
    selection-color: #ffffff;
}
QTableWidget::item {
    padding: 6px 10px;
}
QHeaderView::section {
    background-color: #607456;
    color: #ffffff;
    font-weight: bold;
    padding: 8px 10px;
    border: none;
    border-right: 1px solid #4e5f46;
    font-size: 12px;
}
QHeaderView::section:last {
    border-right: none;
}
QTableCornerButton::section {
    background-color: #607456;
    border: none;
}

/* ─── GroupBox ───────────────────────────── */
QGroupBox {
    border: 2px solid #607456;
    border-radius: 8px;
    margin-top: 10px;
    padding: 10px;
    background-color: #F5F5F5;
    font-weight: bold;
    color: #607456;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    background-color: #F5F5F5;
    color: #607456;
    font-size: 13px;
    font-weight: bold;
}

/* ─── Sidebar Menu ───────────────────────── */
QFrame#sidebar {
    background-color: #607456;
    border-radius: 0px;
}
QPushButton#menu_btn {
    background-color: transparent;
    color: #F5F5F5;
    text-align: left;
    padding: 12px 20px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: normal;
    min-height: 40px;
}
QPushButton#menu_btn:hover {
    background-color: rgba(255,255,255,0.15);
}
QPushButton#menu_btn:checked {
    background-color: #BA6A4C;
    color: #ffffff;
    font-weight: bold;
}

/* ─── ScrollBar ──────────────────────────── */
QScrollBar:vertical {
    background: #F5F5F5;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #607456;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ─── MessageBox ─────────────────────────── */
QMessageBox {
    background-color: #F5F5F5;
}
QMessageBox QPushButton {
    min-width: 80px;
}

/* ─── RadioButton ────────────────────────── */
QRadioButton {
    spacing: 8px;
    color: #2d2d2d;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #607456;
    background: white;
}
QRadioButton::indicator:checked {
    background-color: #607456;
    border: 2px solid #607456;
}

/* ─── Card Frame ─────────────────────────── */
QFrame#card {
    background-color: #F5F5F5;
    border: 1.5px solid #d0c4b0;
    border-radius: 10px;
    padding: 10px;
}
"""