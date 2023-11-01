from PyQt5.QtCore import Qt, QUrl

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import LineEdit, PushButton, PrimaryPushButton, setTheme, Theme, setCustomStyleSheet, CustomStyleSheet


class CustomWebView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # self.url_input = LineEdit()
        # self.load_button = PrimaryPushButton("Load URL")
        self.webview = QWebEngineView()

        # self.load_button.clicked.connect(self.load_url)

        # url = self.url_input.text()
        url = "http://localhost:8501/"
        if url:
            self.webview.setUrl(QUrl(url))

        # self.layout.addWidget(self.url_input)
        # self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.webview)

        self.setLayout(self.layout)
        
        # setCustomStyleSheet(CustomStyleSheet.DARK)



