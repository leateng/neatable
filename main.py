from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QKeyEvent
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QStyleFactory
from PyQt5.Qsci import QsciLexerSQL, QsciScintilla
from os import sys


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.editor = QsciScintilla()
        self.font = QFont("FiraCode Nerd Font Mono", 14)
        # font.setPointSize(24)
        self.lexer = QsciLexerSQL()

        self.editor.setUtf8(True)
        self.editor.setFont(self.font)
        self.editor.setWrapMode(QsciScintilla.WrapMode.WrapWord)
        self.editor.setWrapVisualFlags(
            QsciScintilla.WrapVisualFlag.WrapFlagByBorder,
            QsciScintilla.WrapVisualFlag.WrapFlagNone,
        )
        self.editor.setIndentationsUseTabs(False)
        self.editor.setIndentationGuides(True)
        self.editor.setAutoIndent(True)
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretForegroundColor(QColor("#ff0000ff"))
        self.editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.editor.setMarginWidth(0, "0000")
        self.editor.setMarginsForegroundColor(QColor("#ff888888"))
        self.editor.setLexer(self.lexer)
        self.setCentralWidget(self.editor)
        self.setWindowTitle("SQL editor")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_F5:
            if self.editor.hasFocus() and self.editor.hasSelectedText():
                sel_text = self.editor.selectedText()
                print(f"execute sql: {sel_text}")
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create("Fusion"))

    win = MainWindow()
    win.resize(1280, 800)
    win.show()

    app.exec_()
