from PyQt6.QtWidgets import QApplication, QStyleFactory
from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    QApplication.setStyle(QStyleFactory.create("fusion"))

    win = MainWindow()
    win.resize(1280, 800)
    win.show()

    app.exec()
