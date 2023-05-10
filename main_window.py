from PyQt5.QtWidgets import QMainWindow
from sql_editor import SqlEditor


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.editor = SqlEditor()
        self.setCentralWidget(self.editor)
        self.setWindowTitle("SQL editor")
