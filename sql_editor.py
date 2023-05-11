from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QKeyEvent, QPainter
from PyQt5.Qsci import QsciLexerSQL, QsciScintilla, QsciScintillaBase
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
import sqlglot


class SqlEditor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.editor = QsciScintilla()
        self.font = QFont("FiraCode Nerd Font Mono", 12)
        self.lexer = QsciLexerSQL()
        self.lexer.setFont(self.font)

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
        self.editor.setCaretWidth(2)
        self.editor.setCaretForegroundColor(QColor("#275ce7"))
        self.editor.setCaretLineBackgroundColor(QColor("#eff3f4"))

        self.editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.editor.setMarginWidth(0, "00")
        self.editor.setMarginsForegroundColor(QColor("#ff888888"))
        self.editor.setMarginsBackgroundColor(QColor("#FFFFFF"))
        self.editor.setLexer(self.lexer)
        self.editor.linesChanged.connect(self.on_lines_changed)

        self._layout.addWidget(self.editor)
        self.setLayout(self._layout)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # format sql
        if event.key() == QtCore.Qt.Key.Key_F5:
            if self.editor.hasFocus() and self.editor.hasSelectedText():
                sel_text = self.editor.selectedText()
                try:
                    result = sqlglot.transpile(
                        sel_text,
                        read="postgres",
                        pretty=True,
                        error_level=sqlglot.ErrorLevel.IMMEDIATE,
                    )
                except BaseException as ex:
                    print(ex)
                    return

                pretty_sql = ";\n\n".join(result)
                self.editor.replaceSelectedText(pretty_sql)
        else:
            super().keyPressEvent(event)

    def on_lines_changed(self) -> None:
        line_number = self.editor.lines()
        line_number_width = len(str(line_number))
        current_margin_width = self.editor.marginWidth(0)
        if line_number_width != current_margin_width - 1:
            self.editor.setMarginWidth(0, "0" * (line_number_width + 1))
