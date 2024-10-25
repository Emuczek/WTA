import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QMainWindow,
                               QDockWidget, QPushButton, QWidget, QToolBar,
                               QTableWidget, QTableWidgetItem, QLabel)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QAction, QKeySequence
from pyvis.network import Network

class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Używamy QWebEngineView do wyświetlania HTML
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

        # Tworzymy i rysujemy graf
        self.draw_graph()

    def draw_graph(self):
        # Tworzenie grafu
        net = Network(notebook=True)

        # Dodawanie wierzchołków i krawędzi
        net.add_node(1, label='Node 1')
        net.add_node(2, label='Node 2')
        net.add_node(3, label='Node 3')
        net.add_edge(1, 2)
        net.add_edge(1, 3)
        net.add_edge(2, 3)

        # Generowanie HTML i wyświetlanie w QWebEngineView
        net.show("graph.html")
        with open("graph.html", "r") as f:
            html = f.read()
        self.web_view.setHtml(html)

class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dialog")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ustawienie centralnego widgetu na wykres grafu
        self.central_widget = GraphWidget()
        self.setCentralWidget(self.central_widget)

        # Tworzenie dock widgetów
        self.create_dock_widgets()

        # Tworzenie toolbara
        self.create_toolbars()

        self.status = self.statusBar()
        self.status.showMessage("Witamy!")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Informacje")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Open)
        exit_action.setStatusTip("Kliknij tutaj, aby wykonać Akcję 1")
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)

        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

    def create_dock_widgets(self):
        # Pierwszy dock widget
        dock1 = QDockWidget("Dockable", self)
        dock1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea |
                              Qt.BottomDockWidgetArea)

        label1 = QLabel("Dock Widget 1", dock1)
        dock1.setWidget(label1)

        # Dokowanie na lewą stronę
        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)

        # Drugi dock widget
        dock2 = QDockWidget("Another Dockable", self)
        dock2.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea |
                              Qt.BottomDockWidgetArea)

        some_layout = QVBoxLayout()

        button = QPushButton("Button in Dock", dock2)
        button.setStatusTip("Gowienko")
        button.clicked.connect(self.open_dialog)
        some_layout.addWidget(button)

        # Tworzenie tabeli
        table_widget = QTableWidget(3, 3)  # Tabela z 3 wierszami i 3 kolumnami
        table_widget.setHorizontalHeaderLabels(["Kolumna 1", "Kolumna 2", "Kolumna 3"])

        # Wypełnianie tabeli przykładowymi danymi
        for row in range(3):
            for column in range(3):
                item = QTableWidgetItem(f"Item {row + 1}, {column + 1}")
                table_widget.setItem(row, column, item)

        # Opakowanie tabeli w widget
        table_container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(table_widget)
        table_container.setLayout(layout)

        some_layout.addWidget(table_container)

        # Tworzymy centralny widget dla dock widgeta
        central_widget = QWidget()
        central_widget.setLayout(some_layout)

        # Ustawiamy centralny widget w dock widget
        dock2.setWidget(central_widget)

        # Dokowanie na górną stronę
        self.addDockWidget(Qt.TopDockWidgetArea, dock2)

    def create_toolbars(self):
        # Pierwszy toolbar
        toolbar1 = QToolBar("Main Toolbar")
        self.addToolBar(Qt.TopToolBarArea, toolbar1)

        # Przykład akcji w toolbarze
        action1 = QAction("Action 1", self)
        action1.triggered.connect(self.action_triggered)
        toolbar1.addAction(action1)

        action2 = QAction("Action 2", self)
        action2.triggered.connect(self.action_triggered)
        toolbar1.addAction(action2)

        # Drugi toolbar
        toolbar2 = QToolBar("Secondary Toolbar")
        self.addToolBar(Qt.LeftToolBarArea, toolbar2)

        # Dodajmy przyciski do drugiego toolbara
        button1 = QPushButton("Button 1")
        button1.clicked.connect(self.open_dialog)
        toolbar2.addWidget(button1)

        button2 = QPushButton("Button 2")
        button2.clicked.connect(self.open_dialog)
        toolbar2.addWidget(button2)

    @Slot()
    def action_triggered(self):
        print("Action triggered!")

    @staticmethod
    def open_dialog():
        dialog = Dialog()
        dialog.exec()  # Wyświetl okno dialogowe w trybie modalnym


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.setWindowTitle("Pyvis Graph Example")
    main.show()
    sys.exit(app.exec())
