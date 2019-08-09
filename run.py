# coding: utf-8
# !/usr/bin/env python

from PyQt5.QtWidgets import QApplication
import sys
from livesim import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())
