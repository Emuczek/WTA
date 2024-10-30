import sys
import time
from PySide6.QtCore import Qt, Slot, QTimer, QThread, Signal, QObject
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
from widgets.centralVisualization import GraphWidget
from modules.quizProblemHeuristic import CalculationQuizHeuristic


class Worker(QObject):
    finished = Signal()
    progress = Signal(str)

    def __init__(self):
        super().__init__()
        self.calc = CalculationQuizHeuristic()

    def defstop(self):
        self.calc.stop = True

    def run(self):
        self.calc.calculate("data/testInstance2x2.json")
        self.finished.emit()


class StatusDockWidget(QDockWidget):
    def __init__(self):
        super().__init__("Informacje o przebiegu")

        # Centralny widget dla dock widgeta
        self.progress_bar = QProgressBar()
        self.current_value = None
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

        layout.addWidget(self.progress_bar)

        # Ustawiamy layout
        self.status_widget.setLayout(layout)

        # Timer do aktualizacji czasu
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.elapsed_time = 0

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
        self.status_dock_widget = StatusDockWidget()
        self.markdown_filepath = "modules/documentation.md"
        self.markdown_window = QWidget()
        self.thread = None
        self.worker = None

        # Central widget

        self.central_widget = GraphWidget()
        self.setCentralWidget(self.central_widget)

        # Dock widgets
        self.create_dock_widgets()

        # Toolbars
        self.stop_calc_button = QPushButton("Zakończ obliczanie")
        self.start_calc_button = QPushButton("Rozpocznij obliczanie")
        self.create_toolbars()

        self.status = self.statusBar()
        self.status.showMessage("Witamy!")

        # Menus

        self.create_menus(self)

        geometry = self.screen().availableGeometry()
        self.setFixedSize(int(geometry.width() * 0.8), int(geometry.height() * 0.7))

    @staticmethod
    def create_menus(self):
        self.menubar = QMenuBar()
        self.layout().setMenuBar(self.menubar)
        self.file_menu = self.menubar.addMenu("Wczytywanie danych")
        self.info_menu = self.menubar.addMenu("Informacje")

        self.statusbar = QStatusBar()
        self.filepath_label = QLabel("Brak wybranego pliku z danymi")
        self.statusbar.addWidget(self.filepath_label)
        self.setStatusBar(self.statusbar)

        import_action = QAction("Importuj dane z pliku .JSON", self)
        import_action.setStatusTip("Kliknij tutaj, zaimportować plik .JSON")
        import_action.triggered.connect(self.open_file_dialog)

        documentation_action = QAction("Informacje na temat programu", self)
        documentation_action.setStatusTip("Kliknij tutaj, aby dowiedzieć się wiecej")
        documentation_action.triggered.connect(self.display_markdown)

        self.file_menu.addAction(import_action)
        self.info_menu.addAction(documentation_action)

    def create_dock_widgets(self):
        dock1 = QDockWidget("Wybór metody", self)
        dock1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea |
                              Qt.BottomDockWidgetArea)

        layout_wybor = QVBoxLayout()
        heuristic_button = QPushButton("Heurystyka 'TabuSearch'")
        heuristic_button.clicked.connect(self.status_dock_widget.start_processing)
        linapprox_button = QPushButton("Aproksymacja liniowa")
        linapprox_button.clicked.connect(self.status_dock_widget.start_processing)
        qubo_button = QPushButton("Kwantowe wyżarzanie")
        qubo_button.clicked.connect(self.status_dock_widget.start_processing)

        layout_wybor.addWidget(heuristic_button)
        layout_wybor.addWidget(linapprox_button)
        layout_wybor.addWidget(qubo_button)
        layout_wybor.addStretch(0)

        wybor_widget = QWidget()
        wybor_widget.setLayout(layout_wybor)
        dock1.setWidget(wybor_widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.status_dock_widget)

    def create_toolbars(self):
        start_stop_toolbar = QToolBar("startStopToolbar")
        self.addToolBar(Qt.TopToolBarArea, start_stop_toolbar)

        self.start_calc_button.clicked.connect(self.start_calculations)
        self.stop_calc_button.clicked.connect(self.stop_calculations)

        start_stop_toolbar.addWidget(self.start_calc_button)
        start_stop_toolbar.addWidget(self.stop_calc_button)

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

            self.markdown_window.setWindowTitle("Informacje")
            layout = QVBoxLayout()
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setHtml(html)
            layout.addWidget(text_edit)
            self.markdown_window.setLayout(layout)
            self.markdown_window.show()
            geometry = self.screen().availableGeometry()
            self.markdown_window.setFixedSize(int(geometry.width() * 0.4), int(geometry.height() * 0.35))

        except Exception as e:
            self.filepath_label.setText(f"Błąd podczas otwierania pliku: {e}")

    def start_calculations(self):
        self.thread = QThread()
        self.worker = Worker()  # Pass the algorithm
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.calc.finished.connect(self.thread.quit)
        self.worker.calc.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.calc.emitProgress.connect(self.update_progress)
        self.worker.calc.finished.connect(self.finished_calc)

        self.thread.start()

        self.start_calc_button.setEnabled(False)
        self.stop_calc_button.setEnabled(True)

    def stop_calculations(self):
        self.worker.calc.stop = True
        self.start_calc_button.setEnabled(True)
        self.stop_calc_button.setEnabled(True)

    def finished_calc(self, message):
        print(f"Finished, solve: {message}")
        self.status_dock_widget.value_label.setText(f"Wynik: {message}")
        self.start_calc_button.setEnabled(True)

    def update_progress(self, message):
        self.status_dock_widget.value_label.setText(f"Aktualna wartość: {message}")
