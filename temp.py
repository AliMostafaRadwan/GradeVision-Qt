import sys
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect

class ROIApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('ROI Selection App')

        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(self.imageLabel)

        self.image = None
        self.resized_image = None
        self.roi = None
        self.drawing = False

        openAction = QtWidgets.QAction('Open Image', self)
        openAction.triggered.connect(self.openImage)

        printROIAction = QtWidgets.QAction('Print ROI', self)
        printROIAction.triggered.connect(self.printROI)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(openAction)

        roiMenu = menubar.addMenu('ROI')
        roiMenu.addAction(printROIAction)

    def openImage(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.bmp *.jpeg *.gif *.tiff)', options=options)

        if filePath:
            self.image = QImage(filePath)
            self.resizeImage()
            self.roi = QRect(0, 0, 0, 0)
            self.updateImage()

    def resizeImage(self):
        if self.image:
            target_width = 600  # Adjust to your desired width
            aspect_ratio = self.image.width() / self.image.height()
            target_height = int(target_width / aspect_ratio)
            self.resized_image = self.image.scaled(target_width, target_height, Qt.KeepAspectRatio)

    def printROI(self):
        if self.roi:
            print(f'ROI Coordinates: x={self.roi.x()}, y={self.roi.y()}, width={self.roi.width()}, height={self.roi.height()}')
        else:
            print('No ROI selected.')

    def updateImage(self):
        if self.resized_image:
            pixmap = QPixmap.fromImage(self.resized_image)
            if self.roi:
                painter = QPainter(pixmap)
                painter.setPen(QPen(QColor(255, 0, 0), 2))
                painter.drawRect(self.roi)
                painter.end()

            self.imageLabel.setPixmap(pixmap)
            self.imageLabel.adjustSize()

    def mousePressEvent(self, event):
        if self.resized_image:
            self.drawing = True
            self.roi = QRect(event.x(), event.y(), 0, 0)

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.roi.setWidth(event.x() - self.roi.x())
            self.roi.setHeight(event.y() - self.roi.y())
            self.updateImage()

    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.drawing = False

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = ROIApp()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
