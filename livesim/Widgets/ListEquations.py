# coding: utf-8
# !/usr/bin/env python

import os
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidget


class ListEquations(QListWidget):

    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        self.setFont(QFont("Times", 14))

    def loadEquations(self, dir, system):
        for f in os.listdir("%s/%s" % (dir, system)):
            if(os.path.isdir("%s/%s/%s" % (dir, system, f)) and "__pycache__" not in f):
                self.addItem(f.replace("_", " "))
        self.sortItems()

    def unloadEquations(self):
        for i in range(self.count()):
            self.takeItem(0)
