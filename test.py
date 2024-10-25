import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                               QDockWidget, QLabel, QPushButton, QWidget)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Ustawienie centralnego widgetu (np. edytor tekstu)
        self.central_widget = QTextEdit()
        self.setCentralWidget(self.central_widget)

        # Tworzenie dock widgetów
        self.create_dock_widgets()

    def create_dock_widgets(self):
        # Pierwszy dock widget
        dock1 = QDockWidget("Dockable", self)
        dock1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        label1 = QLabel("Dock Widget 1", dock1)
        dock1.setWidget(label1)

        # Dokowanie na lewą stronę
        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)

        # Drugi dock widget
        dock2 = QDockWidget("Another Dockable", self)
        dock2.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)

        button = QPushButton("Button in Dock", dock2)
        dock2.setWidget(button)

        # Dokowanie na górną stronę
        self.addDockWidget(Qt.TopDockWidgetArea, dock2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.setWindowTitle("Dock Widget Example")
    main.resize(800, 600)
    main.show()
    sys.exit(app.exec())
