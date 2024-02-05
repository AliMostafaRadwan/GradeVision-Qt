from PyQt5 import QtWidgets, QtGui
from .RegionSelectionUI_ui import Ui_Form
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget, QLabel, QTableWidgetItem , QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QRect, QRectF
from qfluentwidgets import PrimaryPushButton, InfoBar, InfoBarPosition

class RegionSelection(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(RegionSelection, self).__init__()
        self.setupUi(self)
        self.table = self.TableWidget
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ROI Number', 'Row Number', 'Column Number'])
        # expand the table to fit the contents
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Creating a stacked widget
        self.stacked_widget = QStackedWidget(self)

        # Page 1: Upload Image Button
        upload_page = QtWidgets.QWidget(self)
        upload_layout = QVBoxLayout(upload_page)

        upload_button = PrimaryPushButton('Upload Image', self)
        upload_button.clicked.connect(self.upload_image_clicked)
        upload_layout.addWidget(upload_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(upload_page)

        # Page 2: Display Image and Select ROI
        self.image_page = QtWidgets.QWidget(self)
        image_layout = QVBoxLayout(self.image_page)

        # Use QHBoxLayout to manage the image label's size policy
        hbox = QHBoxLayout(self.image_page)
        hbox.addWidget(self.image_label, alignment=Qt.AlignCenter)
        image_layout.addLayout(hbox)

        self.image_label.mousePressEvent = self.mouse_press_event
        self.image_label.mouseReleaseEvent = self.mouse_release_event

        self.stacked_widget.addWidget(self.image_page)

        # Set up the UI
        self.gridLayout.addWidget(self.stacked_widget, 0, 0, 1, 1)

    def upload_image_clicked(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;All Files (*)', options=options)

        if file_name:
            InfoBar.success('Image uploaded successfully','now please select your ROI(s)' ,position=InfoBarPosition.TOP,duration=3500 ,parent=self)
            image = QImage(file_name)
            pixmap = QPixmap.fromImage(image.scaled(1000, 500, Qt.KeepAspectRatio))

            # Set the image in the QLabel
            self.image_label.setPixmap(pixmap)

            # Switch to the image display page
            self.stacked_widget.setCurrentIndex(1)

    def mouse_press_event(self, event):
        self.roi_rect = QRect(event.pos(), event.pos())

    def mouse_release_event(self, event):
        self.roi_rect.setBottomRight(event.pos())
        self.display_roi()
        
    def display_roi(self):
        if self.image_label.pixmap() and self.roi_rect:
            # Create a copy of the image pixmap
            image_copy = self.image_label.pixmap().copy()

            painter = QPainter(image_copy)
            painter.setPen(Qt.red)

            # Adjust the coordinates to match the displayed image
            adjusted_roi_rect = QRectF(
                self.roi_rect.x(),
                self.roi_rect.y(),
                self.roi_rect.width(),
                self.roi_rect.height()
            ).toRect()

            painter.drawRect(adjusted_roi_rect)
            painter.end()

            # Set the modified image pixmap to the image label
            self.image_label.setPixmap(image_copy.scaled(self.image_label.size()))

            # Get the selected ROI coordinates
            roi_x = adjusted_roi_rect.x()
            roi_y = adjusted_roi_rect.y()
            roi_width = adjusted_roi_rect.width()
            roi_height = adjusted_roi_rect.height()

            print(f'Selected ROI: x={roi_x}, y={roi_y}, width={roi_width}, height={roi_height}')

            # Add the information to the TableWidget
            self.table.setRowCount(self.table.rowCount() + 1)

            self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(str(self.table.rowCount())))
            self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(str()))  # Corrected indices
            self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(str()))  # Corrected indices

            self.roi_rect = None