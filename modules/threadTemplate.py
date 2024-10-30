import sys
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget)
from PySide6.QtCore import QThread, Signal, QObject


class Worker(QObject):
    finished = Signal()
    progress = Signal(str)  # Signal to send updates

    def __init__(self, algorithm_function):
        super().__init__()
        self._isRunning = True
        self.algorithm_function = algorithm_function


    def run(self):
        while self._isRunning:
            # Replace this with your actual algorithm call
            result = self.algorithm_function()
            self.progress.emit(str(result))  # Emit the result or progress
            time.sleep(1)  # Simulate some work

        self.finished.emit()


    def stop(self):
        self._isRunning = False


class MainWindow(QMainWindow):
    def __init__(self, algorithm_function):  # Pass the algorithm function
        super().__init__()

        self.algorithm_function = algorithm_function # Store the function

        self.start_button = QPushButton("Start Calculations")
        self.stop_button = QPushButton("Stop Calculations")
        self.stop_button.setEnabled(False)  # Initially disabled


        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        self.start_button.clicked.connect(self.start_calculations)
        self.stop_button.clicked.connect(self.stop_calculations)

        self.thread = None
        self.worker = None


    def start_calculations(self):
        self.thread = QThread()
        self.worker = Worker(self.algorithm_function)  # Pass the algorithm
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)  # Clean up the thread
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.on_progress)  # Connect to progress signal


        self.thread.start()


        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_calculations(self):
        if self.worker:
            self.worker.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def on_progress(self, result):
        print(f"Result: {result}") # Or update a label, progress bar, etc.


# Example algorithm function (replace with your actual algorithm)
def my_algorithm():
    # Perform your calculations here.
    # This example just returns a random number:
    import random
    return random.randint(1, 100)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(my_algorithm)  # Pass the algorithm function
    window.show()
    sys.exit(app.exec())