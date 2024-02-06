# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator, setTheme, setThemeColor, Theme

from app.common.config import cfg
from app.view.main_window import Window
import json


# enable dpi scale
if cfg.get(cfg.dpiScale) == "Auto":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)


if __name__ == "__main__":
    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    # setThemeColor('#00CDFF')
    setTheme(Theme.DARK)
    
    # internationalization
    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)
    galleryTranslator = QTranslator()
    galleryTranslator.load(locale, "GradeVision", ".", ":/GradeVision/app/resource/i18n")
    # print(cfg.language.value)
    app.installTranslator(translator)
    app.installTranslator(galleryTranslator)
    
    # create main window
    window = Window()
    window.show()

    # run application
    if not app.closingDown():  # Check if the app is closed
        with open("GradeVision/app/view\JSON/folder_path.json", "w") as f:
            f.write(json.dumps(''))  # Clear the data in the folder_path.json

    sys.exit(app.exec_())
