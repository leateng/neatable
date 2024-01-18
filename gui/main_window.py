from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QSplitter, QTabWidget
from .sql_editor import SqlEditor


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SQL editor")
        self.editor = SqlEditor()
        self.editor2 = SqlEditor()
        self.splitter = QSplitter()
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.editor2)
        self.splitter.setSizes([10000, 30000])
        self.setCentralWidget(self.splitter)
