# coding: utf-8
# !/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import random

from multiprocessing import Value
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox
from livesim.Widgets.FigureWidget import *
from livesim.Widgets.ParamWidget import *
from livesim.Widgets.SaveDialog import *
from .Bidimensional_Complex_Field_Figure import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# constants
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Z_AXIS_OPTIONS = ["Abs", "Arg", "Re*Im", "Re", "Im"]
Z_AXIS = Z_AXIS_OPTIONS[0]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Bidimensional_Complex_Field_Plotter(QWidget):

    def __init__(self, conn, _play, dir=""):
        super().__init__()
        self.dir = dir
        self.conn, self._play = conn, _play

        self.figure_widget = None
        self.setter_widget = None

        self.fig_clicked = False

        self.createUI()

    def figClickPress(self, event):
        self.original_play = self.play
        self.fig_clicked = True
        self.play = False
        while(self.conn.poll()):
            self.conn.recv()

        self.A, self.eps = self.figure_widget.A, self.figure_widget.eps
        i, j = int(event.xdata + 0.5), int(event.ydata + 0.5)
        self.set_Aij(i, j)

    def figMotion(self, event):
        if(self.fig_clicked):
            i, j = int(event.xdata + 0.5), int(event.ydata + 0.5)
            self.set_Aij(i, j)

    def figClickRelease(self, event):
        self.conn.send(self.A)
        self.fig_clicked = False
        self.play = self.original_play

    def set_Aij(self, i, j):
        x_dim, y_dim = 3, 3
        for m in np.arange(i-x_dim//2, i+x_dim//2+0.5):
            for n in np.arange(j-y_dim//2, j+y_dim//2+0.5):
                self.A[int(m), int(n)] = self.setter_widget.get_value()

        if(Z_AXIS_OPTIONS[self.figure_widget.z_axis_index] == "Abs"):
            self.figure_widget.im.set_data(np.abs(self.A.T))
        elif(Z_AXIS_OPTIONS[self.figure_widget.z_axis_index] == "Arg"):
            self.figure_widget.im(np.angle(self.A.T))
        elif(Z_AXIS_OPTIONS[self.figure_widget.z_axis_index] == "Re*Im"):
            self.figure_widget.im(np.real(self.A.T) * np.imag(self.A.T))
        elif(Z_AXIS_OPTIONS[self.figure_widget.z_axis_index] == "Re"):
            self.figure_widget.im(np.real(self.A.T))
        elif(Z_AXIS_OPTIONS[self.figure_widget.z_axis_index] == "Im"):
            self.figure_widget.im(np.imag(self.A.T))

        self.figure_widget.draw()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # user interface functions
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createUI(self):
        # top layout
        self.save_widget = self.createSaveWidget()

        hlayout_top = QHBoxLayout()
        hlayout_top.addWidget(self.save_widget)
        hlayout_top.setAlignment(Qt.AlignLeft)

        # bottom layout
        self.figure_widget = Bidimensional_Complex_Field_Figure(
            self.conn, self._play, dir=self.dir)
        self.figure_widget.fig.canvas.mpl_connect('button_press_event',
                                                  self.figClickPress)
        self.figure_widget.fig.canvas.mpl_connect('motion_notify_event',
                                                  self.figMotion)
        self.figure_widget.fig.canvas.mpl_connect('button_release_event',
                                                  self.figClickRelease)
        self.setter_widget = ParamWidget("A =", "0 + 0j")
        self.z_axis_widget = self.createZAxisWidget()

        hlayout_bottom = QHBoxLayout()
        hlayout_bottom.addWidget(self.setter_widget)
        hlayout_bottom.addWidget(self.z_axis_widget)

        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignTop)

        vlayout.addLayout(hlayout_top)
        vlayout.addWidget(self.figure_widget)
        vlayout.addLayout(hlayout_bottom)
        self.setLayout(vlayout)

    def createZAxisWidget(self):
        def PlotViewClicked(i):
            self.figure_widget.im = None
            self.figure_widget.z_axis_index = i

        cb = QComboBox()
        cb.addItems(Z_AXIS_OPTIONS)
        cb.setFont(QFont("Times", 12))
        cb.currentIndexChanged.connect(PlotViewClicked)

        return cb

    def createSaveWidget(self):
        def saveClicked():
            original_play = self.play
            self.play = False
            def save():
                fname = save_dialog.line_edit.text()
                self.figure_widget.plot(fname)
                save_dialog.close()
                self.play = original_play

            save_dialog = SaveDialog()
            save_dialog.line_edit.returnPressed.connect(save)
            save_dialog.ok_btn.clicked.connect(save)
            save_dialog.show()

        save_button = QPushButton(QIcon("%s/save_icon.png" % DIR), "")
        save_button.setIconSize(QSize(30, 30))
        save_button.setStyleSheet('QPushButton{border: 0px solid;}')
        save_button.clicked.connect(saveClicked)

        return save_button

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
