from PyQt5 import QtWidgets, QtGui, QtCore
from .RegionSelectionUI_ui import Ui_Form
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget, QTableWidgetItem, QShortcut
from PyQt5.QtGui import QPixmap, QImage, QPainter, QKeySequence, QPen
from PyQt5.QtCore import Qt, QRect, pyqtSignal

# Import RCanvas from the edited ROI code
from qfluentwidgets import PrimaryPushButton, Action, FluentIcon, TransparentDropDownPushButton, InfoBar, InfoBarPosition, CommandBar

class RCanvas(QtWidgets.QWidget):
    customSignal = pyqtSignal(int)

    def __init__(self, photo, parent=None):
        super().__init__(parent)
        self.image = QImage(photo)
        self.setFixedSize(self.image.width(), self.image.height())
        self.pressed = self.moving = False
        self.revisions = []
        global roi_count
        roi_count = 0  # Initialize ROI count

        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = True
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.moving = True
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        global roi_count
        if event.button() == Qt.LeftButton:
            self.revisions.append(self.image.copy())
            qp = QPainter(self.image)
            self.draw_rectangle(qp) if self.moving else self.draw_point(qp)
            self.pressed = self.moving = False
            self.update()
            roi_count += 1  # Increment ROI count
            print(f'ROI Count: {roi_count}')  # Print ROI count

            # Emit the roiCountChanged signal here
            self.customSignal.emit(roi_count)

    def paintEvent(self, event):
        qp = QPainter(self)
        rect = event.rect()
        qp.drawImage(rect, self.image, rect)
        if self.moving:
            self.draw_rectangle(qp)
        elif self.pressed:
            self.draw_point(qp)

    def draw_point(self, qp):
        qp.setPen(QPen(Qt.black, 5))
        qp.drawPoint(self.start_point)

    def draw_rectangle(self, qp):
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(QPen(Qt.red, 3, Qt.DashLine))
        rect = QRect(self.start_point, self.end_point)
        qp.drawRect(rect)

    def undo(self):
        global roi_count
        if self.revisions:
            self.image = self.revisions.pop()
            self.update()
            roi_count -= 1  # Decrement ROI count

    def reset(self):
        global roi_count
        if self.revisions:
            self.image = self.revisions[0]
            self.revisions.clear()
            self.update()
            roi_count = 0

    def count(self):
        return self.roi_count

    # Add a direct_roi_count_changed method for direct signal emission
    def direct_roi_count_changed(self, count):
        print(f'Direct ROI Count Changed: {count}')

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

        # Use RCanvas from the edited ROI code
        self.canvas = RCanvas(QImage(), parent=self.image_page)
        image_layout.addWidget(self.canvas)

        self.stacked_widget.addWidget(self.image_page)

        self.gridLayout.addWidget(self.stacked_widget, 0, 0, 1, 1)

        # Connect undo/redo shortcuts to canvas functions
        QShortcut(QKeySequence('Ctrl+Z'), self, self.canvas.undo)
        QShortcut(QKeySequence('Ctrl+R'), self, self.canvas.reset)
        # Connect roiCountChanged signal to display_roi function
        
        self.canvas.customSignal.connect(self.display_roi)
        
        # # Add a timer to periodically check the signal connection
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.display_roi)
        self.timer.start(50)  # Check every 50ms

    
    def upload_image_clicked(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;All Files (*)', options=options)

        if file_name:
            InfoBar.success('Image uploaded successfully', 'Now please select your ROI(s)', position=InfoBarPosition.TOP,
                            duration=3500, parent=self)
            image = QImage(file_name)
            image = QPixmap.fromImage(image.scaled(1000, 500, Qt.KeepAspectRatio))

            self.image_page.layout().removeWidget(self.canvas)
            self.canvas = RCanvas(image, parent=self.image_page)
            self.image_page.layout().addWidget(self.canvas)

            self.command_bar = CommandBar(self)
            self.command_bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.command_bar.addAction(Action(FluentIcon.CANCEL, 'undo', triggered=self.undo_action))
            self.command_bar.addSeparator()
            self.command_bar.addAction(Action(FluentIcon.CLEAR_SELECTION, 'clear selection', triggered=self.clear_selection))
            self.command_bar.addWidget(TransparentDropDownPushButton('Menu', self, FluentIcon.MENU))
            self.image_page.layout().addWidget(self.command_bar)

            # Center the image on the page
            self.image_page.layout().setAlignment(Qt.AlignCenter)
            self.stacked_widget.setCurrentIndex(1)

    def undo_action(self):
        self.canvas.undo()

    def clear_selection(self):
        self.canvas.reset()

    def get_table_data(self):
        table_data = []
        for row in range(self.table.rowCount()):
            row_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
            table_data.append(row_data)
        return table_data

    def restore_table_data(self, data):
        self.table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(value))

    def update_table_with_roi(self, roi_count, row_number, column_number):
        self.table.setRowCount(roi_count)
        self.table.setItem(roi_count - 1, 0, QTableWidgetItem(str(roi_count)))
        self.table.setItem(roi_count - 1, 1, QTableWidgetItem(str(row_number)))
        self.table.setItem(roi_count - 1, 2, QTableWidgetItem(str(column_number)))

    def display_roi(self):
        global roi_count
        print(f'ROI Count: {roi_count} from display_roi function')
        # if self.canvas.image and self.canvas.pressed:
        # Store ROI data for undo/redo
        self.roi_data_list = self.roi_data_list[:self.current_index + 1]
        self.roi_data_list.append(self.canvas.rect())
        self.current_index = len(self.roi_data_list) - 1

        roi_x = self.canvas.rect().x()
        roi_y = self.canvas.rect().y()
        roi_width = self.canvas.rect().width()
        roi_height = self.canvas.rect().height()

        print(f'Selected ROI: x={roi_x}, y={roi_y}, width={roi_width}, height={roi_height}')
        print(f'ROI Count: {roi_count}')

        # Append table data to the list for redo
        self.table_data_list.append(self.get_table_data())

        # Generate a new row in the table using the ROI count from RCanvas
        self.table.setRowCount(roi_count)

        
        # Update the table with the calculated row and column numbers
        self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(str(roi_count)))
        self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(str()))  # Corrected indices
        self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(str()))  # Corrected indices
        
        
        # Update the display of the canvas
        self.canvas.update()
        