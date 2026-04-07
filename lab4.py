import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget


class Shape:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, px, py):
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


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