# coding: utf-8
# !/usr/bin/env python

import pkgutil
import os
import sys
import time

from multiprocessing import Process, Pipe, Value
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, \
    QVBoxLayout, QHBoxLayout

from .Widgets.ListSystems import *
from .Widgets.ListEquations import *
from .Widgets.ListSavedStates import *
from .Widgets.EquationWidget import *
from .Widgets.PlotWidget import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# constants
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
DIR = os.path.dirname(__file__)
SYSTEMS_DIR = "%s/Systems" % DIR


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MainWindow
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.list_systems = None
        self.list_equations = None
        self.list_saved_states = None

        self._current_system = None
        self._current_equation = None
        self._current_saved_state = None

        self.equations_dict = {}
        self._equation_widget, self._plot_widget = None, None

        self.simulator_process = None
        self._equation_selected = Value('i', False)
        self.simulator_conn, self.plotter_conn = Pipe(5)
        self._play = Value('i', False)

        self.setCentralWidget(self.createCentralWidget())

    def createCentralWidget(self):
        centralWidget = QWidget()
        self.hlayout = QHBoxLayout()
        self.vlayouts = [QVBoxLayout() for _ in range(3)]

        # create widget with list of available systems
        self.list_systems = ListSystems()
        self.list_systems.loadSystems(SYSTEMS_DIR)
        self.list_systems.itemClicked.connect(self.systemClicked)
        # create widget with list of available equation
        self.list_equations = ListEquations()
        self.list_equations.itemClicked.connect(self.equationClicked)
        # create widget with list of available states
        self.list_saved_states = ListSavedStates()
        self.list_saved_states.itemClicked.connect(self.savedStateClicked)
        # add them to the first vertical layout
        self.vlayouts[0].addWidget(self.list_systems)
        self.vlayouts[0].addWidget(self.list_equations)
        self.vlayouts[0].addWidget(self.list_saved_states)

        # create widget for equation manipulation
        self.equation_widget = None
        # add it to the second vertical layout
        self.vlayouts[1].addWidget(self.equation_widget)

        # create widget for plotting
        self.plot_widget = None
        # add it to the third vertical layout
        self.vlayouts[2].addWidget(self.plot_widget)

        # add every vertical layout to the horizontal layout
        for vlayout in self.vlayouts:
            self.hlayout.addLayout(vlayout)

        centralWidget.setLayout(self.hlayout)
        return centralWidget

    def loadEquationsDictionary(self):
        pkg_dir = "%s/%s" % (SYSTEMS_DIR, self.current_system)
        import_systems(pkg_dir, prefixes=["Systems", self.current_system])
        Equations = {}
        for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
            if("Figure" in name):
                pass
            elif("Plotter" in name):
                ldict = locals()
                exec("c = %s" % (name), globals(), ldict)
                Equations["Plotter"] = ldict["c"]
            else:
                ldict = locals()
                exec("c = %s" % (name), globals(), ldict)
                Equations[str(name)] = ldict["c"]

        return Equations

    def closeEvent(self, event):
        self.current_system = None
        event.accept()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # clickers
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def systemClicked(self, item):
        self.current_system = item.text().replace(" ", "_")

    def equationClicked(self, item):
        self.current_equation = item.text().replace(" ", "_")

    def savedStateClicked(self, item):
        self.current_saved_state = item.text()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # properties
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def equation_widget(self):
        return self._equation_widget

    @property
    def plot_widget(self):
        return self._plot_widget

    @property
    def current_system(self):
        return self._current_system

    @property
    def current_equation(self):
        return self._current_equation

    @property
    def current_saved_state(self):
        return self._current_saved_state

    @property
    def equation_selected(self):
        return self._equation_selected.value

    @property
    def play(self):
        return self._play.value

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # setters
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @equation_widget.setter
    def equation_widget(self, value):
        if(self._equation_widget is not None):
            del self._equation_widget
            self.vlayouts[1].takeAt(0).widget().deleteLater()

        if(value is None):
            self._equation_widget = EquationWidget(self.simulator_conn, self._play)
            self.plot_widget = None
        else:
            self._equation_widget = value(self.simulator_conn, self._play)
            self.plot_widget = self.equations_dict["Plotter"]
        self.equation_widget.createUI()
        self.vlayouts[1].addWidget(self._equation_widget)

    @plot_widget.setter
    def plot_widget(self, value):
        if(self._plot_widget is not None):
            self._plot_widget.figure_widget.timer.stop()
            self.vlayouts[2].takeAt(0).widget().deleteLater()
        if(value is None):
            self._plot_widget = PlotWidget(self.plotter_conn,
                self._play, dir="")
        else:
            self._plot_widget = value(self.plotter_conn, self._play,
                dir=self.current_equation)
        self.vlayouts[2].addWidget(self._plot_widget)

    @current_system.setter
    def current_system(self, value):
        self.current_saved_state = None
        self.current_equation = None
        self._current_system = value

        self.list_equations.unloadEquations()
        self.list_saved_states.unloadSavedStates()
        if(value is None):
            pass
        else:
            self.list_equations.loadEquations(SYSTEMS_DIR, self.current_system)
            self.equations_dict = self.loadEquationsDictionary()
        self.equation_widget = None

    @current_equation.setter
    def current_equation(self, value):
        self.current_saved_state = None
        self._current_equation = value
        self.list_saved_states.unloadSavedStates()
        if(value is None):
            self.current_saved_state = None
            self.equation_selected = False
        else:
            self.list_saved_states.loadSavedStates(
                SYSTEMS_DIR, self.current_system, self.current_equation)
            self.equation_widget = self.equations_dict[self.current_equation]
            self.equation_selected = True

    @current_saved_state.setter
    def current_saved_state(self, value):
        if(value is None):
            self._current_saved_state = None
        else:
            try:
                value = float(value)
            except ValueError:
                pass
            self._current_saved_state = value

            original_play = self.play
            self.play = False
            while(self.plotter_conn.poll()):
                self.plotter_conn.recv()
            while(self.simulator_conn.poll()):
                self.simulator_conn.recv()
            loaded_data = self.equation_widget.load_state(value)
            self.plotter_conn.send(loaded_data)
            self.play = original_play

    @equation_selected.setter
    def equation_selected(self, value):
        self.play = False
        self._equation_selected.value = value
        if(value is True):
            self.simulator_process = Process(target=simulator,
                args=(self._equation_selected, self.equation_widget, self.plotter_conn))
            self.simulator_process.start()
        else:
            if(self.simulator_process is not None):
                while(self.plotter_conn.poll()):
                    self.plotter_conn.recv()
                while(self.simulator_conn.poll()):
                    self.simulator_conn.recv()
                self.simulator_process.terminate()
                self.simulator_process.join()
                self.simulator_process = None

    @play.setter
    def play(self, value):
        self._play.value = value


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# functions
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def simulator(_equation_selected, equation_widget, plotter_conn):
    while(_equation_selected.value):
        equation_widget.read_conn()
        if(equation_widget.play):
            for _ in range(equation_widget.speed):
                equation_widget.time_step()
            while(plotter_conn.poll()):
                time.sleep(0.03)
            equation_widget.plot()
        else:
            time.sleep(0.5)


def import_systems(pkg_dir, prefixes=[], k=1):
    for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        if(ispkg is True):
            sys.path += ["%s/%s" % (pkg_dir, name)]
            import_systems("%s/%s" % (pkg_dir, name), prefixes + [name], k+1)
        else:
            s = ""
            for prefix in prefixes:
                s += prefix + "."
            name = s + name
            exec('from .%s import *' % name, globals())

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# main
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
