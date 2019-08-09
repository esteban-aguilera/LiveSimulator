# coding: utf-8
# !/usr/bin/env python

import numpy as np

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel


class PlaySpeedWidget(QWidget):

    def __init__(self, play=False, speed=1):
        super().__init__()
        self.createUI()

        self.play = play
        self.speed = speed

    def createUI(self):
        self.PlayButton = QPushButton(" ")
        self.PlayButton.setFont(QFont("Times", 16, QFont.Bold))

        self.SpeedButton = QPushButton(" ")
        self.SpeedButton.setFont(QFont("Times", 16, QFont.Bold))

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.PlayButton)
        hlayout.addWidget(self.SpeedButton)
        self.setLayout(hlayout)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # properties
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def play(self):
        return self._play

    @property
    def speed(self):
        return self._speed

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # setters
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @play.setter
    def play(self, value):
        self._play = value
        if(self._play is True):
            self.PlayButton.setText(u"⏸")
        else:
            self.PlayButton.setText(u"▶")

    @speed.setter
    def speed(self, value):
        if(value > 4 or value < 0 or value == 1):
            self._speed = 1
            self.SpeedButton.setText(u"⏩" )
        else:
            self._speed = value
            self.SpeedButton.setText(u"⏩ × %d" % value)
