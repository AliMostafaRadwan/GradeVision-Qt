
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QColor

from .grading2_ui import Ui_Form
from .test import Grading


class GradingInterface(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setObjectName("grading")
        self.grading_logic = Grading()
        
        #showing the interface
        self.ProgressRing.setValue(0)
        #show image in the label
        pixmap = QPixmap("rgbpattern2.jpg")
        self.images_label.setPixmap(pixmap)
        self.images_label.setScaledContents(True)

        # Start the grading process in a separate thread
        self.grading_thread = GradingThread(self.grading_logic, "C:\Main\Code\GradeVision/test10")
        self.grading_thread.progress_changed.connect(self.update_progress)
        self.grading_thread.start()
        self.show()
        
    def update_progress(self, value):
        # Update the progress ring value
        self.ProgressRing.setValue(value)

class GradingThread(QThread):
    progress_changed = pyqtSignal(int)

    def __init__(self, grading_logic, path):
        super().__init__()
        self.grading_logic = grading_logic
        self.path = path

    def run(self):
        # Perform grading
        self.grading_logic.grade(self.path, self.progress_changed)

        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = GradingInterface()
    sys.exit(app.exec_())    
        