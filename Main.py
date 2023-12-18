# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF, MSFluentTitleBar, isDarkTheme
from pathlib import Path

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout
from qfluentwidgets import (PrimaryPushButton,
                            setTheme, Theme)
from qfluentwidgets import setTheme, Theme,SplashScreen
from qframelesswindow.webengine import FramelessWebEngineView
from CustomWebView import CustomWebView
import subprocess
from TableWidget import CustomTableWidget
import json
from FolderSelector import FolderSelectionWidget
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

from qfluentwidgets import InfoBar, setTheme, Theme, InfoBarPosition, LargeTitleLabel, DisplayLabel,CaptionLabel, SmoothScrollArea

from qfluentwidgets import (FlipImageDelegate, Theme, HorizontalPipsPager, HorizontalFlipView,
                            VerticalFlipView, getFont)

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
from qfluentwidgets import PrimaryPushButton, SubtitleLabel, ProgressRing
from PyQt5.QtCore import Qt
import glob



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
        self.webview = FramelessWebEngineView(self)
        WebUrl = "http://localhost:8501/"
        self.webview.load(QUrl(WebUrl))
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.webview)
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



        
        
class FolderSelectionWidget(QWidget):
    
    folderSelected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # self.progressRing = ProgressRing(self)
        # self.progressRing.setValue(55)
        # self.progressRing.setTextVisible(True)
        # self.progressRing.setFixedSize(180, 180)
        self.button = PrimaryPushButton("Select Folder")
        self.button.clicked.connect(self.openFileDialog)

        self.sublabel = SubtitleLabel("", self)  # Initialize with an empty string
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        layout.addWidget(self.sublabel, alignment=Qt.AlignCenter)
        # layout.addWidget(self.progressRing, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.setObjectName("FolderInterface")
        

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if folder_path:
            print("Selected Folder:", folder_path)
            total_images = len(glob.glob(folder_path + "/*.tif"))
            print("Total Images:", total_images)
            self.sublabel.setText(folder_path)  # Update the label text with the selected folder path
            self.folderSelected.emit(folder_path)
# ...


class ImageDis(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background:rgb(32,32,32)}')
        
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.label = LargeTitleLabel('Image Viewer', self)
        self.note = CaptionLabel('Note: the speed or the lag of the preview is caused by the high image resulotion ', self)
        # self.label.setAlignment(Qt.AlignCenter)

        self.setObjectName('ImageInterface')
        self.flipView = HorizontalFlipView(self)
        self.pager = HorizontalPipsPager(self)

        # change aspect ratio mode
        self.flipView.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

        # adjust view size
        self.flipView.setItemSize(QSize(620, 480))
        self.flipView.setFixedSize(QSize(920, 780))

        # NOTE: use custom delegate
        # self.flipView.setItemDelegate(CustomFlipItemDelegate(self.flipView))

        # add images
        self.flipView.addImages([str(i) for i in Path('C:\Main\Code\GradeVision\images').glob('*')])
        self.pager.setPageNumber(self.flipView.count())

        # adjust border radius
        self.flipView.setBorderRadius(10)
        self.flipView.setFixedSize(QSize(710, 470))
        self.flipView.setSpacing(10)

        self.pager.currentIndexChanged.connect(self.flipView.setCurrentIndex)
        self.flipView.currentIndexChanged.connect(self.pager.setCurrentIndex)

        # self.flipView.setCurrentIndex(2)

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.label, 0, Qt.AlignCenter)
        self.layout().addWidget(self.flipView, 0, Qt.AlignCenter)
        self.layout().addWidget(self.pager, 0, Qt.AlignCenter)
        self.layout().addWidget(self.note, 0, Qt.AlignCenter)
        self.layout().setAlignment(Qt.AlignCenter)
        self.layout().setSpacing(20)
        self.resize(600, 600)
        



class Window(FluentWindow):

    def __init__(self):
        super().__init__()
        self.setMicaEffectEnabled(True)
        # create sub interface
        self.mainInterface = Widget('Folder Interface', self) #WebView()
        self.homeInterface = TableWidget()
        self.musicInterface = FolderSelectionWidget()
        self.videoInterface = ImageDis()
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
        self.addSubInterface(self.videoInterface, FIF.PHOTO, 'Image Preview')

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
        self.updateFrameless()
        self.setMicaEffectEnabled(True)
        desktop = QApplication.screens()[0].availableGeometry()
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