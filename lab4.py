import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget


class Shape:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Canvas(QWidget):
    def __init__(self):
        super().__init__()


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Визуальный редактор")
        self.resize(800, 600)

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)


app = QApplication(sys.argv)
window = Editor()
window.show()
sys.exit(app.exec())