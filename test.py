import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from qfluentwidgets import PrimaryPushButton, setTheme, Theme

class FolderSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.button = PrimaryPushButton("Select Folder")
        self.button.clicked.connect(self.openFileDialog)

        layout.addWidget(self.button)
        self.setLayout(layout)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if folder_path:
            print("Selected Folder:", folder_path)

