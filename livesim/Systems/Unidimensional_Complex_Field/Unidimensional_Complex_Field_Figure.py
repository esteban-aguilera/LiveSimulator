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
PLOT_OPTIONS = ["Abs", "Arg", "Re & Im", "T vs Abs", "T vs Re", "T vs Im"]
DIR_FIGURE = os.path.dirname(__file__)
NUM_IT = 500


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Unidimensional_Complex_Field_Figure(FigureWidget):

    def __init__(self, conn, _play, dir=""):
        self.dir= "%s/%s" % (os.path.dirname(__file__), dir)
        self.z_axis_index = 0

        self.A, self.t, self.x, self.eps = None, None, None, None
        self.real_arr, self.imag_arr, self._it = None, None, 1
        self.ln, self.ln_real, self.ln_imag = None, None, None
        self.im, self.cb = None, None

        super().__init__(conn, _play, dir=dir)

    def plot(self, data):
        if(len(data) == 4):
            self.A, self.t, self.x, self.eps = data
        elif(np.size(data) == 2):
            print(data)
            self.A, self.t, self.x = data
        else:
            self.A = data
        self.x = [i for i in range(len(self.x))]

        if(self.real_arr is None):
            self.real_arr = np.array([np.real(self.A)] * NUM_IT)
            self.imag_arr = np.array([np.imag(self.A)] * NUM_IT)
        else:
            self.real_arr[self.it] = np.real(self.A)
            self.imag_arr[self.it] = np.imag(self.A)
            self.it += 1

        if(self.z_axis_index == 0):
            if(self.ln is None):
                self.ax.remove()
                self.ax = self.fig.add_subplot(111)

                self.ln, = self.ax.plot(self.x, np.abs(self.A.T))
                self.ln_real, self.ln_imag, self.im = None, None, None

                self.ax.set_xlim([self.x[0], self.x[-1]])
                self.ax.set_ylim([0, 1.2])
                self.ax.set_xlabel("$x$ (u.a.)", fontsize=15)
                self.ax.set_ylabel("$|A|$ (u.a.)", fontsize=15)
                self.txt = self.ax.text(
                    .95*self.ax.get_xlim()[1], 0.95*self.ax.get_ylim()[1],
                    "$t=%.3f$" % self.t, fontsize=12, va="top", ha="right",
                    multialignment="left", bbox={'facecolor': 'white', 'alpha': .9})
                self.ax.grid()

                if(self.cb is not None):
                    self.cb.remove()
                    self.cb = None
                self.fig.tight_layout()
            else:
                self.ln.set_ydata(np.abs(self.A))
                self.txt.set_text("$t=%.3f$" % self.t)
        elif(self.z_axis_index == 1):
            if(self.ln is None):
                self.ax.remove()
                self.ax = self.fig.add_subplot(111)

                self.ln, = self.ax.plot(self.x, np.angle(self.A.T))
                self.ln_real, self.ln_imag, self.im = None, None, None

                self.ax.set_xlim([self.x[0], self.x[-1]])
                self.ax.set_ylim([-np.pi, np.pi])
                self.ax.set_xlabel("$x$ (u.a.)", fontsize=15)
                self.ax.set_ylabel("$arg(A)$ (u.a.)", fontsize=15)
                self.txt = self.ax.text(
                    .95*self.ax.get_xlim()[1], 0.95*self.ax.get_ylim()[1],
                    "$t=%.3f$" % self.t, fontsize=12, va="top", ha="right",
                    multialignment="left", bbox={'facecolor': 'white', 'alpha': .9})
                self.ax.grid()

                if(self.cb is not None):
                    self.cb.remove()
                    self.cb = None
                self.fig.tight_layout()
            else:
                self.ln.set_ydata(np.angle(self.A))
                self.txt.set_text("$t=%.3f$" % self.t)
        elif(self.z_axis_index == 2):
            if(self.ln_real is None or self.ln_imag is None):
                self.ax.remove()
                self.ax = self.fig.add_subplot(111)

                self.ln_real, = self.ax.plot(self.x, np.real(self.A))
                self.ln_imag, = self.ax.plot(self.x, np.imag(self.A))
                self.ln, self.im = None, None

                self.ax.set_xlim([self.x[0], self.x[-1]])
                self.ax.set_ylim([-1.2, 1.2])
                self.ax.set_xlabel("$x$ (u.a.)", fontsize=15)
                self.ax.set_ylabel("$u + iv$ (u.a.)", fontsize=15)
                self.txt = self.ax.text(
                    .95*self.ax.get_xlim()[1], 0.95*self.ax.get_ylim()[1],
                    "$t=%.3f$" % self.t, fontsize=12, va="top", ha="right",
                    multialignment="left", bbox={'facecolor': 'white', 'alpha': .9})
                self.ax.grid()

                if(self.cb is not None):
                    self.cb.remove()
                    self.cb = None
                self.fig.tight_layout()
            else:
                self.ln_real.set_ydata(np.real(self.A))
                self.ln_imag.set_ydata(np.imag(self.A))
                self.txt.set_text("$t=%.3f$" % self.t)
        elif(self.z_axis_index == 3):
            if(self.im is None):
                self.ax.remove()
                self.ax = self.fig.add_subplot(111)

                self.im = self.ax.imshow(
                    np.sqrt(self.real_arr**2 + self.imag_arr**2),
                    origin="lower", cmap=plt.get_cmap("OrRd"),
                    vmin=0, vmax=1)
                self.ln, self.ln_real, self.ln_imag = None, None, None

                self.ax.set_xlabel("$x$ (u.a.)", fontsize=15)
                self.ax.set_ylabel("$t$ (u.a.)", fontsize=15)
                self.txt = self.ax.text(
                    .95*self.ax.get_xlim()[1], 0.95*self.ax.get_ylim()[1],
                    "$t=%.3f$" % self.t, fontsize=12, va="top", ha="right",
                    multialignment="left", bbox={'facecolor': 'white', 'alpha': .9})
                self.ax.grid()

                if(self.cb is not None):
                    self.cb.remove()
                    self.cb = None
                self.cb = self.fig.colorbar(self.im)
                self.fig.tight_layout()
            else:
                self.im.set_data(np.sqrt(self.real_arr**2 + self.imag_arr**2))
                self.txt.set_text("$t=%.3f$" % self.t)
        elif(self.z_axis_index == 4):
            if(self.im is None):
                self.ax.remove()
                self.ax = self.fig.add_subplot(111)

                self.im = self.ax.imshow(self.real_arr,
                    origin="lower", cmap=plt.get_cmap("seismic"),
                    vmin=-1, vmax=1)
                self.ln, self.ln_real, self.ln_imag = None, None, None

                self.ax.set_xlabel("$x$ (u.a.)", fontsize=15)
                self.ax.set_ylabel("$t$ (u.a.)", fontsize=15)
                self.txt = self.ax.text(
                    .95*self.ax.get_xlim()[1], 0.95*self.ax.get_ylim()[1],
                    "$t=%.3f$" % self.t, fontsize=12, va="top", ha="right",
                    multialignment="left", bbox={'facecolor': 'white', 'alpha': .9})
                self.ax.grid()

                if(self.cb is not None):
                    self.cb.remove()
                    self.cb = None
                self.cb = self.fig.colorbar(self.im)
                self.fig.tight_layout()
            else:
                self.im.set_data(self.real_arr)
                self.txt.set_text("$t=%.3f$" % self.t)
        elif(self.z_axis_index == 5):
            if(self.im is None):
                self.ax.remove()
                self.ax = self.fig.add_subplot(111)

                self.im = self.ax.imshow(self.imag_arr,
                    origin="lower", cmap=plt.get_cmap("seismic"),
                    vmin=-1, vmax=1)
                self.ln, self.ln_real, self.ln_imag = None, None, None

                self.ax.set_xlabel("$x$ (u.a.)", fontsize=15)
                self.ax.set_ylabel("$t$ (u.a.)", fontsize=15)
                self.txt = self.ax.text(
                    .95*self.ax.get_xlim()[1], 0.95*self.ax.get_ylim()[1],
                    "$t=%.3f$" % self.t, fontsize=12, va="top", ha="right",
                    multialignment="left", bbox={'facecolor': 'white', 'alpha': .9})
                self.ax.grid()

                if(self.cb is not None):
                    self.cb.remove()
                    self.cb = None
                self.cb = self.fig.colorbar(self.im)
                self.fig.tight_layout()
            else:
                self.im.set_data(self.imag_arr)
                self.txt.set_text("$t=%.3f$" % self.t)

        self.draw()

    def save_state(self):
        np.savetxt("%s/saved_states/%s.dat" %
            (self.dir, data), self.A.view(float))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # properties
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def it(self):
        return self._it

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # setters
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @it.setter
    def it(self, value):
        self._it = value % NUM_IT
