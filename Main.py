# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF, MSFluentTitleBar, isDarkTheme

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout
from qfluentwidgets import (PrimaryPushButton,
                            setTheme, Theme)
from qfluentwidgets import setTheme, Theme,SplashScreen

from CustomWebView import CustomWebView
import subprocess
from TableWidget import CustomTableWidget
import json
from FolderSelector import FolderSelectionWidget
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

from qfluentwidgets import InfoBar, setTheme, Theme, InfoBarPosition


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
    print('win11')
else:
    from qframelesswindow import FramelessWindow as Window


class MicaWindow(Window):

    def __init__(self, parent=None):
        super().__init__()
        self.setTitleBar(MSFluentTitleBar(self))
        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())


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

class WebView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.setWindowTitle("My App")
        self.layout = QGridLayout()
        self.layout.addWidget(CustomWebView())  
        self.setLayout(self.layout)
        self.setObjectName("WebView")
        
        self.window
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
        
            
        # Save Button
        self.saveButton = PrimaryPushButton('Save', self, FIF.SAVE)
        self.saveButton.clicked.connect(self.saveData)  # Connect the button click to the saveData method
        
        

        # self.saveButton.clicked.connect(createSuccessInfoBar)
        self.layout.addWidget(self.saveButton)

    def updateTableData(self):
        # Reload data from the JSON file and update the table widget
        new_metadata = json.load(open('meta.json'))
        self.tableWidget.updateData(new_metadata)

        # ... [rest of your TableWidget class]

    def saveData(self):
        # Call the save_table_data_to_json method from CustomTableWidget
        self.tableWidget.save_table_data_to_json('output.json')  # Save to 'output.json'

        InfoBar.success(
            title='Save Successful',
            content='Data has been saved successfully!',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )



        
        
class FolderSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.layout = QVBoxLayout()
        self.FolderWidget = FolderSelectionWidget()
        self.layout.addWidget(self.FolderWidget)
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
        QTimer.singleShot(20, self.splashScreen.close) #200

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
