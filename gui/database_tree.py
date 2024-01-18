from PyQt6.QtWidgets import QMainWindow, QSplitter, QTabWidget
from .sql_editor import SqlEditor


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.splitter = QSplitter()
        self.editor = SqlEditor()

        self.splitter.addWidget(self.editor)

        # self.setCentralWidget(self.editor)
        self.tabs.addTab(SqlEditor(), "SQL console")
        self.tabs.addTab(SqlEditor(), "SQL console2")
        self.setCentralWidget(self.tabs)
        self.setWindowTitle("SQL editor")
