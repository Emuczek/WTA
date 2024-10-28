from widgets.mainWidget import MainWidget
import sys
from PySide6 import QtWidgets

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.setWindowTitle("Weapon target assingment solver")
    main.show()
    sys.exit(app.exec())
