# coding: utf-8
# !/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

from multiprocessing import Value
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QComboBox
from livesim.Widgets.EquationWidget import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# constants
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
WIDTH = 100
HEIGHT = 100
NUM = 500
DT = .01
BOUNDARIES = ["Neumann", "Dirichlet", "Periodic"]
BOUNDARY = BOUNDARIES[0]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Unidimensional_Complex_Field(EquationWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir = "%s%s" % (os.path.dirname(__file__), dir)

        self._width = WIDTH
        self._height = HEIGHT
        self._num = NUM
        self._x = np.linspace(0, WIDTH, num=NUM)
        self._y = np.linspace(0, HEIGHT, num=NUM)
        self._dx = self._x[1]-self._x[0]
        self._dy = self._y[1]-self._y[0]
        self.dt = DT
        self.t = 0

        self.A = 0

        self._boundary_index = Value('i', 0)
        self.set_A_widget, self.set_A = None, 0 + 0j

    def createUI(self):
        super().createUI()

        self.createTitleWidget()
        self.createBoundaryWidget()
        self.createParamWidgets()
        self.createPlaySpeedWidget()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # methods
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def time_step(self):
        for _ in range(self.speed*50):
            if(self.boundary_index == 0):
                self.time_step_neumann()
            elif(self.boundary_index == 1):
                self.time_step_dirichlet()
            elif(self.boundary_index == 2):
                self.time_step_periodic()

    def plot(self):
        data = self.A, self.t, self.x, self.params[0]
        self.conn.send(data)

    def read_conn(self):
        if(self.conn.poll()):
            self.A = self.conn.recv()
            self.plot()

    def load_state(self, value):
        if(value is None):
            self.A = 0
        elif(type(value) == str):
            self.A = np.loadtxt(
                "%s/saved_states/%s.dat" % (self.dir, value)
            )
            try:
                s = open("%s/saved_states/%s_params.dat" % (self.dir, value), 'r').read()
                s_arr = s.split(" ")[:-1]
                self.boundary_index = s_arr[0]
                self.params = [float(s) for s in s_arr[1:]]
            except FileNotFoundError:
                pass
        else:
            self.A = value

        return self.A

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # user interface functions
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createBoundaryWidget(self):
        def boundaryClicked(i):
            self.boundary_index = i

        lb = QLabel("Boundary:")
        lb.setFont(QFont("Times", 14))
        lb.setAlignment(Qt.AlignCenter)
        lb.setFixedWidth(80)

        cb = QComboBox()
        cb.addItems(BOUNDARIES)
        cb.setFont(QFont("Times", 14))
        cb.currentIndexChanged.connect(boundaryClicked)

        hlayout = QHBoxLayout()
        hlayout.addWidget(lb)
        hlayout.addWidget(cb)
        self.vlayout.addLayout(hlayout)

    def createSaveWidget(self):
        def saveClicked():
            original_play = self.play
            self.play = False
            def save():
                fname = save_dialog.line_edit.text()
                self.plot(fname=fname)
                save_dialog.close()
                self.play = original_play

            save_dialog = SaveDialog()
            save_dialog.line_edit.returnPressed.connect(save)
            save_dialog.ok_btn.clicked.connect(save)
            save_dialog.show()

        save_button = QPushButton(QIcon("%s/save_icon.png" % DIR), "")
        save_button.setIconSize(QSize(50, 50))
        save_button.setStyleSheet('QPushButton{border: 0px solid;}')
        save_button.clicked.connect(saveClicked)
        self.vlayout.addWidget(save_button)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # properties
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def A(self):
        return self._A

    @property
    def boundary_index(self):
        return self._boundary_index.value

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def num(self):
        return self._num

    @property
    def dx(self):
        return self._dx

    @property
    def dy(self):
        return self._dy

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def dt(self):
        return self._dt

    @property
    def t(self):
        return self._t

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # setters
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @A.setter
    def A(self, value):
        if(type(value) in [int, float, complex]):
            self._A = np.zeros([self.num], dtype=complex) + value
        elif(type(value) == np.ndarray):
            self._A = np.copy(value)
        elif(type(value) == str):
            self.load_state(value)

    @boundary_index.setter
    def boundary_index(self, value):
        self._boundary_index.value = value

    @width.setter
    def width(self, value):
        self._width = value
        self._x = np.linspace(0, self._width, num=self.num)
        self._dx = self._x[1]-self._x[0]
        self.dt = self.dt

    @num.setter
    def num(self, value):
        self._num = value
        self._x = np.linspace(0, self._width, num=self.num)
        self._dx = self._x[1]-self._x[0]
        self.dt = self.dt

    @dt.setter
    def dt(self, value):
        if(value > 0.1 * np.min([self.dx, self.dy])**2):
            self._dt = 0.01 * np.min([self.dx, self.dy])**2
        else:
            self._dt = value

    @t.setter
    def t(self, value):
        self._t = value
