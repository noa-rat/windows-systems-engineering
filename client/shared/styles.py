APP_STYLE = """
    QWidget {
        background-color: #f2f6fc;
        font-family: Assistant, Arial;
    }
    QFrame#navigationPanel {
        background-color: #e5edf8;
        border: 1px solid #c6d5e8;
        border-radius: 12px;
    }
    QPushButton#navButton {
        background-color: transparent;
        color: #31506f;
        border: 1px solid transparent;
        border-radius: 8px;
        font-size: 11pt;
        font-weight: 600;
        padding: 10px 14px;
        text-align: left;
    }
    QPushButton#navButton:hover {
        background-color: #d3e2f4;
    }
    QPushButton#navButton:checked {
        background-color: #3399ff;
        color: white;
        border-color: #1f6fc1;
    }
    QLabel {
        font-size: 13pt;
    }
    QPushButton {
        background-color: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #66b3ff,
            stop:1 #3399ff
        );
        color: white;
        font-size: 12pt;
        font-weight: bold;
        padding: 8px 12px;
        border-radius: 5px;
        border: 1px solid #1f6fc1;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.5);
        min-height: 28px;
    }
    QPushButton:pressed {
        background-color: #267acc;
        padding-top: 9px;
        padding-bottom: 7px;
    }
    QComboBox {
        padding: 4px;
        font-size: 10pt;
    }
    QTextEdit {
        background-color: #ffffff;
        border: 1px solid #ddd;
        padding: 10px;
        font-size: 10pt;
    }
"""

DARK_STYLE = """
    QWidget {
        background-color: #1e1e1e;
        color: #dddddd;
        font-family: Assistant, Arial;
    }
    QFrame#navigationPanel {
        background-color: #252a31;
        border: 1px solid #3d4650;
        border-radius: 12px;
    }
    QPushButton#navButton {
        background-color: transparent;
        color: #cfd7df;
        border: 1px solid transparent;
        border-radius: 8px;
        font-size: 11pt;
        font-weight: 600;
        padding: 10px 14px;
        text-align: left;
    }
    QPushButton#navButton:hover {
        background-color: #343d47;
    }
    QPushButton#navButton:checked {
        background-color: #3399ff;
        color: white;
        border-color: #1f6fc1;
    }
    QLabel {
        font-size: 13pt;
        color: #dddddd;
    }
    QPushButton {
        background-color: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #66b3ff,
            stop:1 #3399ff
        );
        color: white;
        font-size: 12pt;
        font-weight: bold;
        padding: 8px 12px;
        border-radius: 5px;
        border: 1px solid #1f6fc1;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.5);
        min-height: 28px;
    }
    QPushButton:pressed {
        background-color: #267acc;
        padding-top: 9px;
        padding-bottom: 7px;
    }
    QComboBox {
        background-color: #2c2c2c;
        color: white;
        padding: 4px;
        font-size: 10pt;
        border: 1px solid #555;
    }
    QTextEdit {
        background-color: #2a2a2a;
        color: white;
        border: 1px solid #555;
        padding: 10px;
        font-size: 10pt;
    }
"""