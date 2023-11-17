import sys
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager




def createSuccessInfoBar(self):
    # convenient class mothod
    InfoBar.success(
        title='Lesson 4',
        content="With respect, let's advance towards a new stage of the spin.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        # position='Custom',   # NOTE: use custom info bar manager
        duration=2000,
        parent=self
    )