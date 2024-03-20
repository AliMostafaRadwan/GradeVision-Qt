import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme

from app.config import Config
from app.utils import setup_internationalization, load_translations, setup_dpi_scaling
from app.views.main_window import MainWindow
from app.controllers.grading_controller import GradingController

def main():
    app = QApplication(sys.argv)
    setup_application(app)

    config = Config()
    setup_dpi_scaling(config)
    setup_internationalization(app, config)
    load_translations(app)

    main_window = MainWindow()
    grading_controller = GradingController(main_window)
    main_window.show()

    sys.exit(app.exec_())

def setup_application(app):
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    setTheme(Theme.DARK)

if __name__ == "__main__":
    main()