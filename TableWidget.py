import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QVBoxLayout, QWidget,QHBoxLayout,QHeaderView
from qfluentwidgets import TableWidget as QTableWidget



class CustomTableWidget(QWidget):
    metadata = json.load(open('meta.json'))  # meta.json contains [[(x, y, width, height), num_columns, num_rows], ...
    def __init__(self, meta):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)
        self.tables = []

        for (x, y, width, height), num_columns, num_rows in meta:
            table = QTableWidget(self)
            table.setWordWrap(True)
            table.setRowCount(num_rows)
            table.setColumnCount(num_columns)

            # You should populate each table with your data here
            # Example: songInfos = [...]  # Replace with your data
            # Use a loop to set the table data accordingly

            table.verticalHeader().hide()
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.resizeColumnsToContents()

            self.tables.append(table)
            self.hBoxLayout.addWidget(table)
            #add a vertical blue line in between the tables
            divider = QWidget(self)
            divider.setFixedWidth(2)
            divider.setFixedHeight(10)
            divider.setStyleSheet("background-color: rgb(0, 120, 0);")
            self.hBoxLayout.addWidget(divider)
            divider.show()
            divider.setObjectName("divider")
            # divider.setContentsMargins(0, 0, 0, 0)
            
            

        print(self.tables)
        print('length of tables:',len(self.tables))
        self.setStyleSheet("CustomTableWidget{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.resize(935, 700)

# def main():
#     app = QApplication(sys.argv)
#     window = QMainWindow()
#     table_widget = CustomTableWidget(metadata)
#     window.setCentralWidget(table_widget)
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()
