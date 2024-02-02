from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5.QtCore import QFileSystemWatcher
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
import csv

from qfluentwidgets import CardWidget, SearchLineEdit, TableWidget, TitleLabel, MessageBox, FluentIcon
from .CheckRes_ui import CheckResUI

class CheckRes(QtWidgets.QWidget, CheckResUI):
    
    def __init__(self, parent=None):
        super(CheckRes, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        self.SearchLineEdit.textChanged.connect(self.search)
        self.TableWidget.cellClicked.connect(self.show_image)
        
        # Set up file watcher
        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.fileChanged.connect(self.handle_file_change)
        
        # Load data initially
        self.load_data('GradeVision/app/view\grading_data.csv')
        
        # Add the CSV file to the file watcher
        self.file_watcher.addPath('GradeVision/app/view\grading_data.csv')
       
    def handle_file_change(self):
        # Reload data when the file changes
        self.load_data('GradeVision/app/view\grading_data.csv')

    def search(self):
        search_term = self.SearchLineEdit.text()
        
        matching_row = None  # Store the matching row index
        
        if search_term:
            for row in range(self.TableWidget.rowCount()):
                if search_term in self.TableWidget.item(row, 0).text():
                    matching_row = row
                    self.TableWidget.showRow(row)
                else:
                    self.TableWidget.hideRow(row)
        else:
            for row in range(self.TableWidget.rowCount()):
                self.TableWidget.showRow(row)
                
        # Display the image in the image_label if a matching row is found
        if matching_row is not None:
            image_path = self.TableWidget.item(matching_row, 1).text()
            pixmap = QtGui.QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.image_label.setFixedSize(600, 600)
            self.image_label.show()

    def show_image(self, row, column):
        # Check if the clicked column corresponds to the image path column
        image_path_column_index = 0  # the image column in the csv file
        if column != image_path_column_index:
            return
        
        # Get the image path from the clicked row
        image_path = self.TableWidget.item(row, image_path_column_index).text()
        
        # Check if the image file exists
        if not QtCore.QFile(image_path).exists():
            title = 'Error'
            content = """Please ensure that the image path you've provided is correct. It's possible that the image file does not exist at the specified location, or the path might be empty. Double-check the path for any typos or errors."""
            w = MessageBox(title, content, self )
            w.setIconSize(QSize(50, 50))

            # NOTE: add custom button to button box
            # w.addButton(FilledPushButton('Apply'), QDialogButtonBox.ButtonRole.ApplyRole)

            if w.exec():
                print('Yes button is pressed')
            else:
                print('Cancel button is pressed')
                return
        
        # Display the image in the image_label
        pixmap = QtGui.QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(500, 500)
        self.image_label.show()

    #load data from csv file and display it in the table
    def load_data(self, csv_filename):
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = {row['Image']: [row['Student Answers'], row['Answer Key'], row['Score'], row['Wrong Answers']] for row in reader}

        self.TableWidget.setRowCount(len(data))
        self.TableWidget.setColumnCount(5)
        self.TableWidget.setHorizontalHeaderLabels(["Image", "Student Answers", "Answer Key", "Score", "Wrong Answers"])
        for row, (image, values) in enumerate(data.items()):
            self.TableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(image))
            for col, value in enumerate(values):
                self.TableWidget.setItem(row, col + 1, QtWidgets.QTableWidgetItem(value))
        self.TableWidget.resizeColumnsToContents()
        self.TableWidget.resizeRowsToContents()
        self.TableWidget.horizontalHeader().setStretchLastSection(True)
        self.TableWidget.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = CheckRes()
    w.show()
    sys.exit(app.exec_())
