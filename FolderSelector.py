import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
from qfluentwidgets import PrimaryPushButton, SubtitleLabel, ProgressRing
from PyQt5.QtCore import Qt
import glob


class FolderSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.progressRing = ProgressRing(self)
        self.progressRing.setValue(55)
        self.progressRing.setTextVisible(True)
        self.progressRing.setFixedSize(180, 180)
        self.button = PrimaryPushButton("Select Folder")
        self.button.clicked.connect(self.openFileDialog)

        self.sublabel = SubtitleLabel("", self)  # Initialize with an empty string
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        layout.addWidget(self.sublabel, alignment=Qt.AlignCenter)
        layout.addWidget(self.progressRing, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if folder_path:
            print("Selected Folder:", folder_path)
            total_images = len(glob.glob(folder_path + "/*.tif"))
            print("Total Images:", total_images)
            self.sublabel.setText(folder_path)  # Update the label text with the selected folder path


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = FolderSelectionWidget()
#     ex.show()
#     sys.exit(app.exec_())
