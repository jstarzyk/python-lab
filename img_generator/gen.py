#!/usr/bin/env python
"""
A JSON-formatted image description generator
"""

import argparse
import json
import math
import random


__author__ = 'Jakub Starzyk'
__email__ = 'jstarzyk98@gmail.com'


def gen_points(d, n, width, height):
    for i in range(n):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        d['Figures'].append({'type': 'point', 'x': x, 'y': y})

    return d


def gen_triangles(d, nx, width, height):
    res_x = width / nx
    res_y = res_x / 2 * 3 ** 0.5
    ny = int(math.ceil(height / res_y))

    for j in range(ny):
        for i in range(nx + j % 2):
            points = []
            off_x = - (j % 2) * (res_x / 2)
            points.append([i * res_x + off_x, (j + 1) * res_y])
            points.append([(i + 1) * res_x + off_x, (j + 1) * res_y])
            points.append([i * res_x + res_x / 2 + off_x, j * res_y])
            d['Figures'].append({'type': 'polygon', 'points': points})

    return d


def gen_squares(d, nx, width, height):
    res_x = width / 2 / nx
    ny = int(math.ceil(height / res_x))

    off_y = res_x / 2
    for j in range(ny):
        for i in range(nx):
            off_x = (j % 2) * res_x + res_x / 2
            x = off_x + 2 * i * res_x
            y = off_y + j * res_x
            d['Figures'].append({'type': 'square', 'x': x, 'y': y, 'size': res_x})

    return d


def gen_circles(d, nx, width, height):
    radius = width / 2 / nx
    ny = int(math.ceil(height / radius / 3 ** 0.5)) + 1

    for j in range(ny):
        off_y = j * radius * 3 ** 0.5
        for i in range(nx + 1 - (j % 2)):
            off_x = (j % 2) * radius
            x = off_x + 2 * i * radius
            y = off_y
            d['Figures'].append({'type': 'circle', 'x': x, 'y': y, 'radius': radius})

    return d


def gen(width, height, bg_color, fg_color, type, n):
    d = {'Screen': {'width': width, 'height': height, 'bg_color': bg_color, 'fg_color': fg_color}, 'Figures': []}

    if n < 1:
        return d

    if type == 'point':
        d = gen_points(d, n, width, height)
    elif type == 'triangle':
        d = gen_triangles(d, n, width, height)
    elif type == 'square':
        d = gen_squares(d, n, width, height)
    elif type == 'circle':
        d = gen_circles(d, n, width, height)
        pass

    return d


def setup_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', help='generated image description')
    parser.add_argument('width', type=int, help='canvas width, in pixels')
    parser.add_argument('height', type=int, help='canvas height, in pixels')
    parser.add_argument('bg_color', help='background color')
    parser.add_argument('fg_color', help='foreground color')
    parser.add_argument('type', choices=['point', 'triangle', 'square', 'circle'], help='figure type')
    parser.add_argument('n', type=int, help='figures per canvas width / points per canvas')
    return parser


if __name__ == '__main__':
    parser = setup_parser()
    args = parser.parse_args()
    if args.output:
        with open(args.output, 'w+') as file:
            d = gen(args.width, args.height, args.bg_color, args.fg_color, args.type, args.n)
            file.write(json.dumps(d))
