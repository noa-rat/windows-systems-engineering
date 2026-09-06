# client/views/graph_view.py
# ממשק גרפי למסך הגרפים

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter
from client.shared.styles import APP_STYLE, DARK_STYLE
from client.presenters.graph_presenter import GraphPresenter

class GraphView(QWidget):
    def __init__(self, parent=None , style=APP_STYLE):
        super().__init__()
        # סגנון עיצוב אחיד
        self.setStyleSheet(style)
        # כותרת החלון
        self.setWindowTitle("News Graphs")
        # גודל החלון
        self.resize(400, 400)
        # חלון אב (כדי לאפשר חזרה למסך הקודם)
        self.parent_window = parent
        # הפרזנטור שמספק את הנתונים מהשרת
        self.presenter = GraphPresenter()

        # פריסת רכיבים לאורך
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # כותרת
        self.label = QLabel("📈 News Data Visualization")
        self.label.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # הצגת הגרף
        self.init_chart()

    # שולחת בקשה לשרת דרך הפרזנטור ומציגה את הגרף
    def init_chart(self):
        data = self.presenter.fetch_category_data()

        # גרף מסוג תרשים עוגה
        series = QPieSeries()
        for label, count in data.items():
            series.append(label, count)

        # הצגת הגרף נעשית באמצעות QChart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("News Distribution by Category")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(chart_view)