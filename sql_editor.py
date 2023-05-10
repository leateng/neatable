from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QKeyEvent
from PyQt5.Qsci import QsciLexerSQL, QsciScintilla
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget


class SqlEditor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.editor = QsciScintilla()
        self.font = QFont("FiraCode Nerd Font Mono", 14)
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

        self._layout.addWidget(self.editor)
        self.setLayout(self._layout)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_F5:
            if self.editor.hasFocus() and self.editor.hasSelectedText():
                sel_text = self.editor.selectedText()
                print(f"execute sql: {sel_text}")
        else:
            super().keyPressEvent(event)
