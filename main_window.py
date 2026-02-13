from PySide6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QWidget
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)
        self.setWindowTitle('Calculator')
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)

    def makeMsgBox(self):
        return QMessageBox(self)

    def keyPressEvent(self, event):
        if not hasattr(self, "buttonsGrid"):
            return

        key = event.key()
        text = event.text()

        if text.isdigit() or text == ".":
            self.buttonsGrid.handleKey(text)

        elif text in "+-*/^":
            self.buttonsGrid.handleKey(text)

        elif key in (Qt.Key_Return, Qt.Key_Enter):
            self.buttonsGrid.handleKey("=")

        elif key == Qt.Key_Backspace:
            self.buttonsGrid.handleKey("◀")

        elif key == Qt.Key_Escape:
            self.buttonsGrid.handleKey("C")
