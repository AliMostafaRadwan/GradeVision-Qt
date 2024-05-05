# import os
# from pathlib import Path
# import sys

# from PyQt5.QtCore import QCoreApplication, Qt, QUrl
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtQml import QQmlApplicationEngine

# CURRENT_DIRECTORY = Path(__file__).resolve().parent


# def main():
#     app = QApplication(sys.argv)

#     engine = QQmlApplicationEngine()

#     filename = os.fspath(CURRENT_DIRECTORY / "main.qml")
#     url = QUrl.fromLocalFile(filename)

#     def handle_object_created(obj, obj_url):
#         if obj is None and url == obj_url:
#             QCoreApplication.exit(-1)

#     engine.objectCreated.connect(
#         handle_object_created, Qt.ConnectionType.QueuedConnection
#     )
#     engine.load(url)

#     sys.exit(app.exec())


# if __name__ == "__main__":
#     main()



from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import sys

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()
        self.engine.load(r'GradeVision\app\view\main.qml')
        if not self.engine.rootObjects():
            sys.exit(-1)
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    
    main_widget = MainWidget()
    
    