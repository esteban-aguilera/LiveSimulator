# coding: utf-8
# !/usr/bin/env python

import numpy as np
import os

from ..Bidimensional_Complex_Field import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# constants
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
EPS = 1
DELTA = 0.1
XI = 0.01
ALPHA = 1.0
N = 2  # Dirichlet border condition


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class AGL_Anisotropic_Evolution(Bidimensional_Complex_Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir = os.path.dirname(__file__)

        self.param_strs = ["μ", "δ", "ξ", "α"]
        self.params = [EPS, DELTA, XI, ALPHA]

        self._title = "Anisotropic Ginzburg Landau"

    def time_step_neumann(self):
        mu, delta, xi, alpha = self.params
        A, Ac, A_sig = np.copy(self.A), np.conj(self.A), np.copy(self.A)
        inv_dx, inv_dy, dt = 1/self.dx, 1/self.dy, self.dt
        inv_dx2, inv_dy2 = 1/self.dx**2, 1/self.dy**2

        step = dt * \
            ((mu - np.abs(A[1:-1, 1:-1])**2) * A[1:-1, 1:-1] + \
             (A[2:, 1:-1] + A[0:-2, 1:-1] - 2*A[1:-1, 1:-1])*inv_dx2 + \
             (A[1:-1, 2:] + A[1:-1, 0:-2] - 2*A[1:-1, 1:-1])*inv_dy2 + \
             delta*((Ac[2:, 1:-1] + Ac[:-2, 1:-1] - 2*Ac[1:-1, 1:-1])*inv_dx2 -
                    (Ac[1:-1, 2:] + Ac[1:-1, :-2] - 2*Ac[1:-1, 1:-1])*inv_dy2 +
                    0.5j*(Ac[2:, 2:] + Ac[:-2, :-2] - Ac[2:, :-2] -
                          Ac[:-2, 2:])*inv_dx*inv_dy) + \
             np.sqrt(xi) * np.random.normal(size=[self.nx-2, self.ny-2]) * \
             np.exp(2j*np.random.rand(self.nx-2, self.ny-2)*np.pi))

        A_sig[1:-1, 1:-1] += alpha*np.real(step) + 1j*np.imag(step)

        # Neumann border conditions
        A_sig[0, :] = A_sig[1, :]  # left border
        A_sig[-1, :] = A_sig[-2, :]  # right border
        A_sig[:, 0] = A_sig[:, 1]  # bottom border
        A_sig[:, -1] = A_sig[:, -2]  # upper border

        self.t += self.dt
        self.A = A_sig

    def time_step_periodic(self):
        mu, delta, xi, a = self.params
        A, Ac = np.copy(self.A), np.conj(self.A)
        inv_dx, inv_dy, dt = 1/self.dx, 1/self.dy, self.dt
        inv_dx2, inv_dy2 = 1/self.dx**2, 1/self.dy**2

        step = dt * \
            ((mu - np.abs(A)**2) * A + \
             (np.roll(A,1,axis=0)+np.roll(A,-1,axis=0)-2*A)*inv_dx2 + \
             (np.roll(A,1,axis=1)+np.roll(A,-1,axis=1)-2*A)*inv_dy2 + \
             delta*((np.roll(Ac,1,axis=0)+np.roll(Ac,-1,axis=0)-2*Ac)*inv_dx2 -
                    (np.roll(Ac,1,axis=1)+np.roll(Ac,-1,axis=1)-2*Ac)*inv_dy2 +
                    0.5j*(np.roll(np.roll(Ac,1,axis=0),1,axis=1) +
                          np.roll(np.roll(Ac,-1,axis=0),-1,axis=1) -
                          np.roll(np.roll(Ac,1,axis=0),-1,axis=1) -
                          np.roll(np.roll(Ac,-1,axis=0),1,axis=1)
                          )*inv_dx*inv_dy) + \
             np.sqrt(xi) * np.random.normal(size=[self.nx, self.ny]) * \
             np.exp(2j*np.random.rand(self.nx, self.ny)*np.pi))

        self.t += self.dt
        self.A = A + alpha*np.real(step) + 1j*np.imag(step)

    def time_step_dirichlet(self):
        mu, delta, xi, a = self.params
        A, Ac, A_sig = np.copy(self.A), np.conj(self.A), np.copy(self.A)
        inv_dx, inv_dy, dt = 1/self.dx, 1/self.dy, self.dt
        inv_dx2, inv_dy2 = 1/self.dx**2, 1/self.dy**2

        step = dt * \
            ((mu - np.abs(A[1:-1, 1:-1])**2) * A[1:-1, 1:-1] + \
             (A[2:, 1:-1] + A[0:-2, 1:-1] - 2*A[1:-1, 1:-1])*inv_dx2 + \
             (A[1:-1, 2:] + A[1:-1, 0:-2] - 2*A[1:-1, 1:-1])*inv_dy2 + \
             delta*((Ac[2:, 1:-1] + Ac[:-2, 1:-1] - 2*Ac[1:-1, 1:-1])*inv_dx2 -
                    (Ac[1:-1, 2:] + Ac[1:-1, :-2] - 2*Ac[1:-1, 1:-1])*inv_dy2 +
                    0.5j*(Ac[2:, 2:] + Ac[:-2, :-2] - Ac[2:, :-2] -
                          Ac[:-2, 2:])*inv_dx*inv_dy) + \
             np.sqrt(xi) * np.random.normal(size=[self.nx-2, self.ny-2]) * \
             np.exp(2j*np.random.rand(self.nx-2, self.ny-2)*np.pi))

        A_sig[1:-1, 1:-1] += alpha*np.real(step) + 1j*np.imag(step)

        # Dirichlet border conditions
        A_sig[0, :] = np.sqrt(mu) * \
            np.exp(N * 1j*np.arctan2(.5*self.height-self.y[:],
                                     .5*self.width-self.x[0]))  # left border
        A_sig[-1, :] = np.sqrt(mu) * \
            np.exp(N * 1j*np.arctan2(.5*self.height-self.y[:],
                                     .5*self.width-self.x[-1]))  # right border
        A_sig[:, 0] = np.sqrt(mu) * \
            np.exp(N * 1j*np.arctan2(.5*self.height-self.y[0],
                                     .5*self.width-self.x[:]))  # bottom border
        A_sig[:, -1] = np.sqrt(mu) * \
            np.exp(N * 1j*np.arctan2(.5*self.height-self.y[-1],
                                     .5*self.width-self.x[:]))  # upper border

        self.t += self.dt
        self.A = A_sig
