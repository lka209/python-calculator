# buttons_grid.py
import math
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton
from utils import converToNumber, isNumOrDot, isValidNumber
from variables import MEDIUM_FONT_SIZE


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display, info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display = display
        self.info = info
        self.buttonsGrid = ButtonsGrid(self.display, self.info)
        self.addWidgetToVLayout(self.buttonsGrid)
        self._left = None
        self._op = None
        self._reset_next = False

        self._gridMask = [
            ["C", "◀", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["N", "0", ".", "="],
        ]

        self.display.setText("0")
        self.info.setText("")
        self._makeGrid()

    def _makeGrid(self):
        for r, row in enumerate(self._gridMask):
            for c, text in enumerate(row):
                btn = Button(text)
                self.addWidget(btn, r, c)
                btn.clicked.connect(lambda checked, t=text: self._buttonClicked(t))

    def handleKey(self, text: str):
        self._buttonClicked(text)

    @Slot()
    def _buttonClicked(self, text: str):
        if text == "C":
            self._left = None
            self._op = None
            self._reset_next = False
            self.display.setText("0")
            self.info.setText("")
            return

        if text == "◀":
            current = self.display.text()
            self.display.setText(current[:-1] if len(current) > 1 else "0")
            return

        if text == "N":
            current = self.display.text()
            self.display.setText(current[1:] if current.startswith("-") else "-" + current)
            return

        if text == "=":
            self._calculate()
            self._op = None
            self._left = None
            self._reset_next = True
            self.info.setText("")
            return

        if text in ["+", "-", "*", "/", "^"]:
            current_value = self.display.text()
            if not isValidNumber(current_value):
                return

            if self._left is not None and self._op is not None:
                self._calculate()
            else:
                self._left = converToNumber(current_value)

            self._op = text
            self.info.setText(f"{self._left} {self._op}")
            self._reset_next = True
            return

        if isNumOrDot(text):
            new_text = text if self._reset_next or self.display.text() == "0" else self.display.text() + text
            if isValidNumber(new_text):
                self.display.setText(new_text)
                self._reset_next = False

    def _calculate(self):
        if self._left is None or self._op is None:
            return

        right_value = converToNumber(self.display.text())
        try:
            if self._op == "+":
                result = self._left + right_value
            elif self._op == "-":
                result = self._left - right_value
            elif self._op == "*":
                result = self._left * right_value
            elif self._op == "/":
                result = self._left / right_value
            elif self._op == "^":
                result = math.pow(self._left, right_value)
            else:
                return

            self.display.setText(str(result))
            self._left = result
            self._reset_next = True

        except Exception:
            self.display.setText("Error")
            self._left = None
            self._op = None
            self._reset_next = True
