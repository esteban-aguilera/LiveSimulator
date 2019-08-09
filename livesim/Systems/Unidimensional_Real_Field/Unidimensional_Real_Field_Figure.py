# coding: utf-8
# !/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import os
import random

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox
from livesim.Widgets.FigureWidget import *
from livesim.Widgets.ParamWidget import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# constants
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Z_AXIS_OPTIONS = ["Abs", "Arg", "Re*Im", "Re", "Im"]
DIR_FIGURE = os.path.dirname(__file__)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Bidimensional_Complex_Field_Figure(FigureWidget):

    def __init__(self, conn, _play, dir=""):
        self.dir= "%s/%s" % (os.path.dirname(__file__), dir)
        self.z_axis_index = 0

        self.A, self.t, self.eps = None, None, None
        self.im = None

        super().__init__(conn, _play, dir=dir)

    def plot(self, data):
        if(len(data) == 3):
            self.A, self.t, self.eps = data
        elif(len(np.shape(data)) == 2):
            self.A, self.t = data
        else:
            if(type(data) == str):
                np.savetxt("%s/saved_states/%s" % (self.dir, data), self.A.view(float))
            else:
                self.A = data
        if(self.im is None):
            self.ax.cla()
            if(Z_AXIS_OPTIONS[self.z_axis_index] == "Abs"):
                self.im = self.ax.imshow(np.abs(self.A.T),
                    origin="lower", cmap=plt.get_cmap("OrRd"),
                    vmin=0, vmax=np.sqrt(self.eps))
            elif(Z_AXIS_OPTIONS[self.z_axis_index] == "Arg"):
                self.im = self.ax.imshow(np.angle(self.A.T),
                    origin="lower", cmap=plt.get_cmap("gist_gray"),
                    vmin=-np.pi, vmax=np.pi)
            elif(Z_AXIS_OPTIONS[self.z_axis_index] == "Re*Im"):
                self.im = self.ax.imshow(np.real(self.A) * np.imag(self.A),
                    origin="lower", cmap=plt.get_cmap("seismic"),
                    vmin=-np.sqrt(self.eps), vmax=np.sqrt(self.eps))
            elif(Z_AXIS_OPTIONS[self.z_axis_index] == "Re"):
                self.im = self.ax.imshow(np.real(self.A),
                    origin="lower", cmap=plt.get_cmap("seismic"),
                    vmin=-np.sqrt(self.eps), vmax=np.sqrt(self.eps))
            elif(Z_AXIS_OPTIONS[self.z_axis_index] == "Im"):
                self.im = self.ax.imshow(np.imag(self.A),
                    origin="lower", cmap=plt.get_cmap("seismic"),
                    vmin=-np.sqrt(self.eps), vmax=np.sqrt(self.eps))

            self.ax.set_xlabel("$x$ (u.a.)", fontsize=15)
            self.ax.set_ylabel("$y$ (u.a.)", fontsize=15)
            self.txt = self.ax.text(
                .95*self.ax.get_xlim()[1], 0.95*self.ax.get_ylim()[1],
                "$t=%.3f$" % self.t, fontsize=12, va="top", ha="right",
                multialignment="left", bbox={'facecolor': 'white', 'alpha': .9})
            self.ax.grid()
        else:
            if(Z_AXIS_OPTIONS[self.z_axis_index] == "Abs"):
                self.im.set_data(np.abs(self.A.T))
            elif(Z_AXIS_OPTIONS[self.z_axis_index] == "Arg"):
                self.im.set_data(np.angle(self.A.T))
            elif(Z_AXIS_OPTIONS[self.z_axis_index] == "Re*Im"):
                self.im.set_data(np.real(self.A.T)*np.imag(self.A.T))
            elif(Z_AXIS_OPTIONS[self.z_axis_index] == "Re"):
                self.im.set_data(np.real(self.A.T))
            elif(Z_AXIS_OPTIONS[self.z_axis_index] == "Im"):
                self.im.set_data(np.imag(self.A.T))
            self.txt.set_text("$t=%.3f$" % self.t)
        self.draw()
