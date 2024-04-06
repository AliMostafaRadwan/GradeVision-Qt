# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                              SubtitleLabel, setFont,FlyoutView, Flyout,RadioButton)
from pathlib import Path

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog

import glob

from qfluentwidgets import (FlipImageDelegate, HorizontalPipsPager, HorizontalFlipView,
                            VerticalFlipView)

import json
from PyQt5.QtWidgets import QStackedWidget, QLabel

from qfluentwidgets import ( FluentIcon,setThemeColor,
                                InfoBar,InfoBarPosition,PrimaryPushButton
                                ,LargeTitleLabel,CaptionLabel,SplashScreen)
# from qmaterialwidgets import palette
from qfluentwidgets import SegmentedToggleToolWidget

from .TableWidget import CustomTableWidget

from .Graphs import MyChartWidget as GraphWindow
# from .temp import GradingInterface as Ui_Form
from .GradingWidget import StartWidget as GradingApp
from .checkresults import CheckRes
from .RegionSelectionQT import RegionSelection
from .setting_interface import SettingInterface



# class Widget(QFrame):

#     def __init__(self, text: str, parent=None):
#         super().__init__(parent=parent)
#         self.label = SubtitleLabel(text, self)
#         self.hBoxLayout = QHBoxLayout(self)

#         setFont(self.label, 24)
#         self.label.setAlignment(Qt.AlignCenter)
#         self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
#         self.setObjectName(text.replace(' ', '-'))




metadata = json.load(open('GradeVision/app/view\JSON\meta.json'))  # meta.json contains [[(x, y, width, height), num_columns, num_rows], ...

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.layout = QVBoxLayout()
        
        self.tableWidget = CustomTableWidget(metadata) # Pass initial data from the JSON file
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.setObjectName("TableInterface")
        
        
        
        # Create a timer to periodically update the table data
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTableData)
        self.timer.start(1500)  # Set the update interval (in milliseconds)
        
        
        # Initial data update
        self.updateTableData()
        
        
        # Save Button
        self.saveButton = PrimaryPushButton('Save', self, FluentIcon.SAVE)
        self.saveButton.clicked.connect(self.saveData)  # Connect the button click to the saveData method
        
        

        # self.saveButton.clicked.connect(createSuccessInfoBar)
        self.layout.addWidget(self.saveButton)

    def updateTableData(self):
        # Reload data from the JSON file and update the table widget
        new_metadata = json.load(open('GradeVision/app/view\JSON/meta.json'))
        self.tableWidget.updateData(new_metadata)



    def saveData(self):
        # Call the save_table_data_to_json method from CustomTableWidget
        self.tableWidget.save_table_data_to_json('GradeVision/app/view\JSON\output.json')  # Save to 'output.json'

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

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.button = PrimaryPushButton("Select Folder", self, FluentIcon.FOLDER)
        self.button.clicked.connect(self.openFileDialog)

        # self.sublabel = SubtitleLabel("", self)  # Initialize with an empty string
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        # layout.addWidget(self.sublabel, alignment=Qt.AlignCenter)
        # layout.addWidget(self.progressRing, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.setObjectName("FolderInterface")
        
    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        

        
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options) 
        #write the folder path to a json file
        with open("GradeVision/app/view\JSON/folder_path.json", "w") as f:
            f.write(json.dumps(folder_path))
        
        print("Selected Folder:", folder_path)
        
        total_images = len(glob.glob(folder_path + "/*.tif"))
        print("Total Images:", total_images)
        
        
        if total_images == 0:
            InfoBar.error(
                title='Error',
                content=f'Folder has no images',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3400,
                parent=self
            )
        elif folder_path:
            #remove the button
            self.button.hide()
            # self.setAttribute(Qt.WA_TranslucentBackground)
            self.label = LargeTitleLabel('Image Viewer', self)
            self.note = CaptionLabel('Note: the speed or the lag of the preview is caused by the high image resulotion ', self)
            langbutton = PrimaryPushButton("Select Language", self, FluentIcon.LANGUAGE)
            def LangDialog():
                view = FlyoutView(
                    title='Select Language',
                    content="Select the language of the sheet format you want to grade (left to right or right to left)",
                    isClosable=True
                    # image='GradeVision/app/resource\images\Singer.png',
                    # image='resource/yiku.gif',
                )
                # add radio buttons
                radio_button1 = RadioButton('Arabic', parent=view)
                radio_button2 = RadioButton('English', parent=view)
                # radio_button1.setChecked(True)
                
                def writeToJson(lang):
                    with open("GradeVision/app/view\JSON\lang.json", "w") as f:
                        f.write(json.dumps(lang))
                    print("Selected Language:", lang)
                    # view.close()
                radio_button1.toggled.connect(lambda: writeToJson("Arabic"))
                radio_button2.toggled.connect(lambda: writeToJson("English"))
                view.addWidget(radio_button1, align=Qt.AlignCenter)
                view.addWidget(radio_button2, align=Qt.AlignCenter)

                # adjust layout (optional)
                view.widgetLayout.insertSpacing(1, 5)
                view.widgetLayout.addSpacing(5)
                def closeinfo():
                    lang = json.load(open('GradeVision/app/view\JSON\lang.json'))
                    InfoBar.success(title='Language Selected',content=f'Language has been set to {lang}',
                                        orient=Qt.Horizontal,isClosable=True,position=InfoBarPosition.TOP,
                                        duration=2300,parent=self)
                # show view
                w = Flyout.make(view, langbutton)
                view.closed.connect(w.close)
                view.closed.connect(closeinfo)
                
            langbutton.clicked.connect(LangDialog)
            
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
            image_paths = [str(i) for i in Path(folder_path).glob('*')][:10]
            self.flipView.addImages(image_paths, targetSize=QSize(1000, 1000))
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
            # self.layout().addWidget(self.note, 0, Qt.AlignCenter)
            self.layout().addWidget(langbutton, 0, Qt.AlignCenter)
            self.layout().setAlignment(Qt.AlignCenter)
            self.layout().setSpacing(20)
            self.resize(600, 600)
                
                
            InfoBar.success(
                title='Folder Selected, Showing 10 images',
                content=f'Folder has {total_images} images',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3400,
                parent=self
            )
            
        elif folder_path == "":
            InfoBar.error(
                title='Error',
                content=f'No folder selected',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3400,
                parent=self
            )




class Core(QWidget):


    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet("""
        #     Demo{background: white}
        #     QLabel{
        #         font: 20px 'Segoe UI';
        #         background: rgb(242,242,242);
        #         border-radius: 8px;
        #     }
        # """)
        self.resize(400, 400)
        
        
        
        self.tabWidget = SegmentedToggleToolWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        
        self.stacked_widget = QStackedWidget(self)
        

        self.FolderSelectionInterface = FolderSelectionWidget()
        
        # folder_path = json.load(open('JSON/folder_path.json'))
        
        self.gradingInterface = GradingApp(self.stacked_widget)
        
        # self.artistInterface = QLabel('GitHub Interface', self)

        self.stacked_widget.addWidget(self.gradingInterface)
        # add items to pivot
        self.addSubInterface(self.FolderSelectionInterface, 'videoInterface', FluentIcon.FOLDER_ADD)
        self.addSubInterface(self.stacked_widget, 'albumInterface', FluentIcon.CALORIES)
        # self.addSubInterface(self.artistInterface, 'githubInterface', 'GitHub', FluentIcon.GITHUB)

        self.vBoxLayout.addWidget(self.tabWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        
        
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.FolderSelectionInterface)
        self.tabWidget.setCurrentItem(self.FolderSelectionInterface.objectName())
        self.setObjectName("Demo")
        
    def addSubInterface(self, widget: QLabel, objectName, icon):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)
        self.tabWidget.addItem(
            routeKey=objectName,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
            icon=icon
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.tabWidget.setCurrentItem(widget.objectName())






class Window(FluentWindow):

    def __init__(self):
        super().__init__()
        
        # create sub interface
        self.homeInterface = RegionSelection()
        self.appInterface = TableWidget()
        self.videoInterface = Core()
        self.libraryInterface = CheckRes()
        self.settingInterface = SettingInterface(self)
        
        self.analyticsInterface = GraphWindow(parent=self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, 'Main')
        self.addSubInterface(self.appInterface, FluentIcon.APPLICATION, 'Answer Key')
        self.addSubInterface(self.videoInterface, FluentIcon.VIDEO, 'Start')
        self.addSubInterface(self.analyticsInterface, FluentIcon.IOT, 'Analytics')
        self.addSubInterface(self.libraryInterface, FluentIcon.ALIGNMENT, 'Check Results', NavigationItemPosition.BOTTOM)

        self.addSubInterface(
    self.settingInterface, FluentIcon.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

        
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FluentIcon.HELP,
            text='info',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        
        self.splashScreen.setIconSize(QSize(102, 102))
        self.splashScreen.show()
        QTimer.singleShot(2500, self.splashScreen.close) #2500

        self.resize(1000, 750)
        self.setWindowTitle('GradVision')
        self.updateFrameless()
        self.setMicaEffectEnabled(True)
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        
        

    def showMessageBox(self):
        w = MessageBox(
            'debug🥰',
            'if you like this project and find it helpful, please consider giving it a star on my github repository and sharing it with others who might benefit from it',
            self
        )
        w.yesButton.setText('visit my github')
        w.yesButton.setIcon(FluentIcon.GITHUB)
        
        w.cancelButton.setText('cancel')
        

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/AliMostafaRadwan"))

    # setTheme(Theme.DARK)

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # setThemeColor('#00CDFF')

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()

    if not app.closingDown():  # Check if the app is closed
        with open("GradeVision/app/view/JSON/folder_path.json", "w") as f:
            f.write(json.dumps(''))  # Clear the data in the folder_path.json