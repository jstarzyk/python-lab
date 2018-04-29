#!/usr/bin/env python
"""
A JSON-based image generator.
"""

import argparse
import json
import sys

from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QColor, QPen, QPainter, QPolygonF, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication


__author__ = 'Jakub Starzyk'
__email__ = 'jstarzyk98@gmail.com'


def get_valid_color(spec, color_type, palette, default):
    try:
        color = eval(spec[color_type], None, None)
    except (NameError, SyntaxError):
        color = spec[color_type]
    except KeyError:
        return default

    if type(color) is tuple:
        qc = QColor(*color)
    elif type(color) is str and palette and color in palette:
        qc = QColor(palette[color])
    else:
        qc = QColor(color)

    if not qc.isValid():
        qc = default

    return qc


class Media:
    def __init__(self, screen, palette):
        self.is_valid = True
        try:
            self.width = screen['width']
            self.height = screen['height']
            if self.width < 1 or self.height < 1:
                self.is_valid = False
            self.bg_color = get_valid_color(screen, 'bg_color', palette, QColor('black'))
            self.fg_color = get_valid_color(screen, 'fg_color', palette, QColor('red'))
        except (KeyError, TypeError):
            self.is_valid = False


class Figure:
    def __init__(self, spec, palette, default):
        self.is_valid = True
        self.color = get_valid_color(spec, 'color', palette, default)
        self.antialiased = False

    def draw_with(self, painter):
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(self.color)
        painter.setRenderHint(QPainter.Antialiasing, self.antialiased)


class Point(Figure):
    def __init__(self, spec, palette, default):
        super().__init__(spec, palette, default)
        try:
            self.point = QPointF(spec['x'], spec['y'])
        except (KeyError, TypeError):
            self.is_valid = False

    def draw_with(self, painter):
        super().draw_with(painter)
        painter.setPen(self.color)
        painter.drawPoint(self.point)


class Polygon(Figure):
    def __init__(self, spec, palette, default):
        super().__init__(spec, palette, default)
        self.antialiased = True
        try:
            points = []
            for p in spec['points']:
                try:
                    points.append(QPointF(p[0], p[1]))
                except (TypeError, IndexError):
                    pass
            self.polygon = QPolygonF(points)
        except (KeyError, TypeError):
            self.is_valid = False

    def draw_with(self, painter):
        super().draw_with(painter)
        painter.drawPolygon(self.polygon)


class Rectangle(Figure):
    def __init__(self, spec, palette, default):
        super().__init__(spec, palette, default)
        try:
            width = spec['width']
            height = spec['height']
            x = spec['x'] - width / 2
            y = spec['y'] - height / 2
            self.rect = QRectF(x, y, width, height)
        except (KeyError, TypeError):
            self.is_valid = False

    def draw_with(self, painter):
        super().draw_with(painter)
        painter.drawRect(self.rect)


class Square(Figure):
    def __init__(self, spec, palette, default):
        super().__init__(spec, palette, default)
        try:
            size = spec['size']
            x = spec['x'] - size / 2
            y = spec['y'] - size / 2
            self.rect = QRectF(x, y, size, size)
        except (KeyError, TypeError):
            self.is_valid = False

    def draw_with(self, painter):
        super().draw_with(painter)
        painter.drawRect(self.rect)


class Circle(Figure):
    def __init__(self, spec, palette, default):
        super().__init__(spec, palette, default)
        self.antialiased = True
        try:
            radius = spec['radius']
            self.point = QPointF(spec['x'], spec['y'])
            if type(radius) is int or type(radius) is float:
                self.radius = radius
            else:
                raise TypeError
        except (KeyError, TypeError):
            self.is_valid = False

    def draw_with(self, painter):
        super().draw_with(painter)
        painter.drawEllipse(self.point, self.radius, self.radius)


class Drawing(QWidget):
    def __init__(self, media, pixmap):
        super().__init__()
        self.setFixedSize(media.width, media.height)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.drawPixmap(self.rect(), self.pixmap)


def draw_image(figures, screen, palette):
    media = Media(screen, palette)
    if not media.is_valid:
        return None, None
    image = QImage(media.width, media.height, QImage.Format_RGB32)
    image.fill(media.bg_color)
    painter = QPainter(image)

    for f in figures:
        try:
            figure_class = globals()[f['type'].capitalize()]
            figure = figure_class(f, palette, media.fg_color)
            if figure.is_valid:
                figure.draw_with(painter)
        except KeyError:
            pass

    return media, image


def parse_json(input_file):
    with open(input_file) as file:
        content = json.loads(file.read())
        try:
            figures = content['Figures']
        except KeyError:
            figures = []
        try:
            screen = content['Screen']
        except KeyError:
            screen = {'width': 800, 'height': 600, 'bg_color': 'black', 'fg_color': 'red'}
        try:
            palette = content['Palette']
        except KeyError:
            palette = None

    return figures, screen, palette


def setup_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='JSON file containing image description')
    parser.add_argument('-o', '--output', help='generated image')
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    media, image = draw_image(*parse_json(args.input))

    if not media or not image:
        return

    if args.output:
        image.save(args.output, 'PNG', -1)

    app = QApplication(sys.argv)
    drawing = Drawing(media, QPixmap(image))
    drawing.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
