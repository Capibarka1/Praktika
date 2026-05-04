import sys
from PySide6.QtWidgets import QApplication
from MainMenuWindow import MainMenu

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())
    sys.exit(app.exec())