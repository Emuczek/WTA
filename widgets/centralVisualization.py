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
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)
        self.draw_graph()

    def draw_graph(self):
        net = Network(notebook=True)

        net.add_node(1, label='Broń 1')
        net.add_node(2, label='Broń 2')
        net.add_node(3, label='Cel 1')
        net.add_node(4, label='Cel 2')
        net.add_edge(1, 3)
        net.add_edge(2, 4)

        net.show("widgets/temp/graph.html")
        with open("widgets/temp/graph.html", "r") as f:
            html = f.read()
        self.web_view.setHtml(html)