import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QColorDialog, QToolBar, QWidget
from PyQt6.QtGui import QPainter, QColor, QAction, QPolygon
from PyQt6.QtCore import Qt, QPoint

#Класс формы
class Shape:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = QColor("blue")
        self.selected = False

    def contains(self, px, py):
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

    def move(self, dx, dy, max_w, max_h):
        self.x = min(max(self.x + dx, 0), max_w - self.w)
        self.y = min(max(self.y + dy, 0), max_h - self.h)

    def resize(self, dw, dh, max_w, max_h):
        new_w = self.w + dw
        new_h = self.h + dh
        if new_w < 10 or new_h < 10:
            return
        if self.x + new_w > max_w or self.y + new_h > max_h:
            return
        self.w = new_w
        self.h = new_h

# Класс прямоугольника
class Rectangle(Shape):
    def draw(self, painter):
        painter.setBrush(self.color)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawRect(self.x, self.y, self.w, self.h)
        if self.selected:
            painter.setPen(Qt.GlobalColor.red)
            painter.drawRect(self.x, self.y, self.w, self.h)

# Класс круга
class Circle(Shape):
    def draw(self, painter):
        painter.setBrush(self.color)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawEllipse(self.x, self.y, self.w, self.h)
        if self.selected:
            painter.setPen(Qt.GlobalColor.red)
            painter.drawEllipse(self.x, self.y, self.w, self.h)

# Класс треугольника
class Triangle(Shape):
    def draw(self, painter):
        painter.setBrush(self.color)
        points = QPolygon([
            QPoint(self.x + self.w // 2, self.y),
            QPoint(self.x, self.y + self.h),
            QPoint(self.x + self.w, self.y + self.h)
        ])
        painter.setPen(Qt.GlobalColor.black)
        painter.drawPolygon(points)
        if self.selected:
            painter.setPen(Qt.GlobalColor.red)
            painter.drawPolygon(points)

# Класс для хранения фигур
class ShapeStorage:
    def __init__(self):
        self.shapes = []

    def add(self, shape):
        self.shapes.append(shape)

    def get_all(self):
        return self.shapes

    def clear_selection(self):
        for s in self.shapes:
            s.selected = False

    def get_selected(self):
        return [s for s in self.shapes if s.selected]

    def delete_selected(self):
        self.shapes = [s for s in self.shapes if not s.selected]

# Класс для рисования и обработки кликов
class Canvas(QWidget):
    def __init__(self, storage, parent):
        super().__init__()
        self.storage = storage
        self.parent = parent

    def paintEvent(self, event):
        painter = QPainter(self)
        for s in self.storage.get_all():
            s.draw(painter)

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        x, y = pos.x(), pos.y()

        clicked_shape = None
        for s in reversed(self.storage.get_all()):
            if s.contains(x, y):
                clicked_shape = s
                break

        if clicked_shape:
            # Ctrl + клик для множественного выделения
            if not (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
                self.storage.clear_selection()
            clicked_shape.selected = not clicked_shape.selected
        else:
            # создаём новую фигуру с центром в точке клика
            if self.parent.current_tool == "rect":
                w, h = 80, 60
                self.storage.add(Rectangle(x - w // 2, y - h // 2, w, h))
            elif self.parent.current_tool == "circle":
                size = 60
                self.storage.add(Circle(x - size // 2, y - size // 2, size, size))
            elif self.parent.current_tool == "triangle":
                w, h = 80, 60
                self.storage.add(Triangle(x - w // 2, y - h // 2, w, h))

        self.update()

# Главное окно редактора
class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Визуальный редактор")
        self.resize(800, 600)

        self.storage = ShapeStorage()
        self.current_tool = "rect"

        self.canvas = Canvas(self.storage, self)
        self.setCentralWidget(self.canvas)

        self.init_toolbar()

    def init_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        toolbar.addAction(self.create_action("Прямоугольник", "rect"))
        toolbar.addAction(self.create_action("Круг", "circle"))
        toolbar.addAction(self.create_action("Треугольник", "triangle"))

        color_btn = QAction("Цвет", self)
        color_btn.triggered.connect(self.change_color)
        toolbar.addAction(color_btn)

    def create_action(self, name, tool):
        action = QAction(name, self)
        action.triggered.connect(lambda checked=False: self.set_tool(tool))
        return action

    def set_tool(self, tool):
        self.current_tool = tool

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            for s in self.storage.get_selected():
                s.color = color
        self.canvas.update()

    def keyPressEvent(self, event):
        dx = dy = dw = dh = 0
        if event.key() == Qt.Key.Key_Left: dx = -10
        elif event.key() == Qt.Key.Key_Right: dx = 10
        elif event.key() == Qt.Key.Key_Up: dy = -10
        elif event.key() == Qt.Key.Key_Down: dy = 10
        elif event.key() in (Qt.Key.Key_Plus, Qt.Key.Key_Equal): dw = dh = 10
        elif event.key() == Qt.Key.Key_Minus: dw = dh = -10
        elif event.key() == Qt.Key.Key_Delete: self.storage.delete_selected()

        max_w = self.canvas.width()
        max_h = self.canvas.height()
        for s in self.storage.get_selected():
            s.move(dx, dy, max_w, max_h)
            s.resize(dw, dh, max_w, max_h)

        self.canvas.update()

# Запуск приложения
app = QApplication(sys.argv)
window = Editor()
window.show()
sys.exit(app.exec())