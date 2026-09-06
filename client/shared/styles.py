APP_STYLE = """
    QWidget {
        background-color: #f2f6fc;
        font-family: Assistant, Arial;
    }
    QLabel {
        font-size: 18px;
    }
    QPushButton {
        background-color: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #66b3ff,
            stop:1 #3399ff
        );
        color: white;
        font-size: 16px;
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
        font-size: 14px;
    }
    QTextEdit {
        background-color: #ffffff;
        border: 1px solid #ddd;
        padding: 10px;
        font-size: 14px;
    }
"""

DARK_STYLE = """
    QWidget {
        background-color: #1e1e1e;
        color: #dddddd;
        font-family: Assistant, Arial;
    }
    QLabel {
        font-size: 18px;
        color: #dddddd;
    }
    QPushButton {
        background-color: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #66b3ff,
            stop:1 #3399ff
        );
        color: white;
        font-size: 16px;
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
        font-size: 14px;
        border: 1px solid #555;
    }
    QTextEdit {
        background-color: #2a2a2a;
        color: white;
        border: 1px solid #555;
        padding: 10px;
        font-size: 14px;
    }
"""