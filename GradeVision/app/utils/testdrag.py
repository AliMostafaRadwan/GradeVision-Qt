import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

class DraggableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAcceptDrops(True)
        self.mousePressPos = None
        self.mouseMovePos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressPos = event.globalPos()
            self.mouseMovePos = event.globalPos()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.mousePressPos:
                delta = event.globalPos() - self.mouseMovePos
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.mouseMovePos = event.globalPos()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressPos = None

        super().mouseReleaseEvent(event)

class DragAndDropApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drag and Drop Example")
        self.setGeometry(100, 100, 400, 400)

        label1 = DraggableLabel("Drag this label!", self)
        label1.setGeometry(50, 50, 100, 30)

        label2 = DraggableLabel("Drag this label too!", self)
        label2.setGeometry(150, 150, 120, 30)

def main():
    app = QApplication(sys.argv)
    window = DragAndDropApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
