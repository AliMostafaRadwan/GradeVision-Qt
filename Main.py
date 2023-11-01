# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QIcon, QDesktopServices, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QVBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition)
from qfluentwidgets import FluentIcon as FIF
import time

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QAction, QGridLayout
from qfluentwidgets import (Action, DropDownPushButton, DropDownToolButton, PushButton, PrimaryPushButton,
                            HyperlinkButton, setTheme, Theme, ToolButton, ToggleButton, RoundMenu,
                            SplitPushButton, SplitToolButton, PrimaryToolButton, PrimarySplitPushButton,
                            PrimarySplitToolButton, PrimaryDropDownPushButton, PrimaryDropDownToolButton,
                            TogglePushButton, ToggleToolButton, TransparentPushButton, TransparentToolButton,
                            TransparentToggleToolButton, TransparentTogglePushButton, TransparentDropDownToolButton,
                            TransparentDropDownPushButton, PillPushButton, PillToolButton, setCustomStyleSheet,
                            CustomStyleSheet)
from qfluentwidgets import LineEdit, PushButton, SearchLineEdit, setTheme, Theme,SplashScreen

from PyQt5.QtWebEngineWidgets import QWebEngineView
from CustomWebView import CustomWebView
import subprocess
from TableWidget import CustomTableWidget
import json
from test import FolderSelectionWidget


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.gridLayout = QGridLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label, 0, 0, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

#create a new class for our main window

class WebView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.setWindowTitle("My App")
        self.layout = QGridLayout()
        self.layout.addWidget(CustomWebView())  
        self.setLayout(self.layout)
        self.setObjectName("WebView")

        
        subprocess.Popen(["streamlit", "run", "RegionSelection.py",'--server.headless','true'])


metadata = json.load(open('meta.json'))  # meta.json contains [[(x, y, width, height), num_columns, num_rows], ...
class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.layout = QVBoxLayout()
        self.tableWidget = CustomTableWidget(metadata)  # Pass initial data from the JSON file
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.setObjectName("TableInterface")

        # Create a timer to periodically update the table data
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTableData)
        self.timer.start(2000)  # Set the update interval (in milliseconds)

        # Initial data update
        self.updateTableData()

    def updateTableData(self):
        # Reload data from the JSON file and update the table widget
        new_metadata = json.load(open('meta.json'))
        self.tableWidget.updateData(new_metadata)
        
        
class FolderSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.layout = QVBoxLayout()
        self.button = FolderSelectionWidget()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.setObjectName("FolderInterface")
# ...
class Window(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.mainInterface = WebView()
        self.homeInterface = TableWidget()
        self.musicInterface = FolderSelection()
        self.videoInterface = Widget('Video Interface', self)
        self.folderInterface = Widget('Folder Interface', self)
        self.settingInterface = Widget('Setting Interface', self)
        self.albumInterface = Widget('Album Interface', self)
        self.albumInterface1 = Widget('Album Interface 1', self)
        self.albumInterface2 = Widget('Album Interface 2', self)
        self.albumInterface1_1 = Widget('Album Interface 1-1', self)


        self.initNavigation()
        self.initWindow()
        





    def initNavigation(self):
        self.addSubInterface(self.mainInterface, FIF.HOME, 'Main')
        self.addSubInterface(self.homeInterface, FIF.LABEL, 'Answer Key')
        
        self.addSubInterface(self.musicInterface, FIF.CHECKBOX, 'Grading')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, 'Video library')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.albumInterface, FIF.ALBUM, 'Albums', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.albumInterface1, FIF.ALBUM, 'Album 1', parent=self.albumInterface)
        self.addSubInterface(self.albumInterface1_1, FIF.ALBUM, 'Album 1.1', parent=self.albumInterface1)
        self.addSubInterface(self.albumInterface2, FIF.ALBUM, 'Album 2', parent=self.albumInterface)
        self.addSubInterface(self.folderInterface, FIF.FOLDER, 'Folder library', NavigationItemPosition.SCROLL)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('zhiyiYo', 'resource\shoko.png'),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # add badge to navigation item
        # item = self.navigationInterface.widget(self.homeInterface.objectName())
        # InfoBadge.attension(
        #     text=len(metadata),
        #     parent=item.parent(),
        #     target=item,
        #     position=InfoBadgePosition.NAVIGATION_ITEM
        # )


    def initWindow(self):
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        
        self.splashScreen.setIconSize(QSize(102, 102))
        self.splashScreen.show()
        QTimer.singleShot(2000, self.splashScreen.close)

        self.resize(1000, 750)
        self.setWindowTitle('GradVision')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        
        # self.setStyleSheet("background-image: url(resource\shoko.png);")

    def showMessageBox(self):
        w = MessageBox(
            'This is a test🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('Yes')
        w.cancelButton.setText('No')
        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))
    
    #theme
    setTheme(Theme.DARK)



if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
