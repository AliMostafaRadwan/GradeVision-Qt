from PyQt5 import QtWidgets, QtGui, QtCore
from .RegionSelectionUI_ui import Ui_Form
from .DetectCircles import detect_contours as detect_circles
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget, QTableWidgetItem, QShortcut, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QKeySequence, QPen, QColor
from PyQt5.QtCore import Qt, QRect, pyqtSignal
import cv2
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
            print(f'x: {x}, y: {y}')
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
                print(f'ROI Count: {roi_count}')  # Print ROI count


            
            # roi_list.append([self.start_point, self.end_point])  # Append ROI coordinates to the list
            # print(f'ROI List: {roi_list}')  # Print ROI list
            width = self.end_point.x() - self.start_point.x()
            height = self.end_point.y() - self.start_point.y()
            print(f'Width: {width}, Height: {height}')
            if Not_omr == False:
            
                roi_list.append([self.start_point.x(), self.start_point.y(), width, height])
                print(f'ROI List: {roi_list}')  # Print ROI list
            
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

    def reset(self):
        if self.revisions:
            self.image = self.revisions[0]
            self.revisions.clear()
            self.update()

    def detect_circles_in_roi(self, image):
        global roi_list
        for roi in roi_list:
            x, y, w, h = roi
            detect_circles(image, x, y, w, h)
            print(f'X: {x}, Y: {y}, W: {w}, H: {h}')
            
        


class RegionSelection(QtWidgets.QWidget, Ui_Form):
    roi_signal = pyqtSignal(int)
    def __init__(self):
        super(RegionSelection, self).__init__()
        self.setupUi(self)
        # global roi_count
        self.table = self.TableWidget
        self.table.setColumnCount(3)
        # self.table.setRowCount(roi_count)
        self.table.setHorizontalHeaderLabels(['ROI Number', 'Row Number', 'Column Number'])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

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
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;All Files (*)', options=options)

        if file_name:
            InfoBar.success('Image uploaded successfully', 'Now please select your ROI(s)', position=InfoBarPosition.TOP,
                            duration=2500, parent=self)
            image = QImage(file_name)
            image = QPixmap.fromImage(image.scaled(1000, 500, Qt.KeepAspectRatio))
            
            global width
            global height
            width = image.width()
            height = image.height()
            
            self.command_bar = CommandBar(self)
            self.command_bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.command_bar.addAction(Action(FluentIcon.CANCEL, 'undo', triggered=self.undo_action))
            
            self.command_bar.addSeparator()
            self.command_bar.addAction(Action(FluentIcon.CLEAR_SELECTION, 'clear selection', triggered=self.clear_selection))
            #not omr button
            self.command_bar.addSeparator()
            self.command_bar.addAction(Action(FluentIcon.TAG, 'Not OMR', triggered=self.not_omr,checkable=True))
            
            self.command_bar.addAction(Action(FluentIcon.CLOSE, 'Close image', triggered=self.clear_image))
            self.command_bar.addAction(Action(FluentIcon.GAME, 'Detect circles', triggered=self.detect_circles))
            
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
    
            #add the command bar to the layout
            self.image_page.layout().addWidget(self.command_bar)
            
            
            # Center the image on the page
            self.image_page.layout().setAlignment(Qt.AlignCenter)
            
            self.canvas.roi_signal.connect(self.display_roi)





    def detect_circles(self):
        global file_name
        global width
        global height
        img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (width, height))
        self.canvas.detect_circles_in_roi(img)



    def clear_image(self):
        global roi_count
        roi_count = 0  # Reset ROI count
        global roi_list
        roi_list.clear()  # Clear the ROI list
        
        self.table_data_list.clear()
        self.stacked_widget.setCurrentIndex(0)
        
        #prevent the command bar from repeating after the image is cleared
        self.command_bar.deleteLater()
        # self.menu.deleteLater()
        # self.timer.stop()
        

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
        # global roi_list
        

        # Generate a new row in the table using the ROI count from RCanvas
        self.table.setRowCount(roi_count)

        # Update the table with the calculated row and column numbers
        self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(str(roi_count)))
        self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(str()))  # number of rows
        self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(str()))  # number of columns

        # Update the display of the canvas
        self.canvas.update()
    
    
    def testing(self, event):
        print("testing", event)
        
    