# coding: utf-8
# !/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import random

from multiprocessing import Value
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, \
    QComboBox, QTabWidget
from livesim.Widgets.FigureWidget import *
from livesim.Widgets.ParamWidget import *
from livesim.Widgets.SaveDialog import *
from .Bidimensional_Complex_Field_Figure import *


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

    def set_Aij(self, i, j):
        x_dim, y_dim = 3, 3
        for m in np.arange(i-x_dim//2, i+x_dim//2+0.5):
            for n in np.arange(j-y_dim//2, j+y_dim//2+0.5):
                self.A[int(m), int(n)] = self.setter_widget.get_value()

        self.figure_widget.plot(self.A)

    def winding_number(self, x1, x2, y1, y2):
        theta = np.angle(self.A)
        w = 0  # countour integral value arround p

        nx_min = x1 if (x1>0) else 0
        nx_max = x2 if (x2<np.shape(self.A)[0]-2) else np.shape(self.A)[0]-2
        ny_min = y1 if (y1>0) else 0
        ny_max = y2 if (y2<np.shape(self.A)[1]-2) else np.shape(self.A)[1]-2

        for ix in range(nx_min, nx_max):
            w += theta[ix+1, ny_min]-theta[ix, ny_min]
            w += theta[ix, ny_max]-theta[ix+1, ny_max]

            if((theta[ix+1, ny_min]-theta[ix, ny_min]) > .99 * np.pi):
                w += 2.0 * np.pi
            elif((theta[ix+1, ny_min]-theta[ix, ny_min]) < -.99 * np.pi):
                w -= 2.0 * np.pi

            if((theta[ix, ny_max]-theta[ix+1, ny_max]) > .99 * np.pi):
                w += 2.0 * np.pi
            elif((theta[ix, ny_max]-theta[ix+1, ny_max]) < -.99 * np.pi):
                w -= 2.0 * np.pi

        for iy in range(ny_min, ny_max):
            w += theta[nx_max, iy+1]-theta[nx_max, iy]
            w += theta[nx_min, iy]-theta[nx_min, iy+1]

            if((theta[nx_max, iy+1]-theta[nx_max, iy]) > .99 * np.pi):
                w += 2.0 * np.pi
            elif((theta[nx_max, iy+1]-theta[nx_max, iy]) < -.99 * np.pi):
                w -= 2.0 * np.pi

            if((theta[nx_min, iy]-theta[nx_min, iy+1]) > .99 * np.pi):
                w += 2.0 * np.pi
            elif((theta[nx_min, iy]-theta[nx_min, iy+1]) < -.99 * np.pi):
                w -= 2.0 * np.pi

        return w / (2.0*np.pi)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # figure interaction methods
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def figClickPress(self, event):
        self.original_play = self.play
        self.fig_clicked = True
        self.play = False
        while(self.conn.poll()):
            self.conn.recv()

        i, j = int(event.xdata + 0.5), int(event.ydata + 0.5)
        self.A = self.figure_widget.A
        if(self.tabs.currentIndex() == 0):  # set A
            self.set_Aij(i, j)
        elif(self.tabs.currentIndex() == 1):  # winding number
            self.x1, self.y1 = i, j

    def figMotion(self, event):
        if(self.fig_clicked):
            i, j = int(event.xdata + 0.5), int(event.ydata + 0.5)
            if(self.tabs.currentIndex() == 0):  # set A
                self.set_Aij(i, j)
            elif(self.tabs.currentIndex() == 1):  # winding number
                self.figure_widget.drawRectangle(self.x1, i, self.y1, j)

    def figClickRelease(self, event):
        if(self.tabs.currentIndex() == 0):
            self.conn.send(self.A)
        elif(self.tabs.currentIndex() == 1):
            x1, y1 = self.x1, self.y1
            x2, y2 = int(event.xdata + 0.5), int(event.ydata + 0.5)
            wn = 0
            if(x1 < x2):
                if(y1 < y2):
                    wn = self.winding_number(x1, x2, y1, y2)
                else:
                    wn = self.winding_number(x1, x2, y2, y1)
            else:
                if(y1 < y2):
                    wn = self.winding_number(x2, x1, y1, y2)
                else:
                    wn = self.winding_number(x2, x1, y2, y1)
            self.wn_label.setText("Winding Number: %.5f" % wn)

        self.figure_widget.removeRectangle()
        self.fig_clicked = False
        self.play = self.original_play


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # user interface methods
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createUI(self):
        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignTop)

        # top layout
        self.save_widget = self.createSaveWidget()
        self.z_axis_widget = self.createZAxisWidget()

        hlayout_top = QHBoxLayout()
        hlayout_top.addWidget(self.save_widget)
        hlayout_top.addWidget(self.z_axis_widget)
        hlayout_top.setAlignment(Qt.AlignLeft)
        vlayout.addLayout(hlayout_top)

        # figure
        self.figure_widget = Bidimensional_Complex_Field_Figure(
            self.conn, self._play, dir=self.dir)
        self.figure_widget.fig.canvas.mpl_connect('button_press_event',
                                                  self.figClickPress)
        self.figure_widget.fig.canvas.mpl_connect('motion_notify_event',
                                                  self.figMotion)
        self.figure_widget.fig.canvas.mpl_connect('button_release_event',
                                                  self.figClickRelease)
        vlayout.addWidget(self.figure_widget)

        # bottom layout
        self.setter_widget = ParamWidget("A =", "0 + 0j")
        self.wn_label = QLabel("Select Area to Calculate Winding Number",
            alignment=Qt.AlignCenter)
        self.wn_label.setFont(QFont("Times", 14))

        self.tabs = QTabWidget()
        self.tabs.addTab(self.setter_widget, "Set A")
        self.tabs.addTab(self.wn_label, "Winding Number")
        self.tabs.setFixedHeight(100)

        hlayout_bottom = QHBoxLayout()
        hlayout_bottom.addWidget(self.tabs)
        vlayout.addLayout(hlayout_bottom)

        self.setLayout(vlayout)

    def createSaveWidget(self):
        def saveClicked():
            original_play = self.play
            self.play = False
            def save():
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

    def createZAxisWidget(self):
        def PlotViewClicked(i):
            self.figure_widget.im = None
            self.figure_widget.z_axis_index = i
            self.figure_widget.plot(self.figure_widget.A)

        cb = QComboBox()
        cb.addItems(Z_AXIS_OPTIONS)
        cb.setFont(QFont("Times", 12))
        cb.currentIndexChanged.connect(PlotViewClicked)

        return cb

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
