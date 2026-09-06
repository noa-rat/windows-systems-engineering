
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter
from client.shared.styles import APP_STYLE, DARK_STYLE
from client.presenters.graph_presenter import GraphPresenter

class GraphView(QWidget):
    def __init__(self, parent=None , style=APP_STYLE):
        super().__init__()
        self.setStyleSheet(style)
        self.setWindowTitle("News Graphs")
        self.resize(400, 400)
        self.parent_window = parent
        self.presenter = GraphPresenter()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("📈 News Data Visualization")
        self.label.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.chart_view = None
        self.init_chart()

    def init_chart(self):
        self.series = QPieSeries()

        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("News Distribution by Category")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(self.chart_view)
        self.presenter.fetch_category_data(self._data_loaded, self._data_failed)

    def _data_loaded(self, data):
        self.series.clear()
        for label, count in (data or {}).items():
            self.series.append(str(label), float(count))

    def _data_failed(self, error):
        print("Failed to load graph data:", error)