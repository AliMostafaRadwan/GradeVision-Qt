from PyQt5.QtCore import Qt, QUrl

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QVBoxLayout, QWidget
# from qfluentwidgets import LineEdit, PushButton, PrimaryPushButton, setTheme, Theme, setCustomStyleSheet, CustomStyleSheet
from qframelesswindow.webengine import FramelessWebEngineView
import sys
from qfluentwidgets import FluentIcon as FIF, MSFluentTitleBar, isDarkTheme


# def isWin11():
#     return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


# if isWin11():
#     from qframelesswindow import AcrylicWindow as Window
#     print('win11')
# else:
#     from qframelesswindow import FramelessWindow as Window


# class MicaWindow(Window):

#     def __init__(self):
#         def __init__(self, parent=None):
#             super().__init__()
#             self.setTitleBar(MSFluentTitleBar(self))
#             if isWin11():
#                 self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())


class CustomWebView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # self.url_input = LineEdit()
        # self.load_button = PrimaryPushButton("Load URL")
        self.webview = FramelessWebEngineView(self)
        
        # self.load_button.clicked.connect(self.load_url)

        # url = self.url_input.text()
        url = "http://localhost:8501/"
        if url:
            self.webview.setUrl(QUrl(url))

        # self.layout.addWidget(self.url_input)
        # self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.webview)

        self.setLayout(self.layout)
        # setMicaEnabled() must be called before setTheme()
        
        
        # setCustomStyleSheet(CustomStyleSheet.DARK)



