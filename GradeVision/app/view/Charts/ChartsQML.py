import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtCore import QUrl

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout to hold widgets
        layout = QVBoxLayout(self)

        # Create the QQuickWidget
        self.chart_view = QQuickWidget(self)
        self.chart_view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.chart_view.setSource(QUrl(r'GradeVision\app\view\Charts\main.qml'))

        # Add the QQuickWidget to the layout
        layout.addWidget(self.chart_view)

        # Set the window properties
        self.setWindowTitle('QML Chart in QWidget')
        self.setGeometry(300, 300, 500, 400)

def main():
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
