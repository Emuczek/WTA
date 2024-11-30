from widgets.mainWidget import MainWindow
from PySide6.QtWidgets import QApplication
import sys
from PySide6 import QtWidgets

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget {
            background-color: #1e1e1e;  /* Ciemne tło */
            color: #dcdcdc;  /* Jasnoszary tekst */
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 20px;
        }

        QPushButton {
            background-color: #2d2d30;  /* Standardowe tło */
            color: #ffffff;  /* Kolor czcionki */
            font-weight: bold;
            padding: 10px;
            border: 2px solid #3e3e42;  /* Szara ramka */
            border-radius: 5px;
        }
        
        /* Podświetlenie, gdy mysz jest nad przyciskiem */
        QPushButton:hover {
            background-color: #3e3e42;  /* Jaśniejszy szary */
            border: 2px solid #0078d7;  /* Niebieska ramka na hover */
        }
        
        /* Zmiana koloru przy aktywacji (kliknięciu) */
        QPushButton:pressed {
            background-color: #0078d7;  /* Niebieskie tło */
            color: #ffffff;
            border: 2px solid #005a9e;  /* Ciemniejszy niebieski */
        }
        
        /* Wskazanie aktywnego (wybranego) przycisku */
        QPushButton:checked {
            background-color: #0078d7;  /* Niebieskie tło */
            color: #ffffff;  /* Biała czcionka */
            border: 2px solid #005a9e;  /* Aktywna ramka */
        }
        
        /* Przycisk nieaktywny (disabled) */
        QPushButton:disabled {
            background-color: #3e3e42;  /* Ciemny szary dla wyłączonych */
            color: #6c6c6c;  /* Przyciemniona czcionka */
            border: 2px solid #3e3e42;
        }

        QMenuBar {
            background-color: #2d2d30;
            color: #dcdcdc;
            border: 0px solid #3e3e42;
        }

        QMenu {
            background-color: #2d2d30;
            color: #dcdcdc;
        }

        QMenu::item::selected {
            background-color: #0078d7;  /* Podświetlenie opcji w menu */
        }

        QDockWidget::title {
            background-color: #2d2d30;
            text-align: center;
            padding: 4px;
            color: #dcdcdc;
        }

        QToolBar {
            background-color: #1e1e1e;
            border: 1px solid #3e3e42;
        }

        QLabel {
            color: #dcdcdc;
        }

        QTextEdit, QLineEdit {
            background-color: #252526;
            color: #ffffff;
            border: 1px solid #3e3e42;
            border-radius: 5px;
            padding: 5px;
        }

        QStatusBar {
            background-color: #2d2d30;
            color: #ffffff;
        }

        QProgressBar {
            background-color: #3e3e42;
            color: white;
            border: 1px solid #5a5a5a;
            text-align: center;
        }

        QProgressBar::chunk {
            background-color: #0078d7;
        }
    """)

    main = MainWindow()
    main.setWindowTitle("Weapon target assingment solver")
    main.show()
    sys.exit(app.exec())
