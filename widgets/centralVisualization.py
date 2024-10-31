import sys
import time
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QMainWindow, QDockWidget, QToolBar,  QTableWidget,
                               QTableWidgetItem, QWidget, QApplication, QMainWindow, QDockWidget,
                               QVBoxLayout, QLabel, QProgressBar, QWidget, QPushButton, QFileDialog, QStatusBar)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QAction, QKeySequence
from pyvis.network import Network
import markdown


class GraphWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data_x = data
        if len(self.data_x) > 0:
            self.m = len(self.data_x)
            self.n = len(self.data_x[0])
        else:
            self.m = 0
            self.n = 0
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)
        self.draw_graph()

    def draw_graph(self):
        net = Network(notebook=True)

        for x in range(self.m):
            net.add_node(x, label=f"Broń {x}")

        for x in range(self.m, self.m+self.n):
            net.add_node(x, label=f"Cel {x-self.m}")

        for i in range(self.m):
            for j in range(self.n):
                if self.data_x[i][j] == 1:
                    net.add_edge(i, j+self.m)

        net.show("widgets/temp/graph.html")
        with open("widgets/temp/graph.html", "r") as f:
            html = f.read()
        self.web_view.setHtml(html)
