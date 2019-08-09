# coding: utf-8
# !/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, \
    QLabel, QLineEdit, QPushButton, QComboBox


class SaveDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setFixedHeight(100)
        self.setFixedWidth(350)
        self.setWindowTitle("Save")

        self.createUI()

    def createUI(self):
        self.label_name = QLabel("Enter Name:")
        self.label_name.setFont(QFont("Times", 14))

        self.line_edit = QLineEdit("file name")
        self.line_edit.setFont(QFont("Times", 14))

        self.label_void = QLabel("")
        self.label_void.setFont(QFont("Times", 14))

        self.extensions_cb = QComboBox()
        self.extensions_cb.addItems(["dat", "png", "pdf"])
        self.extensions_cb.setFont(QFont("Times", 14))

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setFont(QFont("Times", 14))

        hlayouts = [QHBoxLayout() for _ in range(2)]

        hlayouts[0].addWidget(self.label_name)
        hlayouts[0].addWidget(self.line_edit)

        hlayouts[1].addWidget(self.extensions_cb)
        hlayouts[1].addWidget(self.label_void)
        hlayouts[1].addWidget(self.ok_btn)

        vlayout = QVBoxLayout()
        for hlayout in hlayouts:
            vlayout.addLayout(hlayout)
        self.setLayout(vlayout)

    def extension(self):
        return self.extensions_cb.currentText()
