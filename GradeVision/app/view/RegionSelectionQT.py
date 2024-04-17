from PyQt5 import QtWidgets, QtGui, QtCore
from .RegionSelectionUI_ui import Ui_Form
from .DetectCircles import detect_contours as detect_circles
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget, QTableWidgetItem, QShortcut, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QKeySequence, QPen, QColor
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QTimer
import cv2
import json
# Import RCanvas from the edited ROI code
from qfluentwidgets import PrimaryPushButton, Action, FluentIcon, TransparentDropDownPushButton, InfoBar, InfoBarPosition, CommandBar, RoundMenu


class RCanvas(QtWidgets.QWidget):
    roi_signal = pyqtSignal(int)

    def __init__(self, photo, parent=None):
        super().__init__(parent)
        # self.setupUi(self)
        self.image = QImage(photo)
        self.setFixedSize(self.image.width(), self.image.height())
        self.pressed = self.moving = False
        self.revisions = []

        global roi_count
        roi_count = 0  # Initialize ROI count

        global roi_list
        roi_list = []  # List to store ROIs
        global Not_omr
        Not_omr = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = True
            self.start_point = event.pos()
            self.end_point = event.pos()
            
            x = self.start_point.x()
            y = self.start_point.y()
            # print(f'x: {x}, y: {y}')
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
            if Not_omr == False:
                roi_count += 1  # Increment ROI count
                # print(f'ROI Count: {roi_count}')  # Print ROI count

            # roi_list.append([self.start_point, self.end_point])  # Append ROI coordinates to the list
            # print(f'ROI List: {roi_list}')  # Print ROI list
            width = self.end_point.x() - self.start_point.x()
            height = self.end_point.y() - self.start_point.y()
            # print(f'Width: {width}, Height: {height}')
            if Not_omr == False:

                roi_list.append(
                    [self.start_point.x(), self.start_point.y(), width, height])
                # print(f'ROI List: {roi_list}')  # Print ROI list

            self.roi_signal.emit(roi_count)

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
        qp.setBrush(QColor(0, 255, 0, 100))  # Fill color with transparency
        qp.setPen(QPen(Qt.green, 3, Qt.DashLine))
        rect = QRect(self.start_point, self.end_point)
        qp.drawRect(rect)

        if Not_omr:
            qp.setBrush(QColor(0, 0, 255, 100))
            qp.setPen(QPen(Qt.blue, 3, Qt.DashLine))
            rect = QRect(self.start_point, self.end_point)
            qp.drawRect(rect)

    def undo(self):
        global roi_count
        if self.revisions:
            self.image = self.revisions.pop()
            self.update()
            if Not_omr == False:
                try:
                    roi_count -= 1  # Decrement ROI count
                    roi_list.pop()  # Remove the last ROI from the list
                except IndexError:
                    roi_count = 0
                    roi_list.clear()  # Clear the ROI list
            self.roi_signal.emit(roi_count)

    def reset(self):
        if self.revisions:
            self.image = self.revisions[0]
            self.revisions.clear()
            self.update()
            self.roi_signal.emit(roi_count)

    def detect_circles_in_roi(self, image):
        global roi_list
        for roi in roi_list:
            x, y, w, h = roi
            detect_circles(image, x, y, w, h)
            # print(f'X: {x}, Y: {y}, W: {w}, H: {h}')


class RegionSelection(QtWidgets.QWidget, Ui_Form):
    roi_signal = pyqtSignal(int)

    def __init__(self):
        super(RegionSelection, self).__init__()
        self.setupUi(self)
        # global roi_count
        self.table = self.TableWidget
        self.table.setColumnCount(3)
        # self.table.setRowCount(roi_count)
        self.table.setHorizontalHeaderLabels(
            ['ROI Number', 'Number of rows', 'Number Columns'])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

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

        # Add a QVBoxLayout to arrange the command bar and canvas vertically
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        # Set the layout for the image page
        self.image_page.setLayout(layout)

        self.stacked_widget.addWidget(self.image_page)

        self.gridLayout.addWidget(self.stacked_widget, 0, 0, 1, 1)

        # Add a timer to periodically check the signal connection
        # self.timer = QtCore.QTimer(self)
        # self.timer.timeout.connect(self.display_roi)
        # self.timer.start(50)  # Check every 50ms

    def upload_image_clicked(self):
        options = QtWidgets.QFileDialog.Options()
        global file_name
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;All Files (*)', options=options)

        if file_name:
            InfoBar.success('Image uploaded successfully', 'Now please select your ROI(s)', position=InfoBarPosition.TOP,
                            duration=2500, parent=self)
            image = QImage(file_name)
            image = QPixmap.fromImage(
                image.scaled(1000, 500, Qt.KeepAspectRatio))

            global width
            global height
            width = image.width()
            height = image.height()
            print(f'Width: {width}, Height: {height}')



            self.command_bar = CommandBar(self)
            self.command_bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.command_bar.addAction(
                Action(FluentIcon.CANCEL, 'undo', triggered=self.undo_action))

            self.command_bar.addSeparator()
            self.command_bar.addAction(Action(
                FluentIcon.CLEAR_SELECTION, 'clear selection', triggered=self.clear_selection))
            # not omr button
            self.command_bar.addSeparator()
            self.command_bar.addAction(
                Action(FluentIcon.TAG, 'Not OMR', triggered=self.not_omr, checkable=True))

            self.command_bar.addAction(
                Action(FluentIcon.CLOSE, 'Close image', triggered=self.clear_image))
            # self.command_bar.addAction(
            #     Action(FluentIcon.GAME, 'Detect circles', triggered=self.detect_circles))

            # menu_button = TransparentDropDownPushButton('More', self, FluentIcon.MENU)
            # self.menu = RoundMenu(self)
            # self.menu.addAction(Action(FluentIcon.FLAG, 'Auto detect rows and columns (experimental)', triggered=self.auto_detect))
            # menu_button.setMenu(self.menu)
            # self.command_bar.addWidget(menu_button)

            layout = QVBoxLayout()
            command_bar_layout = QVBoxLayout()
            command_bar_layout.addWidget(self.command_bar)
            layout.addLayout(command_bar_layout)

            self.stacked_widget.setCurrentIndex(1)

            self.image_page.layout().removeWidget(self.canvas)
            self.canvas = RCanvas(image, parent=self.image_page)
            self.image_page.layout().addWidget(self.canvas)

            # add the command bar to the layout
            self.image_page.layout().addWidget(self.command_bar)

            # Center the image on the page
            self.image_page.layout().setAlignment(Qt.AlignCenter)

            self.canvas.roi_signal.connect(self.display_roi)

    # def detect_circles(self):
    #     global file_name
    #     global width
    #     global height
    #     img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
    #     img = cv2.resize(img, (width, height))
    #     self.canvas.detect_circles_in_roi(img)

    def clear_image(self):
        global roi_count
        roi_count = 0  # Reset ROI count
        global roi_list
        roi_list.clear()  # Clear the ROI list
        self.stacked_widget.setCurrentIndex(0)

        # prevent the command bar from repeating after the image is cleared
        self.command_bar.deleteLater()
        # self.menu.deleteLater()
        # self.timer.stop()

        # emit the signal to reset the ROI count
        self.canvas.roi_signal.emit(roi_count)

    def not_omr(self, checked):
        global Not_omr
        Not_omr = checked
        if checked:
            InfoBar.warning('Not OMR selected', 'The selected area will be highlighted in blue', position=InfoBarPosition.TOP,
                            duration=2500, parent=self)
        else:
            InfoBar.warning('OMR selected', 'The selected area will be highlighted in green', position=InfoBarPosition.TOP,
                            duration=2500, parent=self)

    def undo_action(self):
        self.canvas.undo()

    def clear_selection(self):
        global roi_count
        roi_count = 0
        global roi_list
        roi_list.clear()
        self.canvas.reset()

    def display_roi(self):
        global roi_count
        global roi_list

        # Generate a new row in the table using the ROI count from RCanvas
        self.table.setRowCount(roi_count)

        # Update the table with the calculated row and column numbers
        self.table.setItem(self.table.rowCount() - 1, 0,
                           QTableWidgetItem(str(roi_count)))
        row_item = QTableWidgetItem(str())
        column_item = QTableWidgetItem(str())
        # number of rows user will enter
        self.table.setItem(self.table.rowCount() - 1, 1, row_item)
        # number of columns user will enter
        self.table.setItem(self.table.rowCount() - 1, 2, column_item)
        # print(row_item.text(), column_item.text())

        # Update the display of the canvas
        self.canvas.update()

        # Read table data using Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_table_data)
        self.timer.start(1000)  # 1 second interval

    def read_table_data(self):
        data = []

        for row in range(self.table.rowCount()):
            # Adjusting index since table index is 1-based
            roi_index = int(self.table.item(row, 0).text()) - 1
            roi_values = roi_list[roi_index] if 0 <= roi_index < len(
                roi_list) else None
            row_text = self.table.item(row, 1).text()
            column_text = self.table.item(row, 2).text()
            try:
                x, y, w, h = roi_values
                
                scaled_width, scaled_height = 1000, 1000  # Target size
                print(f"width:{width}, height:{height} from read_table_data")
                
                width_scaling_factor = scaled_width / width
                height_scaling_factor = scaled_height / height
                adjusted_x = int(x * width_scaling_factor)
                adjusted_y = int(y * height_scaling_factor)
                adjusted_width = int(width * width_scaling_factor)
                adjusted_height = int(height * height_scaling_factor)
                
                new_roi = [adjusted_x, adjusted_y, adjusted_width, adjusted_height]
                data.append([new_roi, int(column_text), int(row_text)])
                print(f"ROI: {new_roi}, Row: {row_text}, Column: {column_text}")
            except Exception as e:
                print(f"Error occurred: {e}")
        # print(data)

        # Save data to a JSON file
        json_data = json.dumps(data)
        with open('GradeVision/app/view\JSON\meta.json', 'w') as file:
            file.write(json_data)
