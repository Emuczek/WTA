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


class StatusDockWidget(QDockWidget):
    def __init__(self):
        super().__init__("Informacje o przebiegu")

        # Centralny widget dla dock widgeta
        self.status_widget = QWidget()
        self.setWidget(self.status_widget)

        # Layout
        layout = QVBoxLayout()

        layout.addStretch(0)

        # Etykieta do wyświetlania czasu
        self.time_label = QLabel("Czas: 0 s")
        layout.addWidget(self.time_label)

        # Etykieta do wyświetlania aktualnej wartości
        self.value_label = QLabel("Aktualna wartość: 0")
        layout.addWidget(self.value_label)

        # Pasek postępu
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Ustawiamy layout
        self.status_widget.setLayout(layout)

        # Timer do aktualizacji czasu
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.elapsed_time = 0

        # Inicjalizacja paska postępu
        self.current_value = 0

    @Slot(name="processing")
    def start_processing(self):
        self.elapsed_time = 0
        self.current_value = 0
        self.progress_bar.setValue(0)
        self.timer.start(1000)  # Aktualizacja co sekundę

        # Symulacja obliczeń
        self.simulate_processing()

    def update_time(self):
        self.elapsed_time += 1
        self.time_label.setText(f"Czas: {self.elapsed_time} s")

        # Zaktualizuj aktualną wartość i pasek postępu
        self.current_value += 0.1  # Przykładowa aktualizacja
        if self.current_value > 100:
            self.current_value = 100

        self.value_label.setText(f"Aktualna wartość: {self.current_value}")
        self.progress_bar.setValue(self.current_value)

    def simulate_processing(self):
        # Funkcja symulująca długotrwałe obliczenia
        while self.current_value < 100:
            time.sleep(0.01)  # Symuluj opóźnienie
            self.update_time()  # Aktualizuj stan na dock widget
        self.timer.stop()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_file_path = str()
        self.markdown_filepath = "D:/Studia/Praca_Inzynierska/ProjectPythonWTA/modules/documentation.md"

        # Ustawienie centralnego widgetu na wykres grafu
        self.markdown_window = QWidget()  # Create a new window
        self.central_widget = GraphWidget()
        self.setCentralWidget(self.central_widget)

        # Tworzenie dock widgetów
        self.create_dock_widgets()
        self.status_dock_widget = StatusDockWidget()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.status_dock_widget)

        # Tworzenie toolbara
        self.create_toolbars()

        self.status = self.statusBar()
        self.status.showMessage("Witamy!")

        # Menu
        self.menubar = QMenuBar()
        self.layout().setMenuBar(self.menubar)  # Set layout before adding menubar
        self.file_menu = self.menubar.addMenu("Wczytywanie danych")
        self.info_menu = self.menubar.addMenu("Informacje")

        self.statusbar = QStatusBar(self)
        self.filepath_label = QLabel("Brak wybranego pliku z danymi")
        self.statusbar.addWidget(self.filepath_label)
        self.setStatusBar(self.statusbar)  # Use setStatusBar()

        # Exit QAction
        exit_action = QAction("Importuj dane z pliku .JSON", self)
        exit_action.setStatusTip("Kliknij tutaj, zaimportować plik .JSON")
        exit_action.triggered.connect(self.open_file_dialog)

        exi_action = QAction("Informacje na temat programu", self)
        exi_action.setStatusTip("Kliknij tutaj, aby dowiedzieć się wiecej")
        exi_action.triggered.connect(self.display_markdown)

        self.file_menu.addAction(exit_action)
        self.info_menu.addAction(exi_action)

        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

    def create_dock_widgets(self):
        dock1 = QDockWidget("Wybór metody", self)
        dock1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea |
                              Qt.BottomDockWidgetArea)

        layout_wybor = QVBoxLayout()
        heuristic_button = QPushButton("Heurystyka 'TabuSearch'")
        heuristic_button.clicked.connect(self.open_dialog)
        linapprox_button = QPushButton("Aproksymacja liniowa")
        linapprox_button.clicked.connect(self.open_dialog)
        qubo_button = QPushButton("Kwantowe wyżarzanie")
        qubo_button.clicked.connect(self.open_dialog)

        layout_wybor.addWidget(heuristic_button)
        layout_wybor.addWidget(linapprox_button)
        layout_wybor.addWidget(qubo_button)
        layout_wybor.addStretch(0)

        wybor_widget = QWidget()
        wybor_widget.setLayout(layout_wybor)
        dock1.setWidget(wybor_widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)

    def create_toolbars(self):
        toolbar2 = QToolBar("Secondary Toolbar")
        self.addToolBar(Qt.TopToolBarArea, toolbar2)

        button1 = QPushButton("Rozpocznij obliczanie")
        button1.clicked.connect(self.status_dock_widget.start_processing)
        toolbar2.addWidget(button1)

        button2 = QPushButton("Zakończ obliczanie")
        button2.clicked.connect(self.open_dialog)
        toolbar2.addWidget(button2)

    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("JSON files (*.json)")

        if file_dialog.exec():
            self.selected_file_path = file_dialog.selectedFiles()[0]
            self.filepath_label.setText(f"Wybrany plik: {self.selected_file_path}")

    def display_markdown(self, filepath):
        try:
            with open(self.markdown_filepath, 'r', encoding='utf-8') as f:
                markdown_text = f.read()
            html = markdown.markdown(markdown_text)

            # Documentation as dock widget

            # dock = QDockWidget("Information", self)  # Dock title is the file path
            # dock.setAllowedAreas(Qt.AllDockWidgetAreas)
            # text_edit = QTextEdit()
            # text_edit.setReadOnly(True)  # Make the content read-only
            # text_edit.setHtml(html)
            # dock.setWidget(text_edit)
            # self.addDockWidget(Qt.RightDockWidgetArea, dock)  # Initial position

            # Documentation as pop window

            self.markdown_window.setWindowTitle("Informacje")
            layout = QVBoxLayout()  # Add layout to new window
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setHtml(html)
            layout.addWidget(text_edit)
            self.markdown_window.setLayout(layout)  # Set layout on new window
            self.markdown_window.show()
            geometry = self.screen().availableGeometry()
            self.markdown_window.setFixedSize(geometry.width() * 0.4, geometry.height() * 0.35)

        except Exception as e:
            print(f"Error opening or rendering markdown: {e}")

    @Slot()
    def action_triggered(self):
        print("Action triggered!")

    @staticmethod
    def open_dialog():
        dialog = Dialog()
        dialog.exec()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = MainWindow()
#     main.setWindowTitle("Weapon target assingment solver")
#     main.show()
#     sys.exit(app.exec())
