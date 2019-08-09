# coding: utf-8
# !/usr/bin/env python

import os

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

DIR = os.path.dirname(__file__)


class FigureWidget(FigureCanvas):
    def __init__(self, conn, _play, dir=""):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.conn, self._play = conn, _play

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerFunction)
        if(dir == ""):
            pass
        else:
            self.timer.start(30)

    def plot(self, data, save=False):
        pass

    def timerFunction(self):
        if(self.conn.poll()):
            data = self.conn.recv()
            self.plot(data)

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
