import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,)
from PyQt5.QtChart import (
    QBarSet,
    QBarSeries,
    QLineSeries,
    QChart,
    QBarCategoryAxis,
    QChartView,)

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

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Correct vs Wrong Answers")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # Use only the image name (text after the last slash) as the key
        categories = [re.search(r'[^\\]+$', image).group() for image in self.grading_data.keys()]
       
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(chartView)

        # Create second chart (Line Chart)
        line_series = QLineSeries(self)

        # Process data for Line Chart
        for image, data_entry in self.grading_data.items():
            processing_time = data_entry['Processing Time']
            line_series.append(QPointF(categories.index(re.search(r'[^\\]+$', image).group()) + 1, processing_time))

        chart = QChart()
        chart.addSeries(line_series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Processing Time per Image")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        # Line thickness
        line_series.setPen(QPen(QColor("purple"), 4))

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(chartView)

        self.setLayout(self.layout)
        self.setObjectName("graphWindow")

    def load_grading_data(self):
        # Load grading data from CSV
        self.grading_data = defaultdict(dict)

        try:
            with open('GradeVision/app/view\grading_data.csv', 'r') as csvfile:
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
