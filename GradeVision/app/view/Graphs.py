import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,
)
from PyQt5.QtChart import (
    QBarSet,
    QBarSeries,
    QLineSeries,
    QChart,
    QBarCategoryAxis,
    QChartView,
    QValueAxis
)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
import csv
from collections import defaultdict
import re

class MyChartWidget(QWidget):
    def __init__(self, parent=None):
        super(MyChartWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Load grading data from CSV
        self.load_grading_data()

        # Create first chart (Bar Chart)
        series = QBarSeries()

        # Process data for Bar Chart
        correct_answers_set = QBarSet("Correct Answers")
        wrong_answers_set = QBarSet("Wrong Answers")

        for image, data_entry in self.grading_data.items():
            correct_answers = data_entry['Score']
            wrong_answers = len(data_entry['Wrong Answers'])
            correct_answers_set.append(correct_answers)
            wrong_answers_set.append(wrong_answers)

        series.append(correct_answers_set)
        series.append(wrong_answers_set)

        chart1 = QChart()
        chart1.addSeries(series)
        chart1.setTitle("Correct vs Wrong Answers")
        chart1.setAnimationOptions(QChart.SeriesAnimations)

        # Set chart title color
        chart1.setTitleBrush(QColor("white"))

        # Use only the image name (text after the last slash) as the key
        categories = [re.search(r'[^\\]+$', image).group() for image in self.grading_data.keys()]

        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisY = QValueAxis()

        # Set axis label colors
        axisX.setLabelsBrush(QColor("white"))
        axisY.setLabelsBrush(QColor("white"))

        chart1.addAxis(axisX, Qt.AlignBottom)
        chart1.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)

        chart1.legend().setVisible(True)
        chart1.legend().setAlignment(Qt.AlignBottom)
        chart1.legend().setLabelBrush(QColor("white"))

        # Set chart background to transparent
        chart1.setBackgroundBrush(Qt.transparent)
        chart1.setPlotAreaBackgroundBrush(Qt.transparent)

        chartView1 = QChartView(chart1)
        chartView1.setRenderHint(QPainter.Antialiasing)
        chartView1.setStyleSheet("background: transparent")
        self.layout.addWidget(chartView1)

        # Create second chart (Line Chart)
        line_series = QLineSeries(self)

        # Process data for Line Chart
        for image, data_entry in self.grading_data.items():
            processing_time = data_entry['Processing Time']
            line_series.append(QPointF(categories.index(re.search(r'[^\\]+$', image).group()) + 1, processing_time))

        chart2 = QChart()
        chart2.addSeries(line_series)
        chart2.createDefaultAxes()
        chart2.setAnimationOptions(QChart.SeriesAnimations)
        chart2.setTitle("Processing Time per Image")
        chart2.setTitleBrush(QColor("white"))

        chart2.legend().setVisible(True)
        chart2.legend().setAlignment(Qt.AlignBottom)
        chart2.legend().setLabelBrush(QColor("white"))
        # Line thickness
        line_series.setPen(QPen(QColor("purple"), 4))

        axisX2 = QBarCategoryAxis()
        axisX2.append(categories)
        axisY2 = QValueAxis()

        # Set axis label colors
        axisX2.setLabelsBrush(QColor("white"))
        axisY2.setLabelsBrush(QColor("white"))

        chart2.setAxisX(axisX2, line_series)
        chart2.setAxisY(axisY2, line_series)

        # Set chart background to transparent
        chart2.setBackgroundBrush(Qt.transparent)
        chart2.setPlotAreaBackgroundBrush(Qt.transparent)

        chartView2 = QChartView(chart2)
        chartView2.setRenderHint(QPainter.Antialiasing)
        chartView2.setStyleSheet("background: transparent")
        self.layout.addWidget(chartView2)

        self.setLayout(self.layout)
        self.setObjectName("graphWindow")

    def load_grading_data(self):
        # Load grading data from CSV
        self.grading_data = defaultdict(dict)

        try:
            with open('GradeVision/app/view/grading_data.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    image = row['Image']
                    self.grading_data[image]['Score'] = int(row['Score'])
                    self.grading_data[image]['Wrong Answers'] = row['Wrong Answers'].split(',')
                    self.grading_data[image]['Processing Time'] = float(row['Processing Time'])
        except FileNotFoundError:
            print("CSV file not found. Run the grading script first.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    chart_widget = MyChartWidget(window)
    window.setCentralWidget(chart_widget)
    window.show()
    sys.exit(app.exec_())
