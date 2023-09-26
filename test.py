from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import TableWidget, isDarkTheme, setTheme, TableView, TableItemDelegate
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
import json

metadata = json.load(open('meta.json')) #meta.json contains [[(x, y, width, height), num_columns, num_rows], ...

print(metadata)
class CustomTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)
        self.tableView1 = TableWidget(self)
        self.tableView2 = TableWidget(self)

        self.tableView1.setWordWrap(True)
        self.tableView1.setRowCount(4)
        self.tableView1.setColumnCount(5)
        songInfos1 = [
            ['かばん', 'aaaaaaiko', 'かばん', '2004', '5:04'],
            ['爱你', '王心凌', '爱你', '2004', '3:39'],
            ['星のない世界', 'aiko', '星のない世界/横顔', '2007', '5:30'],
            ['横顔', 'aiko', '星のない世界/横顔', '2007', '5:06'],
            # ... (rest of the data)
        ]
        songInfos1 += songInfos1
        for i, songInfo in enumerate(songInfos1):
            for j in range(5):
                self.tableView1.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.tableView1.verticalHeader().hide()
        self.tableView1.setHorizontalHeaderLabels(['Title', 'Artist', 'Album', 'Year', 'Duration'])
        self.tableView1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView1.resizeColumnsToContents()

        self.tableView2.setWordWrap(True)
        self.tableView2.setRowCount(4)
        self.tableView2.setColumnCount(5)
        songInfos2 = [
            ['かばん', 'aaaaaaiko', 'かばん', '2004', '5:04'],
            ['爱你', '王心凌', '爱你', '2004', '3:39'],
            ['星のない世界', 'aiko', '星のない世界/横顔', '2007', '5:30'],
            ['横顔', 'aiko', '星のない世界/横顔', '2007', '5:06'],
            # ... (rest of the data)
        ]
        songInfos2 += songInfos2
        for i, songInfo in enumerate(songInfos2):
            for j in range(5):
                self.tableView2.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.tableView2.verticalHeader().hide()
        self.tableView2.setHorizontalHeaderLabels(['Title', 'Artist', 'Album', 'Year', 'Duration'])
        self.tableView2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView2.resizeColumnsToContents()

        self.setStyleSheet("CustomTableWidget{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.tableView1)
        self.hBoxLayout.addWidget(self.tableView2)
        self.resize(935, 700)



