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
     key = event.key()
     text = event.text()
     KEYS = Qt.Key

  
    if key in (KEYS.Key_Return, KEYS.Key_Enter, KEYS.Key_Equal):
        self.eqPressed.emit()
        return

    if key in (KEYS.Key_Backspace, KEYS.Key_Delete):
        self.delPressed.emit()
        return

    if key == KEYS.Key_Escape:
        self.clearPressed.emit()
        return

    if KEYS.Key_0 <= key <= KEYS.Key_9:
        self.inputPressed.emit(str(key - KEYS.Key_0))
        return

    if key in (KEYS.Key_Period, KEYS.Key_Comma):
        self.inputPressed.emit(".")
        return

    if key in (
        KEYS.Key_Plus,
        KEYS.Key_Minus,
        KEYS.Key_Slash,
        KEYS.Key_Asterisk,
    ):
        self.operatorPressed.emit(text)
        return

    if key == KEYS.Key_P:
        self.operatorPressed.emit("^")
        return
    
    super().keyPressEvent(event)

