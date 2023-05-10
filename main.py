from PyQt5.QtWidgets import QApplication, QStyleFactory
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    QApplication.setStyle(QStyleFactory.create("Fusion"))

    win = MainWindow()
    win.resize(1280, 800)
    win.show()

    app.exec_()
