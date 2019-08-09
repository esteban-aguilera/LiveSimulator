# coding: utf-8
# !/usr/bin/env python

import os
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidget


class ListSavedStates(QListWidget):

    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        self.setFont(QFont("Times", 14))

    def loadSavedStates(self, dir, system, equation):
        self.addItem("0")
        for f in os.listdir("%s/%s/%s/saved_states" % (dir, system, equation)):
            if("__pycache__" not in f and "_params.dat" not in f):
                if(f[-4:] == ".dat"):
                    self.addItem(f[:-4])
                else:
                    self.addItem(f)
        self.sortItems()

    def unloadSavedStates(self):
        for i in range(self.count()):
            self.takeItem(0)
