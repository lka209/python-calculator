import math
from typing import TYPE_CHECKING
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton
from utils import converToNumber, isEmpty, isNumOrDot, isValidNumber
from variables import MEDIUM_FONT_SIZE

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(
        self,
        display: "Display",
        info: "Info",
        window: "MainWindow",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ["C", "◀", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["N", "0", ".", "="],
        ]

        self.display = display
        self.info = info
        self.window = window

        self._equation = ""
        self._equationInitialValue = "Do The Math"
        self._left = None
        self._right = None
        self._op = None

        self.display.setText(self._equationInitialValue)
        self._makeGrid()
        
    def _makeGrid(self):
        for row_index, row in enumerate(self._gridMask):
            for col_index, button_text in enumerate(row):
                button = Button(button_text)
                self.addWidget(button, row_index, col_index)

                button.clicked.connect(
                    lambda checked, text=button_text: self._buttonClicked(text)
                )
    @Slot()
    def _buttonClicked(self, text: str):

        # LIMPAR
        if text == "C":
            self._left = None
            self._right = None
            self._op = None
            self.display.clear()
            return

        if text == "◀":
            self.display.setText(self.display.text()[:-1])
            return

        # INVERTER SINAL
        if text == "N":
            current = self.display.text()
            if current.startswith("-"):
                self.display.setText(current[1:])
            else:
                self.display.setText("-" + current)
            return

        if text == "=":
            self._calculate()
            return

        if text in ["+", "-", "*", "/", "^"]:
            self._left = converToNumber(self.display.text())
            self._op = text
            self.display.clear()
            return

        if isNumOrDot(text):
            current_text = self.display.text()
            new_text = current_text + text

            if isValidNumber(new_text):
                self.display.setText(new_text)

    def _calculate(self):
        if self._left is None or self._op is None:
            return

        self._right = converToNumber(self.display.text())

        try:
            if self._op == "+":
                result = self._left + self._right
            elif self._op == "-":
                result = self._left - self._right
            elif self._op == "*":
                result = self._left * self._right
            elif self._op == "/":
                result = self._left / self._right
            elif self._op == "^":
                result = math.pow(self._left, self._right)
            else:
                return

            self.display.setText(str(result))

            self._left = result
            self._right = None
            self._op = None

        except Exception:
            self.display.setText("Error")
