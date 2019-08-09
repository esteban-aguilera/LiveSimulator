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
from .Unidimensional_Complex_Field_Figure import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Unidimensional_Complex_Field_Plotter(QWidget):

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
        i = int(event.xdata + 0.5)
        self.set_Ai(i)

    def figMotion(self, event):
        if(self.fig_clicked):
            i = int(event.xdata + 0.5)
            self.set_Ai(i)

    def figClickRelease(self, event):
        self.conn.send(self.A)
        self.fig_clicked = False
        self.play = self.original_play

    def set_Ai(self, i):
        x_dim = 5
        for n in np.arange(i-x_dim//2, i+x_dim//2+0.5):
            self.A[int(n)] = self.setter_widget.get_value()
        self.figure_widget.plot(self.A)

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
        self.figure_widget = Unidimensional_Complex_Field_Figure(
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
            self.figure_widget.ln = None
            self.figure_widget.ln_re = None
            self.figure_widget.ln_im = None
            self.figure_widget.im = None
            self.figure_widget.z_axis_index = i

        cb = QComboBox()
        cb.addItems(PLOT_OPTIONS)
        cb.setFont(QFont("Times", 12))
        cb.currentIndexChanged.connect(PlotViewClicked)

        return cb

    def createSaveWidget(self):
        def saveClicked():
            original_play = self.play
            self.play = False
            def save():
                fname = save_dialog.line_edit.text()
                fname = save_dialog.line_edit.text()
                if(save_dialog.extension() == "dat"):
                    self.figure_widget.save_state(fname)
                else:
                    self.figure_widget.fig.savefig(
                        "%s.%s" % (fname, save_dialog.extension()))
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
