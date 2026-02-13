import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from display import Display
from info import Info
from buttons import ButtonsGrid
from variables import WINDOW_ICON_PATH

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle("Calculator")

    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    display = Display()

    window.addWidgetToVLayout(info)
    window.addWidgetToVLayout(display)

    window.buttonsGrid = ButtonsGrid(display, info)
    window.vLayout.addLayout(window.buttonsGrid)

    display.eqPressed.connect(lambda: window.buttonsGrid.handleKey("="))
    display.delPressed.connect(lambda: window.buttonsGrid.handleKey("◀"))
    display.clearPressed.connect(lambda: window.buttonsGrid.handleKey("C"))
    display.inputPressed.connect(window.buttonsGrid.handleKey)
    display.operatorPressed.connect(window.buttonsGrid.handleKey)

    window.adjustFixedSize()
    window.setFocus()
    window.cw.setFocusPolicy(window.cw.StrongFocus)
    window.cw.setFocus()

    window.show()
    app.exec()
