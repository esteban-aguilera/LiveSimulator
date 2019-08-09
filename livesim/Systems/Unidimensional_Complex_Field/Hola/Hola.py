# coding: utf-8
# !/usr/bin/env python

import numpy as np
import os

from ..Unidimensional_Complex_Field import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# constants
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
a = -1.0
b = -3.0


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Hola(Unidimensional_Complex_Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir = os.path.dirname(__file__)

        self.param_strs = ["a", "b"]  # nombre de los parametros
        self.params = [a,b]  # valores por default

        self._title = "Ginzburg Landau"

    def time_step_neumann(self):
        a, b = self.params
        A, A_sig = np.copy(self.A), np.copy(self.A)
        inv_dx, inv_dx2, dt = 1/self.dx, 1/self.dx**2, self.dt

        A_sig[1:-1] += dt * \
            ((1 - (1+1j*b)*np.abs(A[1:-1])**2) * A[1:-1] + \
             (1 + 1j*a)*(A[2:] + A[0:-2] - 2*A[1:-1])*inv_dx2 + \
             np.sqrt(.01) * np.random.normal(size=[self.num-2]) * \
             np.exp(2j*np.random.rand(self.num-2)*np.pi))

        # Neumann border conditions
        A_sig[0] = A_sig[1]  # left border
        A_sig[-1] = A_sig[-2]  # right border

        self.t += self.dt
        self.A = A_sig

    def time_step_periodic(self):
        a,b = self.params
        A, A_sig = np.copy(self.A), np.copy(self.A)
        inv_dx, inv_dx2, dt = 1/self.dx, 1/self.dx**2, self.dt

        A_sig += dt * \
            ((1 - (1+1j*b)*np.abs(A)**2) * A + \
             (1+1j*a)*(np.roll(A, 1) + np.roll(A, -1) - 2*A)*inv_dx2 + \
             np.sqrt(.01) * np.random.normal(size=[self.num]) * \
             np.exp(2j*np.random.rand(self.num)*np.pi))

        self.t += self.dt
        self.A = A_sig

    def time_step_dirichlet(self):
        a,b = self.params
        A, A_sig = np.copy(self.A), np.copy(self.A)
        inv_dx, inv_dx2, dt = 1/self.dx, 1/self.dx**2, self.dt

        A_sig[1:-1] += dt * \
            ((1 -(1+1j*b)*np.abs(A[1:-1])**2) * A[1:-1] + \
             (1+1j*a)*(A[2:] + A[0:-2] - 2*A[1:-1])*inv_dx2 + \
             np.sqrt(.01) * np.random.normal(size=[self.num-2]) * \
             np.exp(2j*np.random.rand(self.num-2)*np.pi))

        # Dirichlet border conditions
        A_sig[0] = -1  # left border
        A_sig[-1] = 1  # right border

        self.t += self.dt
        self.A = A_sig
