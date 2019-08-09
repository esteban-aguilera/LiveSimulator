# coding: utf-8
# !/usr/bin/env python

import os
from multiprocessing import Value
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from .ParamWidget import *
from .PlaySpeedWidget import *

DIR = os.path.dirname(__file__)


class EquationWidget(QWidget):

    def __init__(self, conn, _play):
        super().__init__()
        self.dir = os.path.dirname(__file__)

        self.conn = conn
        self._params = []  # [Value('d', float) for _ in range(N_params)]
        self.param_strs = []  # [str for _ in range(N_params)]
        self._play = _play
        self._speed = Value('i', 1)

        self.vlayout = QVBoxLayout()
        self.vlayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.vlayout)
        self.setFixedWidth(300)

    def createUI(self):
        self.clearWidget()

    def plot(self):
        pass

    def read_conn(self):
        pass

    def readParams(self):
        self.params = [w.get_value() for w in self.param_widgets]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # user interface functions
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createTitleWidget(self):
        titleWidget = QLabel(self.__class__.__name__.replace("_", " "))
        titleWidget.setFont(QFont("Times", 16, QFont.Bold))

        vd = QLabel(" ")
        vd.setFont(QFont("Times", 16, QFont.Bold))

        self.vlayout.addWidget(titleWidget, alignment=Qt.AlignTop)
        self.vlayout.addWidget(vd, alignment=Qt.AlignTop)

    def createParamWidgets(self):
        self.param_widgets = [None] * len(self.param_strs)
        for i in range(len(self.param_strs)):
            self.param_widgets[i] = ParamWidget(self.param_strs[i], self.params[i])
            self.param_widgets[i].Edit.returnPressed.connect(self.readParams)
            self.vlayout.addWidget(self.param_widgets[i], alignment=Qt.AlignTop)

    def createPlaySpeedWidget(self):
        def playClicked():
            play_speed_widget.play = not play_speed_widget.play
            self.play = play_speed_widget.play
            self.readParams()

        def speedClicked():
            play_speed_widget.speed += 1
            self.speed = play_speed_widget.speed
            self.readParams()

        play_speed_widget = PlaySpeedWidget()
        play_speed_widget.PlayButton.clicked.connect(playClicked)
        play_speed_widget.SpeedButton.clicked.connect(speedClicked)
        self.vlayout.addWidget(play_speed_widget, alignment=Qt.AlignTop)

    def clearWidget(self):
        while self.vlayout.count():
            child = self.vlayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # properties
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def simulating(self):
        return self._simulating.value

    @property
    def play(self):
        return self._play.value

    @property
    def speed(self):
        return self._speed.value

    @property
    def params(self):
        return [param_value.value for param_value in self._params]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # setters
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @simulating.setter
    def simulating(self, value):
        self._simulating.value = value

    @play.setter
    def play(self, value):
        self._play.value = value

    @speed.setter
    def speed(self, value):
        self._speed.value = value

    @params.setter
    def params(self, values):
        if(len(self._params) == 0):
            self._params = [None] * len(values)
            for k in range(len(values)):
                self._params[k] = Value('d', values[k])
        else:
            for k in range(len(values)):
                self._params[k].value = values[k]
                self.param_widgets[k].Edit.setText("%s" % values[k])
