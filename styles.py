STYLE = """
/* ─── Global ─────────────────────────────── */
QMainWindow, QDialog, QWidget {
    background-color: #0a0a1a;
    font-family: 'Helvetica', 'Arial', sans-serif;
    font-size: 13px;
    color: #e0e8ff;
}

/* ─── Labels ─────────────────────────────── */
QLabel {
    color: #e0e8ff;
}
QLabel#title_label {
    font-size: 22px;
    font-weight: bold;
    color: #ffffff;
    padding: 6px 0;
    letter-spacing: 4px;
}
QLabel#subtitle_label {
    font-size: 13px;
    color: #00ffcc;
    font-weight: bold;
    letter-spacing: 2px;
}

/* ─── Input Fields ───────────────────────── */
QLineEdit, QComboBox, QDateEdit, QSpinBox {
    background-color: rgba(0, 255, 204, 0.07);
    border: 1.5px solid rgba(0, 255, 204, 0.45);
    border-radius: 4px;
    padding: 5px 10px;
    font-size: 13px;
    color: #e0f8ff;
    min-height: 28px;
    font-family: 'Helvetica', 'Arial', sans-serif;
    letter-spacing: 1px;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus {
    border: 2px solid #00ffcc;
    background-color: rgba(0, 255, 204, 0.12);
    color: #ffffff;
}
QLineEdit[echoMode="2"] {
    lineedit-password-character: 9679;
}
QComboBox::drop-down {
    border: none;
    background: transparent;
}
QComboBox QAbstractItemView {
    background-color: #0d1b2a;
    border: 1.5px solid #00ffcc;
    color: #e0f8ff;
    selection-background-color: rgba(0, 255, 204, 0.25);
}

/* ─── Buttons ────────────────────────────── */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1a1aff, stop:0.5 #7b2fff, stop:1 #00d4ff);
    color: #ffffff;
    border: 1.5px solid rgba(255, 255, 255, 0.35);
    border-radius: 4px;
    padding: 8px 18px;
    font-size: 12px;
    font-weight: bold;
    font-family: 'Helvetica', 'Arial', sans-serif;
    letter-spacing: 2px;
    min-height: 32px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #3333ff, stop:0.5 #9933ff, stop:1 #00ffff);
    border: 1.5px solid #00ffcc;
    color: #ffffff;
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0000cc, stop:0.5 #5500cc, stop:1 #009999);
}

QPushButton#btn_danger {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #ff0055, stop:1 #cc0033);
    border: 1.5px solid rgba(255,0,85,0.6);
}
QPushButton#btn_danger:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #ff3377, stop:1 #ff0055);
}

QPushButton#btn_warning {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #ff6600, stop:1 #ffcc00);
    border: 1.5px solid rgba(255,165,0,0.6);
    color: #0a0a1a;
}
QPushButton#btn_warning:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #ff8800, stop:1 #ffdd33);
}

QPushButton#btn_secondary {
    background: rgba(0, 255, 204, 0.08);
    color: #00ffcc;
    border: 1.5px solid #00ffcc;
}
QPushButton#btn_secondary:hover {
    background: rgba(0, 255, 204, 0.18);
    color: #ffffff;
}

QPushButton#btn_logout {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #ff0055, stop:1 #cc0033);
    border: 1.5px solid rgba(255,0,85,0.6);
}
QPushButton#btn_logout:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #ff3377, stop:1 #ff0055);
}

/* ─── Table ──────────────────────────────── */
QTableWidget {
    background-color: rgba(10, 10, 40, 0.85);
    gridline-color: rgba(0, 255, 204, 0.18);
    border: 1.5px solid rgba(0, 255, 204, 0.35);
    border-radius: 4px;
    alternate-background-color: rgba(0, 255, 204, 0.04);
    selection-background-color: rgba(0, 212, 255, 0.3);
    selection-color: #ffffff;
    color: #e0f8ff;
}
QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid rgba(0, 255, 204, 0.08);
}
QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1a1aff, stop:1 #7b2fff);
    color: #ffffff;
    font-weight: bold;
    font-family: 'Helvetica', 'Arial', sans-serif;
    letter-spacing: 2px;
    padding: 8px 10px;
    border: none;
    border-right: 1px solid rgba(255,255,255,0.15);
    font-size: 11px;
}
QHeaderView::section:last {
    border-right: none;
}
QTableCornerButton::section {
    background: #1a1aff;
    border: none;
}

/* ─── GroupBox ───────────────────────────── */
QGroupBox {
    border: 1.5px solid rgba(0, 255, 204, 0.4);
    border-radius: 4px;
    margin-top: 10px;
    padding: 10px;
    background-color: rgba(0, 255, 204, 0.04);
    font-weight: bold;
    font-family: 'Helvetica', 'Arial', sans-serif;
    color: #00ffcc;
    letter-spacing: 1px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    background-color: #0a0a1a;
    color: #00ffcc;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
}

/* ─── Sidebar Menu ───────────────────────── */
QFrame#sidebar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0d0d2b, stop:1 #0a0a1a);
    border-right: 1px solid rgba(0, 255, 204, 0.2);
    border-radius: 0px;
}
QPushButton#menu_btn {
    background-color: transparent;
    color: rgba(200, 220, 255, 0.75);
    text-align: left;
    padding: 12px 20px;
    border-radius: 3px;
    font-size: 12px;
    font-family: 'Helvetica', 'Arial', sans-serif;
    font-weight: normal;
    letter-spacing: 1.5px;
    min-height: 40px;
    border: none;
}
QPushButton#menu_btn:hover {
    background-color: rgba(0, 255, 204, 0.1);
    color: #00ffcc;
}
QPushButton#menu_btn:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(123,47,255,0.5), stop:1 rgba(0,212,255,0.2));
    color: #ffffff;
    font-weight: bold;
    border-left: 3px solid #00ffcc;
}

/* ─── ScrollBar ──────────────────────────── */
QScrollBar:vertical {
    background: rgba(0, 255, 204, 0.05);
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7b2fff, stop:1 #00d4ff);
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ─── MessageBox ─────────────────────────── */
QMessageBox {
    background-color: #0d0d2b;
    color: #e0f8ff;
    font-family: 'Helvetica', 'Arial', sans-serif;
}
QMessageBox QLabel {
    color: #e0f8ff;
}
QMessageBox QPushButton {
    min-width: 80px;
}

/* ─── RadioButton ────────────────────────── */
QRadioButton {
    spacing: 8px;
    color: #c0d8ff;
    font-family: 'Helvetica', 'Arial', sans-serif;
    letter-spacing: 1px;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #00ffcc;
    background: rgba(0, 255, 204, 0.08);
}
QRadioButton::indicator:checked {
    background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
        fx:0.5, fy:0.5, stop:0 #00ffcc, stop:0.6 #00ffcc, stop:1 transparent);
    border: 2px solid #00ffcc;
}

/* ─── Card Frame ─────────────────────────── */
QFrame#card {
    background-color: rgba(0, 255, 204, 0.05);
    border: 1px solid rgba(0, 255, 204, 0.25);
    border-radius: 4px;
    padding: 10px;
}
"""