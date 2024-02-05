import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QRect

class ImageROISelector(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_pixmap = None

        self.row_label = QLabel('Rows:', self)
        self.row_entry = QLineEdit(self)

        self.col_label = QLabel('Columns:', self)
        self.col_entry = QLineEdit(self)

        self.roi_rect = None
        self.roi_counter = 0  # Counter for the number of ROIs selected

        # Create a table to display ROI information
        self.roi_table = QTableWidget(self)
        self.roi_table.setColumnCount(3)
        self.roi_table.setHorizontalHeaderLabels(['ROI Number', 'Row Number', 'Column Number'])

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        upload_button = QPushButton('Upload Image', self)
        upload_button.clicked.connect(self.upload_image)
        layout.addWidget(upload_button)

        layout.addWidget(self.image_label)

        layout.addWidget(self.row_label)
        layout.addWidget(self.row_entry)

        layout.addWidget(self.col_label)
        layout.addWidget(self.col_entry)

        layout.addWidget(self.roi_table)  # Add the ROI table to the layout

        self.setCentralWidget(central_widget)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image ROI Selector')

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)', options=options)

        if file_name:
            image = QImage(file_name)
            self.image_pixmap = QPixmap.fromImage(image.scaled(1000, 1000, Qt.KeepAspectRatio))
            self.image_label.setPixmap(self.image_pixmap)
            self.image_label.mousePressEvent = self.mouse_press_event
            self.image_label.mouseReleaseEvent = self.mouse_release_event

    def mouse_press_event(self, event):
        self.roi_rect = QRect(event.pos(), event.pos())

    def mouse_release_event(self, event):
        self.roi_rect.setBottomRight(event.pos())
        self.display_roi()

    def display_roi(self):
        if self.image_pixmap and self.roi_rect:
            roi_image = self.image_pixmap.copy(self.roi_rect)
            painter = QPainter(self.image_pixmap)
            painter.setPen(Qt.red)
            painter.drawRect(self.roi_rect)
            painter.end()

            # Get the selected ROI coordinates
            roi_x = self.roi_rect.x()
            roi_y = self.roi_rect.y()
            roi_width = self.roi_rect.width()
            roi_height = self.roi_rect.height()

            print(f'Selected ROI {self.roi_counter + 1}: x={roi_x}, y={roi_y}, width={roi_width}, height={roi_height}')

            # Update the ROI table with the selected ROI information
            self.roi_table.setRowCount(self.roi_counter + 1)
            self.roi_table.setItem(self.roi_counter, 0, QTableWidgetItem(str(self.roi_counter + 1)))
            self.roi_table.setItem(self.roi_counter, 1, QTableWidgetItem(str()))
            self.roi_table.setItem(self.roi_counter, 2, QTableWidgetItem(str()))

            self.image_label.setPixmap(self.image_pixmap)
            self.roi_counter += 1
            self.roi_rect = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageROISelector()
    window.show()
    sys.exit(app.exec_())
