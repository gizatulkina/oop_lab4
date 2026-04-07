import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt


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


class Rectangle(Shape):
    def draw(self, painter):
        painter.setBrush(Qt.GlobalColor.blue)
        painter.drawRect(self.x, self.y, self.w, self.h)


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []

    def paintEvent(self, event):
        painter = QPainter(self)
        for shape in self.shapes:
            shape.draw(painter)


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