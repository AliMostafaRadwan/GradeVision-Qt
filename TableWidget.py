import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QVBoxLayout, QWidget,QHBoxLayout,QHeaderView,QLabel
from qfluentwidgets import TableWidget as QTableWidget


class CustomTableWidget(QWidget):

    
    def __init__(self, meta):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)
        self.tables = []


        for (x, y, width, height), num_columns, num_rows in meta:
            table = QTableWidget(self)
            table.setWordWrap(True)
            table.setRowCount(num_rows)
            table.setColumnCount(1)

            # You should populate each table with your data here
            # Example: songInfos = [...]  # Replace with your data
            # Use a loop to set the table data accordingly
            table.setHorizontalHeaderLabels([f'Column {len(self.tables) + 1}'])
            table.verticalHeader().hide()
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.resizeColumnsToContents()

            self.tables.append(table)
            self.hBoxLayout.addWidget(table)

            # Add a vertical blue line in between the tables
            divider = QWidget(self)
            divider.setFixedWidth(2)
            divider.setFixedHeight(8)
            divider.setStyleSheet("background-color: rgb(0, 120, 0);")
            self.hBoxLayout.addWidget(divider)
            divider.show()
            divider.setObjectName("divider")

        self.setStyleSheet("CustomTableWidget{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.resize(935, 700)
    
    def updateData(self, new_data):
            for i, ((x, y, width, height), num_columns, num_rows) in enumerate(new_data):
                try:
                    table = self.tables[i]
                    table.setWordWrap(True)
                    table.setRowCount(num_rows)
                    table.setColumnCount(1)
                    table.setHorizontalHeaderLabels([f'Column {i + 1}'])
                    try:
                        # write the table data in a json file
                        data = set()
                        for column in range(table.columnCount()):
                            for row in range(table.rowCount()):
                                data.add(table.item(row, column).text())
                        with open('data.json', 'w') as f:
                            json.dump(list(data), f)
                            
                    except Exception as e:
                        print('error')
                        print(e)
                        pass
                except IndexError:
                    table = QTableWidget(self)
                    table.setWordWrap(True)
                    table.setRowCount(num_rows)
                    table.setColumnCount(1)
                    table.setHorizontalHeaderLabels([f'Column {i + 1}'])
                    table.verticalHeader().hide()
                    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    table.resizeColumnsToContents()
                    self.tables.append(table)
                    self.hBoxLayout.addWidget(table)

                    # Add a vertical blue line in between the tables
                    divider = QWidget(self)
                    divider.setFixedWidth(2)
                    divider.setFixedHeight(8)
                    divider.setStyleSheet("background-color: rgb(0, 120, 0);")
                    self.hBoxLayout.addWidget(divider)
                    divider.show()
                    divider.setObjectName("divider")
                    # print the table text
    
    
    
    def save_table_data_to_json(self, file_name):
        all_tables_data = []  # List to hold data of all tables

        for table_index, table in enumerate(self.tables):
            column_data = []  # Data for the single column in the current table
            for row in range(table.rowCount()):
                item = table.item(row, 0)  # Assuming there's only one column
                cell_data = item.text() if item is not None else ""
                column_data.append(cell_data)

            # Add this table's data as an object with the column index as the key
            table_data = {f"Column {table_index + 1}": column_data}
            all_tables_data.append(table_data)

        # Writing data to a JSON file
        with open(file_name, 'w') as json_file:
            json.dump(all_tables_data, json_file, indent=4)



# def main():
#     app = QApplication(sys.argv)
#     window = QMainWindow()
#     table_widget = CustomTableWidget(metadata)
#     window.setCentralWidget(table_widget)
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()
