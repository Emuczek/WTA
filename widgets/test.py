import sys
import time
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QVBoxLayout, QLabel,
    QProgressBar, QWidget, QPushButton
)

class Worker(QThread):
    # Sygnalizuje aktualizację postępu
    progress_updated = Signal(int)
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.should_stop = False  # Flaga do zatrzymywania obliczeń

    def run(self):
        # Funkcja symulująca długotrwałe obliczenia
        current_value = 0
        while current_value < 100:
            if self.should_stop:
                break  # Zatrzymaj obliczenia, jeśli flaga jest ustawiona
            time.sleep(0.1)  # Symuluj obliczenia
            current_value += 1  # Zwiększamy aktualną wartość
            self.progress_updated.emit(current_value)  # Emituj sygnał z nową wartością

        self.finished.emit()  # Emituj sygnał zakończenia

    def stop(self):
        self.should_stop = True  # Ustaw flagę zatrzymania

class StatusDockWidget(QDockWidget):
    def __init__(self):
        super().__init__("Status")

        # Centralny widget dla dock widgeta
        self.status_widget = QWidget()
        self.setWidget(self.status_widget)

        # Layout
        layout = QVBoxLayout()

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

        # Przycisk do rozpoczęcia obliczeń
        self.start_button = QPushButton("Rozpocznij obliczenia")
        self.start_button.clicked.connect(self.start_processing)
        layout.addWidget(self.start_button)

        # Przycisk do zatrzymania obliczeń
        self.stop_button = QPushButton("Zatrzymaj obliczenia")
        self.stop_button.clicked.connect(self.stop_processing)
        layout.addWidget(self.stop_button)

        # Worker do wykonywania obliczeń w oddzielnym wątku
        self.worker = Worker()
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.processing_finished)

    @Slot()
    def start_processing(self):
        self.worker.should_stop = False  # Resetujemy flagę zatrzymania
        self.worker.start()  # Uruchamiamy wątek

    @Slot(int)
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.value_label.setText(f"Aktualna wartość: {value}")

    @Slot()
    def processing_finished(self):
        self.time_label.setText("Czas: zakończone")

    @Slot()
    def stop_processing(self):
        self.worker.stop()  # Ustaw flagę zatrzymania
        self.worker.quit()  # Zatrzymaj wątek (można też użyć `terminate()`)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Status Dock Widget Example")

        # Dodaj dock widget do głównego okna
        self.status_dock_widget = StatusDockWidget()
        self.addDockWidget(Qt.RightDockWidgetArea, self.status_dock_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.resize(600, 400)
    main_window.show()
    sys.exit(app.exec())
