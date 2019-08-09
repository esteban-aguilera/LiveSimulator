# coding: utf-8
# !/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import random

from multiprocessing import Value
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox
from livesim.Widgets.FigureWidget import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# constants
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Z_AXIS_OPTIONS = ["Abs", "Arg", "Re*Im", "Re", "Im"]
Z_AXIS = Z_AXIS_OPTIONS[0]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class PlotWidget(QWidget):

    def __init__(self, conn, _play, dir=""):
        super().__init__()

        self.conn, self._play = conn, _play
        self.figure_widget = None

        self.createUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # user interface functions
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createUI(self):
        self.figure_widget = FigureWidget(self.conn, self._play)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.figure_widget)
        self.setLayout(vlayout)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # properties
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def play(self):
        return self._play.value

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # setters
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @play.setter
    def play(self, value):
        self._play.value = value
