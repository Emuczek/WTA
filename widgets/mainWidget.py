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

from modules.objectivefunction import objective
from widgets.centralVisualization import GraphWidget
from modules.AlgorytmQP import CalculationQP
from modules.AlgorytmFHO import CalculationFHO
from modules.Contraint import CalculationCONST
from modules.LinearAprox import CalculationAPROX


class Worker(QObject):
    finished = Signal()

    def __init__(self, file_path, method_choice):
        super().__init__()
        if method_choice == 0:
            self.calc = CalculationCONST()
        if method_choice == 1:
            self.calc = CalculationAPROX()
        if method_choice == 2:
            self.calc = CalculationFHO()
        if method_choice == 3:
            self.calc = CalculationQP()
        self.current_file_path = file_path

    def defstop(self):
        self.calc.stop = True

    def run(self):
        self.calc.calculate(self.current_file_path)
        self.finished.emit()


class StopwatchWorker(QObject):
    time_updated = Signal(str)
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_time)
        self.start_time = None
        self.elapsed_time = 0
        print("stopwatch init")

    def start(self):
        self.start_time = time.time()
        self.timer.start()
        print("Started!")

    def stop(self):
        self.timer.stop()
        self.finished.emit()
        print("Stopped!")

    def update_time(self):
        self.elapsed_time = str(round(float(time.time() - self.start_time), 3))
        print(self.elapsed_time)
        self.time_updated.emit(self.elapsed_time)


class StatusDockWidget(QDockWidget):
    def __init__(self):
        super().__init__("Informacje o przebiegu")

        self.current_value = None
        self.status_widget = QWidget()
        self.setWidget(self.status_widget)

        layout = QVBoxLayout()
        layout.addStretch(0)
        self.time_label = QLabel("Czas: 0s")
        layout.addWidget(self.time_label)
        self.value_label = QLabel("Aktualna wartość: 0")
        layout.addWidget(self.value_label)
        self.status_widget.setLayout(layout)


class MainWindow(QMainWindow):

    file_path = Signal(str)

    def __init__(self):
        super().__init__()

        self.methodchoice = 0
        self.stopwatch_thread = None
        self.stopwatch_worker = None
        self.selected_file_path = str()
        self.status_dock_widget = StatusDockWidget()
        self.markdown_filepath = "modules/documentation.md"
        self.markdown_window = QWidget()
        self.thread = None
        self.worker = None

        # Central widget

        self.central_widget = GraphWidget([])
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
        import_action.setStatusTip("Kliknij tutaj, aby zaimportować plik .JSON")
        import_action.triggered.connect(self.open_file_dialog)

        documentation_action = QAction("Informacje na temat programu", self)
        documentation_action.setStatusTip("Kliknij tutaj, aby dowiedzieć się wiecej")
        documentation_action.triggered.connect(self.display_markdown)

        self.file_menu.addAction(import_action)
        self.info_menu.addAction(documentation_action)

    def create_dock_widgets(self):
        dock1 = QDockWidget("Wybór metody", self)
        dock1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        layout_wybor = QVBoxLayout()
        self.constraint_button = QPushButton("Programowanie ogarniczeń")
        self.constraint_button.setStyleSheet("""
        background-color: lightgreen;
        color: black;
        """)
        self.constraint_button.clicked.connect(self.changeto_const)
        self.linapprox_button = QPushButton("Aproksymacja liniowa")
        self.linapprox_button.clicked.connect(self.changeto_aprox)
        self.heuristic_fire_button = QPushButton("Heurystyka 'Fire Hawk Optimizer'")
        self.heuristic_fire_button.clicked.connect(self.changeto_fho)
        self.heuristic_quiz_button = QPushButton("Heurystyka 'Quiz Problem Heuristic'")
        self.heuristic_quiz_button.clicked.connect(self.changeto_qp)

        layout_wybor.addWidget(self.constraint_button)
        layout_wybor.addWidget(self.linapprox_button)
        layout_wybor.addWidget(self.heuristic_fire_button)
        layout_wybor.addWidget(self.heuristic_quiz_button)
        layout_wybor.addStretch(0)

        wybor_widget = QWidget()
        wybor_widget.setLayout(layout_wybor)
        dock1.setWidget(wybor_widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.status_dock_widget)

        self.buttons = [
            self.constraint_button,
            self.linapprox_button,
            self.heuristic_fire_button,
            self.heuristic_quiz_button
        ]

        # Podłączenie funkcji wyboru
        for button in self.buttons:
            button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        clicked_button = self.sender()  # Przycisk, który został kliknięty

        # Resetowanie stylu wszystkich przycisków
        for button in self.buttons:
            button.setStyleSheet("")  # Domyślny styl

        # Ustawienie nowego stylu dla klikniętego przycisku
        clicked_button.setStyleSheet("""
        background-color: lightgreen;
        color: black;
        """)

    def changeto_const(self):
        self.methodchoice = 0

    def changeto_aprox(self):
        self.methodchoice = 1

    def changeto_fho(self):
        self.methodchoice = 2

    def changeto_qp(self):
        self.methodchoice = 3


    def create_toolbars(self):
        start_stop_toolbar = QToolBar("startStopToolbar")
        self.addToolBar(Qt.TopToolBarArea, start_stop_toolbar)

        self.start_calc_button.clicked.connect(self.start_calculations)
        self.stop_calc_button.clicked.connect(self.stop_calculations)

        self.start_calc_button.setEnabled(False)
        self.stop_calc_button.setEnabled(False)

        start_stop_toolbar.addWidget(self.start_calc_button)
        start_stop_toolbar.addWidget(self.stop_calc_button)

    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("JSON files (*.json)")

        if file_dialog.exec():
            self.selected_file_path = file_dialog.selectedFiles()[0]
            self.filepath_label.setText(f"Wybrany plik: {self.selected_file_path}")

        self.start_calc_button.setEnabled(True)

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
        self.stopwatch_thread = QThread()
        self.worker = Worker(self.selected_file_path, self.methodchoice)
        self.stopwatch_worker = StopwatchWorker()
        self.worker.moveToThread(self.thread)
        self.stopwatch_worker.moveToThread(self.stopwatch_thread)

        self.thread.started.connect(self.worker.run)
        self.worker.calc.finished.connect(self.thread.quit)
        self.worker.calc.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.calc.emitProgress.connect(self.update_progress)
        self.worker.calc.finished.connect(self.finished_calc)

        self.stopwatch_thread.started.connect(self.stopwatch_worker.start)  # Start stopwatch
        self.stopwatch_worker.time_updated.connect(lambda t: self.status_dock_widget.time_label.setText(f"Czas: {t}s"))
        self.stopwatch_worker.finished.connect(self.stopwatch_thread.quit)
        self.stopwatch_thread.finished.connect(self.stopwatch_thread.deleteLater)  # Cleanup

        self.thread.start()
        self.stopwatch_thread.start()

        self.start_calc_button.setEnabled(False)
        if self.methodchoice >= 2:
            self.stop_calc_button.setEnabled(True)

    def stop_calculations(self):
        self.worker.calc.stop = True
        self.start_calc_button.setEnabled(True)
        self.stop_calc_button.setEnabled(False)

    def finished_calc(self, message):
        self.stopwatch_worker.stop()
        self.central_widget = GraphWidget(message)
        self.setCentralWidget(self.central_widget)
        print(f"Finished, solve: {message}")
        self.status_dock_widget.value_label.setText(f"Wynik: {round(objective(self.selected_file_path, message, False),3)}")
        self.start_calc_button.setEnabled(True)
        self.stop_calc_button.setEnabled(False)

    def update_progress(self, message):
        self.status_dock_widget.value_label.setText(f"Aktualna wartość:"
                                                    f" {round(objective(self.selected_file_path, message, False),3)}")
