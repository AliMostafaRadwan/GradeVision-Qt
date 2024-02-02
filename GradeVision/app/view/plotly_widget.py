
# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qmaterialwidgets import (OutlinedPushButton, Flyout, InfoBarIcon, setTheme, Theme, FlyoutView, FlyoutViewBase,
                            BodyLabel, setFont, FlyoutAnimationType, FilledPushButton, palette)
from qfluentwidgets import ComboBox

class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet("Demo{background:"+palette.surface.name()+"}")

        self.vBoxLayout = QHBoxLayout(self)
        self.button2 = OutlinedPushButton('Click Me', self)

        self.resize(750, 550)
        self.button2.setFixedWidth(150)
        self.vBoxLayout.addWidget(self.button2, 0, Qt.AlignBottom)
        self.vBoxLayout.setContentsMargins(30, 50, 30, 50)


        self.button2.clicked.connect(self.showFlyout2)


 
    def showFlyout2(self):
        view = FlyoutView(
            title='杰洛·齐贝林',
            content="触网而起的网球会落到哪一侧，谁也无法知晓。\n如果那种时刻到来，我希望「女神」是存在的。\n这样的话，不管网球落到哪一边，我都会坦然接受的吧。",
            image='resource/SBR.jpg',
            isClosable=True
            # image='resource/yiku.gif',
        )

        # add combo box
        combo = ComboBox(self)
        items = ['Item 1', 'Item 2', 'Item 3']
        combo.addItems(items)
        combo.setCurrentIndex(0)
        combo.setFixedWidth(140)
        view.addWidget(combo,align=Qt.AlignRight)
        

        # adjust layout (optional)
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.addSpacing(5)

        # show view
        w = Flyout.make(view, self.button2, self)
        view.closed.connect(w.close)

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()