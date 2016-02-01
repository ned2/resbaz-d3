#!/usr/bin/env python3

import sys
import math
import argparse

# maybe change this to use actual ratios

phi = (1 + 5 ** 0.5) / 2
angle = 360 - 360/phi


def argparser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--width", type=int, default=1100)
    argparser.add_argument("--height", type=int, default=950)
    argparser.add_argument("--iterations", type=int, default=1000)
    argparser.add_argument("--angle", type=float, default=angle)
    argparser.add_argument("--distance", type=float, default=8.0)
    argparser.add_argument("--size", type=float, default=5.0)
    argparser.add_argument("--debug", action='store_true')
    argparser.add_argument("--func", default="default")
    argparser.add_argument("--title", default="ResBaz D3 SVG Challenge")
    argparser.add_argument("--justsvg", action="store_true")
    return argparser

         
class Tag(object):

    def __init__(self, name, *children, **kwargs):
        self.name = name
        self.children = children
        self._initial_attrs = kwargs
        self.attrs = kwargs.copy()

    def get_tag(self):
        attrs_str = ' '.join('{}="{}"'.format(attr, val)
                        for attr, val in self.attrs.items())

        if len(self.children) == 0:
            tag_str = "<{} {}/>".format(self.name, attrs_str)
        else:
            children_str = "\n".join(str(tag) for tag in self.children)

            tag_str = "<{} {}>{}</{}>".format(self.name, children_str, attrs_str,
                                              self.name)

        return tag_str.replace('clss=', 'class=')
        
    def reset(self):
        self.attrs = self._initial_attrs.copy()
    
    def __str__(self):
        return self.get_tag()

    def __repr__(self):
        return self.get_tag()


class Circle(Tag):
    def __init__(self, cx, cy, r, **kwargs):
        super().__init__('circle', cx=cx, cy=cy, r=r, **kwargs)

    def move_left(self, val):
        self.attrs['cx'] = self.attrs['cx'] - val

    def move_right(self, val):
        self.attrs['cx'] = self.attrs['cx'] + val

    def move_up(self, val):
        self.attrs['cy'] = self.attrs['cy'] - val

    def move_down(self, val):
        self.attrs['cy'] = self.attrs['cy'] + val

    def move_angle(self, angle, dist):
        rads = math.radians(angle)
        self.attrs['cx'] = self.attrs['cx'] + math.cos(rads) * dist
        self.attrs['cy'] = self.attrs['cy'] + math.sin(rads) * dist

        
class Rect(Tag):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__('rect', x=x, y=y, width=width, height=height, **kwargs)

    def move_left(self, val):
        self.attrs['x'] = self.attrs['x'] - val

    def move_right(self, val):
        self.attrs['x'] = self.attrs['x'] + val

    def move_up(self, val):
        self.attrs['y'] = self.attrs['y'] - val

    def move_down(self, val):
        self.attrs['y'] = self.attrs['y'] + val

    def move_angle(self, angle, dist):
        rads = math.radians(angle)
        self.attrs['x'] = self.attrs['x'] + math.cos(rads) * dist
        self.attrs['y'] = self.attrs['y'] + math.sin(rads) * dist

        
class Ellipse(Tag):
    def __init__(self, cx, cy, rx, ry, **kwargs):
        super().__init__('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, **kwargs)

    def move_left(self, val):
        self.attrs['cx'] = self.attrs['cx'] - val

    def move_right(self, val):
        self.attrs['cx'] = self.attrs['cx'] + val

    def move_up(self, val):
        self.attrs['cy'] = self.attrs['cy'] - val

    def move_down(self, val):
        self.attrs['cy'] = self.attrs['cy'] + val

        
class Line(Tag):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super().__init__('line', x1=x1, y1=y1, x2=x2, y2=y2)

    def move_left(self, val):
        self.attrs['x1'] = self.attrs['x1'] - val
        self.attrs['x2'] = self.attrs['x2'] - val
        
    def move_right(self, val):
        self.attrs['x1'] = self.attrs['x1'] + val
        self.attrs['x2'] = self.attrs['x2'] + val

    def move_up(self, val):
        self.attrs['y1'] = self.attrs['y1'] - val
        self.attrs['y2'] = self.attrs['y2'] - val
        
    def move_down(self, val):
        self.attrs['y1'] = self.attrs['y1'] + val
        self.attrs['y2'] = self.attrs['y2'] + val        

        
class Polygon(Tag):
    def __init__(self, *args, **kwargs): 
        super().__init__('polygon')
        # convert args into tuples of args
        # ie [x1, y1, x2, y2] -> [(x1, y1), (x2, y2)]
        self._initial_points = list(zip(*[args[i::2] for i in range(2)]))
        self.points = self._initial_points.copy()
        self.update_points()

    def update_points(self):
        points_str = " ".join("{},{}".format(x,y) for x,y in self.points)
        self.attrs['points'] = points_str
        
    # overide the reset method as we have to reset the points also
    def reset(self):
        self.attrs = self._initial_attrs.copy()
        self.points = self._initial_points.copy()
        self.update_points()
        
    def move_left(self, val):
        self.points = [(x - 1, y) for x,y in self.points]
        self.update_points()
        
    def move_right(self, val):
        self.points = [(x + 1, y) for x,y in self.points]
        self.update_points()

    def move_up(self, val):
        self.points = [(x, y - 1) for x,y in self.points]
        self.update_points()
        
    def move_down(self, val):
        self.points = [(x, y + 1) for x,y in self.points]
        self.update_points()

    def move_angle(self, angle, dist):
        rads = math.radians(angle)
        self.points = [(x+math.cos(rads)*dist, y + math.sin(rads)*dist) for x,y in self.points]
        self.update_points()


def fibonacci_gen(shape, iterations):
    dist = DISTANCE
    angle = ANGLE

    for i in range(iterations):
        yield str(shape)
        shape.reset()
        dist = DISTANCE*(i+1)
        shape.move_angle(angle, dist)
        angle += ANGLE

    
def fibonacci():
    xcenter = WIDTH/2.0
    ycenter = HEIGHT/2.0

    # triangle!
    shape = Polygon(xcenter, ycenter,
                    xcenter-0.5*SIZE, ycenter+SIZE,
                    xcenter+0.5*SIZE, ycenter+SIZE)
    
    #shape = Rect(xcenter, ycenter, SIZE, SIZE)
    #shape = Circle(xcenter, ycenter, SIZE)
    return "".join(t for t in fibonacci_gen(shape, ITERATIONS))


def do_svg(svg_body, width, height):
    svg = """<svg version="1.1"
                  baseProfile="full"
                  width="{width}" height="{height}"
                  xmlns="http://www.w3.org/2000/svg">
    {svg_body}
    </svg>""".format(svg_body=svg_body, width=width, height=height)
    return svg


def do_html(title, svg):
    html = """<!DOCTYPE html>
<html>
  <head>
    <title>{}</title>
    <link rel="stylesheet" type="text/css" href="svg.css">
  </head>
  <body>
    {}
  </body>
</html>""".format(title, svg)
    return html


def main(argv=None):
    global ITERATIONS
    global DISTANCE
    global ANGLE
    global HEIGHT
    global SIZE
    global WIDTH
    
    if argv is None:
        arg = argparser().parse_args()
    else:
        arg = argparser().parse_args(args=argv)

    HEIGHT = arg.height
    WIDTH = arg.width
    SIZE = arg.size
    DISTANCE = arg.distance
    ANGLE = arg.angle
    ITERATIONS = arg.iterations
    
    svg_body = fibonacci()
    svg = do_svg(svg_body, arg.width, arg.height)
    if arg.justsvg:
        print(svg)
    else:
        html = do_html(arg.title, svg)
        print(html)

    
if __name__ == "__main__":
    sys.exit(main())
