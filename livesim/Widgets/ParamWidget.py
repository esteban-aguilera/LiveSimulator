# coding: utf-8
# !/usr/bin/env python

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit

Pi, E, Sqrt, Exp, Log = np.pi, np.e, np.sqrt, np.exp, np.log
Sin, Sinh, Arcsin, Asin = np.sin, np.sinh, np.arcsin, np.arcsin
Cos, Cosh, Arccos, Acos = np.cos, np.cosh, np.arccos, np.arccos
Tan, Tanh, Arctan, Atan = np.tan, np.tanh, np.arctan, np.arctan


class ParamWidget(QWidget):

    def __init__(self, name, value):
        super().__init__()
        self.Label = None
        self.Edit = None

        self.setFixedWidth(300)
        self.createUI(name, value)

    def createUI(self, name, value):
        self.Label = QLabel(name, alignment=Qt.AlignCenter)
        self.Label.setFont(QFont("Times", 16, QFont.Bold))

        self.Edit = QLineEdit(str(value))
        self.Edit.setFont(QFont("Times", 14))

        hlayout = QHBoxLayout(self)
        hlayout.addWidget(self.Label)
        hlayout.addWidget(self.Edit)

    def get_value(self):
        _locals = locals()
        command = "x = %s" % self.Edit.text()
        for r in [("^", "**")]:
            command = command.replace(r[0], r[1])
        exec(command, globals(), _locals)
        return _locals["x"]
