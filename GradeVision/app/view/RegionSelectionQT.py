from PyQt5 import QtWidgets, QtGui
from .RegionSelectionUI_ui import Ui_Form
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget, QLabel, QTableWidgetItem, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QRect, QRectF
from qfluentwidgets import PrimaryPushButton, Action, FluentIcon, TransparentDropDownPushButton, InfoBar, InfoBarPosition, CommandBar

class RegionSelection(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(RegionSelection, self).__init__()
        self.setupUi(self)
        self.table = self.TableWidget
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ROI Number', 'Row Number', 'Column Number'])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.roi_list = []  # List to store ROIs
        self.current_index = -1  # Index to keep track of the current state
        self.roi_data_list = []  # List to store ROI data for undo/redo
        self.table_data_list = []  # List to store table data for undo/redo

        self.stacked_widget = QStackedWidget(self)

        upload_page = QtWidgets.QWidget(self)
        upload_layout = QVBoxLayout(upload_page)
        upload_button = PrimaryPushButton('Upload Image', self)
        upload_button.clicked.connect(self.upload_image_clicked)
        upload_layout.addWidget(upload_button, alignment=Qt.AlignCenter)
        self.stacked_widget.addWidget(upload_page)

        self.image_page = QtWidgets.QWidget(self)
        image_layout = QVBoxLayout(self.image_page)
        hbox = QHBoxLayout(self.image_page)
        hbox.addWidget(self.image_label, alignment=Qt.AlignCenter)
        image_layout.addLayout(hbox)

        self.image_label.mousePressEvent = self.mouse_press_event
        self.image_label.mouseReleaseEvent = self.mouse_release_event

        self.stacked_widget.addWidget(self.image_page)

        self.gridLayout.addWidget(self.stacked_widget, 0, 0, 1, 1)

    def upload_image_clicked(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;All Files (*)', options=options)

        if file_name:
            InfoBar.success('Image uploaded successfully', 'Now please select your ROI(s)', position=InfoBarPosition.TOP,
                            duration=3500, parent=self)
            image = QImage(file_name)
            pixmap = QPixmap.fromImage(image.scaled(1000, 500, Qt.KeepAspectRatio))

            self.image_label.setPixmap(pixmap)

            self.command_bar = CommandBar(self)
            self.command_bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.command_bar.addAction(Action(FluentIcon.LEFT_ARROW, 'undo', triggered=self.undo_action))
            self.command_bar.addSeparator()
            self.command_bar.addAction(Action(FluentIcon.RIGHT_ARROW, 'redo', triggered=self.redo_action))
            self.command_bar.addWidget(TransparentDropDownPushButton('Menu', self, FluentIcon.MENU))
            self.image_page.layout().addWidget(self.command_bar)

            self.stacked_widget.setCurrentIndex(1)

    def mouse_press_event(self, event):
        self.roi_rect = QRect(event.pos(), event.pos())

    def mouse_release_event(self, event):
        self.roi_rect.setBottomRight(event.pos())
        self.display_roi()

    def display_roi(self):
        if self.image_label.pixmap() and self.roi_rect:
            image_copy = self.image_label.pixmap().copy()
            painter = QPainter(image_copy)
            painter.setPen(Qt.red)

            adjusted_roi_rect = QRectF(
                self.roi_rect.x(),
                self.roi_rect.y(),
                self.roi_rect.width(),
                self.roi_rect.height()
            ).toRect()

            painter.drawRect(adjusted_roi_rect)
            painter.end()

            self.image_label.setPixmap(image_copy.scaled(self.image_label.size()))

            # Store ROI data for undo/redo
            self.roi_data_list = self.roi_data_list[:self.current_index + 1]
            self.roi_data_list.append(adjusted_roi_rect)
            self.current_index = len(self.roi_data_list) - 1

            roi_x = adjusted_roi_rect.x()
            roi_y = adjusted_roi_rect.y()
            roi_width = adjusted_roi_rect.width()
            roi_height = adjusted_roi_rect.height()

            print(f'Selected ROI: x={roi_x}, y={roi_y}, width={roi_width}, height={roi_height}')

            # Append table data to the list for redo
            self.table_data_list.append(self.get_table_data())

            self.table.setRowCount(self.table.rowCount() + 1)
            self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(str(self.table.rowCount())))
            self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(str()))  # Corrected indices
            self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(str()))  # Corrected indices

            self.roi_rect = None

    def undo_action(self):
        if self.current_index >= 0:
            # Remove the last ROI and corresponding table data
            self.roi_data_list.pop()
            self.table_data_list.pop()
            self.table.removeRow(self.table.rowCount() - 1)
            self.current_index = len(self.roi_data_list) - 1
            self.update_display()

    def redo_action(self):
        if self.current_index < len(self.roi_data_list) - 1:
            # Redo the last undone ROI
            self.current_index += 1
            self.table.clearContents()
            self.restore_table_data(self.table_data_list[self.current_index])
            self.display_roi()

    def update_display(self):
        if 0 <= self.current_index < len(self.roi_data_list):
            image_copy = self.image_label.pixmap().copy()
            painter = QPainter(image_copy)
            painter.setPen(Qt.red)

            for roi_rect in self.roi_data_list[:self.current_index + 1]:
                painter.drawRect(roi_rect)

            painter.end()
            self.image_label.setPixmap(image_copy.scaled(self.image_label.size()))

    def get_table_data(self):
        table_data = []
        for row in range(self.table.rowCount()):
            row_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
            table_data.append(row_data)
        return table_data

    def restore_table_data(self, data):
        self.table.setRowCount(0)
        for row_data in data:
            self.table.setRowCount(self.table.rowCount() + 1)
            for col, value in enumerate(row_data):
                self.table.setItem(self.table.rowCount() - 1, col, QTableWidgetItem(value))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = RegionSelection()
    window.show()
    app.exec_()
