# coding: utf-8
# !/usr/bin/env python

import os
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidget


class ListSystems(QListWidget):

    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        self.setFont(QFont("Times", 14))

    def loadSystems(self, dir):
        for f in os.listdir(dir):
            if(os.path.isdir("%s/%s" % (dir, f)) and "__pycache__" not in f):
                self.addItem(f.replace("_", " "))
        self.sortItems()
