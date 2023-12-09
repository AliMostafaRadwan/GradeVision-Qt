# coding:utf-8
import sys

import qfluentwidgets
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout
from qfluentwidgets import FluentWindow, SmoothScrollArea

from qframelesswindow import StandardTitleBar
from qframelesswindow.webengine import FramelessWebEngineView


class Window(FluentWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMicaEffectEnabled(True)

        self.interface = SmoothScrollArea(self)
        self.interface.setObjectName("testInterface")

        self.addSubInterface(self.interface, qfluentwidgets.FluentIcon.TAG, "test")

        # change the default title bar if you like
        self.setTitleBar(StandardTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self.interface)

        # must replace QWebEngineView with FramelessWebEngineView
        self.webEngine = FramelessWebEngineView(self)

        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.webEngine)

        # load web page
        self.webEngine.load(QUrl("https://qfluentwidgets.com/"))
        self.resize(1200, 800)

        self.titleBar.raise_()


if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    app.exec()