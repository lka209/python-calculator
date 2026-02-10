from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QKeyEvent
from variables import MINIMUM_WIDTH, TEXT_MARGIN, MEDIUM_FONT_SIZE
from utils import isEmpty, isNumOrDot


class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        margins = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f"font-size: {MEDIUM_FONT_SIZE}px;")
        self.setMinimumHeight(MEDIUM_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in (
            KEYS.Key_Enter,
            KEYS.Key_Return,
            KEYS.Key_Equal,
        )

        isDelete = key in (
            KEYS.Key_Backspace,
            KEYS.Key_Delete,
        )

        isEsc = key in (
            KEYS.Key_Escape,
            KEYS.Key_C,
        )

        isOperator = key in (
            KEYS.Key_Plus,
            KEYS.Key_Minus,
            KEYS.Key_Slash,
            KEYS.Key_Asterisk,
            KEYS.Key_P,
        )

        # ENTER / =
        if isEnter:
            self.eqPressed.emit()
            event.accept()
            return

        # BACKSPACE / DELETE
        if isDelete:
            self.delPressed.emit()
            event.accept()
            return

        # ESC / C
        if isEsc:
            self.clearPressed.emit()
            event.accept()
            return

        # OPERADORES
        if isOperator:
            if text.lower() == "p":
                text = "^"
            self.operatorPressed.emit(text)
            event.accept()
            return

        # IGNORA TECLAS SEM TEXTO
        if isEmpty(text):
            event.ignore()
            return

        # NÚMEROS E PONTO
        if isNumOrDot(text):
            self.inputPressed.emit(text)
            event.accept()
            return

        super().keyPressEvent(event)
