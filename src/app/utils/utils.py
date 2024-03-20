import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator
from PyQt5.QtCore import Qt, QTranslator

def setup_dpi_scaling(config):
    if config.get("dpi_scale") == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(config.get("dpi_scale"))

def setup_internationalization(app, config):
    locale = config.get("language")
    translator = FluentTranslator(locale)
    app.installTranslator(translator)

def load_translations(app):
    translator = QTranslator()
    translation_file_path = "app/resources/i18n/gallery.qm"
    if translator.load(translation_file_path):
        app.installTranslator(translator)
    else:
        print(f"Failed to load translation file: {translation_file_path}")