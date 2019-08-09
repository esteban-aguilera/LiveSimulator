# coding: utf-8
# !/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import os
import random

from matplotlib.patches import Rectangle
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox
from livesim.Widgets.FigureWidget import *
from livesim.Widgets.ParamWidget import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# constants
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Z_AXIS_OPTIONS = ["Abs", "Arg", "Re*Im", "Re", "Im", "Pol. Cruzados"]
DIR_FIGURE = os.path.dirname(__file__)
theta_0 = np.pi/3*0


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Bidimensional_Complex_Field_Figure(FigureWidget):

    def __init__(self, conn, _play, dir=""):
        self.dir= "%s/%s" % (os.path.dirname(__file__), dir)
        self.z_axis_index = 0

        self.A, self.t, self.boudnary, self.params = None, None, None, None
        self.im, self.cb = None, None
        self.patch = None

        super().__init__(conn, _play, dir=dir)

    def plot(self, data):
        if(len(data) == 4):
            self.A, self.t, self.boundary, self.params = data
        else:
            self.A = data
        if(self.im is None):
            self.ax.cla()
            if(self.z_axis_index == 0):
                self.im = self.ax.imshow(np.abs(self.A.T),
                    origin="lower", cmap=plt.get_cmap("OrRd"),
                    vmin=0, vmax=np.sqrt(self.params[0]))
            elif(self.z_axis_index == 1):
                self.im = self.ax.imshow(np.angle(self.A.T),
                    origin="lower", cmap=plt.get_cmap("gist_gray"),
                    vmin=-np.pi, vmax=np.pi)
            elif(self.z_axis_index == 2):
                self.im = self.ax.imshow(np.real(self.A.T) * np.imag(self.A.T),
                    origin="lower", cmap=plt.get_cmap("seismic"),
                    vmin=-.3*np.sqrt(self.params[0]), vmax=.3*np.sqrt(self.params[0]))
            elif(self.z_axis_index == 3):
                self.im = self.ax.imshow(np.real(self.A.T),
                    origin="lower", cmap=plt.get_cmap("seismic"),
                    vmin=-.3*np.sqrt(self.params[0]), vmax=.3*np.sqrt(self.params[0]))
            elif(self.z_axis_index == 4):
                self.im = self.ax.imshow(np.imag(self.A.T),
                    origin="lower", cmap=plt.get_cmap("seismic"),
                    vmin=-.3*np.sqrt(self.params[0]), vmax=.3*np.sqrt(self.params[0]))
            elif(self.z_axis_index == 5):
                self.im = self.ax.imshow(np.abs(self.A.T)**2 *
                    np.sin(np.angle(self.A.T) - theta_0) *
                    np.cos(np.angle(self.A.T) - theta_0),
                    origin="lower", cmap=plt.get_cmap("copper"),
                    vmin=0, vmax=0.25*self.params[0])

            self.ax.set_xlabel("$x$ (u.a.)", fontsize=15)
            self.ax.set_ylabel("$y$ (u.a.)", fontsize=15)
            self.txt = self.ax.text(
                .95*self.ax.get_xlim()[1], 0.95*self.ax.get_ylim()[1],
                "$t=%.3f$" % self.t, fontsize=12, va="top", ha="right",
                multialignment="left", bbox={'facecolor': 'white', 'alpha': .9})
            self.ax.grid()

            if(self.cb is not None):
                self.cb.remove()
                self.cb = None
            self.cb = self.fig.colorbar(self.im)
        else:
            if(self.z_axis_index == 0):
                self.im.set_data(np.abs(self.A.T))
            elif(self.z_axis_index == 1):
                self.im.set_data(np.angle(self.A.T))
            elif(self.z_axis_index == 2):
                self.im.set_data(np.real(self.A.T)*np.imag(self.A.T))
            elif(self.z_axis_index == 3):
                self.im.set_data(np.real(self.A.T))
            elif(self.z_axis_index == 4):
                self.im.set_data(np.imag(self.A.T))
            elif(self.z_axis_index == 5):
                self.im.set_data((np.sin(np.angle(self.A.T) - theta_0)*np.cos(np.angle(self.A.T) - theta_0))**2)
            self.txt.set_text("$t=%.3f$" % self.t)
        self.draw()

    def save_state(self, fname):
        np.savetxt("%s/saved_states/%s.dat" %
                (self.dir, fname), self.A.view(float))

        f = open("%s/saved_states/%s_params.dat" % (self.dir, fname), "w")
        f.write(self.boundary)
        for param in self.params:
            f.write(" %.5f" % param)
        f.close()

    def drawRectangle(self, x1, x2, y1, y2):
        self.removeRectangle()

        x0, y0 = np.minimum(x1, x2), np.minimum(y1, y2)
        width, height = np.abs(x2-x1), np.abs(y2-y1)

        self.removeRectangle()
        self.patch = self.ax.add_patch(
            Rectangle((x0, y0), width, height, fill=False)
        )

        self.draw()

    def removeRectangle(self):
        if(self.patch is not None):
            self.patch.remove()
            self.patch = None
