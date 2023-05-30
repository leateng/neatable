import sqlglot
from PyQt6 import QtCore, QtWidgets
from PyQt6.Qsci import QsciLexerCustom
from PyQt6.Qsci import QsciLexerSQL
from PyQt6.Qsci import QsciScintilla
from PyQt6.Qsci import QsciScintillaBase
from PyQt6.QtGui import QColor, QPainter, QWheelEvent
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from tree_sitter import Language
from tree_sitter import Parser
import re


# from IPython import embed


class LexerSQL(QsciLexerCustom):
    def __init__(self, parent=None):
        super(LexerSQL, self).__init__(parent)
        self._init_styles()
        self._init_parser()
        self.sql_keyword_reg = re.compile("keyword_\w+")

    def language(self):
        return "SQL"

    def description(self, style_nr):
        if style_nr == 0:
            return "myStyle_0"
        elif style_nr == 1:
            return "myStyle_1"
        elif style_nr == 2:
            return "myStyle_2"
        elif style_nr == 3:
            return "myStyle_3"
        else:
            return ""

    # Called everytime the editors text has changed
    def styleText(self, start, end):
        text = self.parent().text()
        tree = self.parser.parse(bytes(text, "utf8"))
        self.syntaxStyling(tree)

    def syntaxStyling(self, syntax_tree):
        self.startStyling(0)
        self.traverse(syntax_tree.root_node)

    def traverse(self, node):
        # print(f"{node.type}: {node.text}({node.start_byte}, {node.end_byte})")

        if self.sql_keyword_reg.match(node.type):
            self.startStyling(node.start_byte, 0)
            self.setStyling(node.end_byte - node.start_byte, 2)
        elif node.type == "table_reference":
            self.startStyling(node.start_byte, 0)
            self.setStyling(node.end_byte - node.start_byte, 1)
        elif node.type == "literal":
            self.startStyling(node.start_byte, 0)
            self.setStyling(node.end_byte - node.start_byte, 3)

        for child in node.children:
            self.traverse(child)

    def _init_styles(self):
        self.font1 = QFont("FiraCode Nerd Font Mono", 12)
        self.font1.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

        # Default text settings
        # ----------------------
        self.setDefaultColor(QColor("#ff000000"))
        self.setDefaultPaper(QColor("#ffffffff"))
        self.setDefaultFont(self.font1)

        # Initialize colors per style
        # ----------------------------
        self.setColor(QColor("#ff000000"), 0)  # Style 0: black
        self.setColor(QColor("#ff7f0000"), 1)  # Style 1: red
        self.setColor(QColor("#ff0000bf"), 2)  # Style 2: blue
        self.setColor(QColor("#ff067d17"), 3)  # Style 3: green

        # Initialize paper colors per style
        # ----------------------------------
        self.setPaper(QColor("#ffffffff"), 0)  # Style 0: white
        self.setPaper(QColor("#ffffffff"), 1)  # Style 1: white
        self.setPaper(QColor("#ffffffff"), 2)  # Style 2: white
        self.setPaper(QColor("#ffffffff"), 3)  # Style 3: white

        # Initialize fonts per style
        # ---------------------------
        # Style 0: 14pt bold
        self.setFont(QFont("Consolas", 12, weight=QFont.Weight.Normal), 0)
        # Style 1: 14pt bold
        self.setFont(QFont("Consolas", 12, weight=QFont.Weight.Bold), 1)
        # Style 2: 14pt bold
        self.setFont(QFont("Consolas", 12, weight=QFont.Weight.Bold), 2)
        self.setFont(QFont("Consolas", 12, weight=QFont.Weight.Normal), 3)

    def _init_parser(self):
        lang = Language("parser/sql.dll", "sql")
        self.parser = Parser()
        self.parser.set_language(lang)


class EditorWidget(QsciScintilla):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # format sql
        if event.key() == QtCore.Qt.Key.Key_F5:
            if self.hasFocus() and self.hasSelectedText():
                sel_text = self.selectedText()
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
                self.replaceSelectedText(pretty_sql)
                event.accept()
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        super().wheelEvent(event)
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            self.linesChanged.emit()


class SqlEditor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.editor = EditorWidget()
        self.editor.setEolMode(QsciScintilla.EolMode.EolUnix)
        # self.font = QFont("FiraCode Nerd Font Mono", 12)
        # self.lexer = QsciLexerSQL()
        self.lexer = LexerSQL(self.editor)
        self.editor.setLexer(self.lexer)
        # self.lexer.setFont(self.font)

        self.editor.setUtf8(True)
        # self.editor.setFont(self.font)
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

        self.editor.linesChanged.connect(self.onLinesChanged)

        self._layout.addWidget(self.editor)
        self.setLayout(self._layout)

    def onLinesChanged(self) -> None:
        line_number = self.editor.lines()
        line_number_width = len(str(line_number))
        current_margin_width = self.editor.marginWidth(0)
        if line_number_width != current_margin_width - 1:
            self.editor.setMarginWidth(0, "0" * (line_number_width + 1))
