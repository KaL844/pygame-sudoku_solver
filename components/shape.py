from typing import TypedDict

import pygame
from components.component import Component

class LineConf(TypedDict):
    startX: int
    startY: int
    z: int
    endX: int
    endY: int
    width: int
    color: tuple[int, int, int]
    isVisible: bool

class Line(Component):
    DEFAULT_START_X = 0
    DEFAULT_START_Y = 0
    DEFAULT_Z = 0
    DEFAULT_END_X = 0
    DEFAULT_END_Y = 0
    DEFAULT_WIDTH = 0
    DEFAULT_COLOR = (255, 255, 255)
    DEFAULT_VISIBLE = True

    def __init__(self, conf: LineConf) -> None:
        super().__init__(conf['startX'] if 'startX' in conf else Line.DEFAULT_START_X, 
            conf['startY'] if 'startY' in conf else Line.DEFAULT_START_Y, 
            conf['z'] if 'z' in conf else Line.DEFAULT_Z,
            conf['isVisible'] if 'isVisible' in conf else Line.DEFAULT_VISIBLE)

        self.width = conf['width'] if 'width' in conf else Line.DEFAULT_WIDTH
        self.color = conf['color'] if 'color' in conf else Line.DEFAULT_COLOR
        self.endX = conf['endX'] if 'endX' in conf else Line.DEFAULT_END_X
        self.endY = conf['endY'] if 'endY' in conf else Line.DEFAULT_END_Y

    def draw(self, screen: pygame.surface.Surface) -> None:
        if not self.isVisible: return
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.endX, self.endY), self.width)

class RectangleConf(TypedDict):
    x: int; y: int; z: int
    width: int; height: int
    color: tuple[int, int, int]
    borderWidth: int
    isVisible: bool

class Rectangle(Component):
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_Z = 0
    DEFAULT_WIDTH = 0
    DEFAULT_HEIGHT = 0
    DEFAULT_COLOR = (255, 255, 255)
    DEFAULT_BORDER_WIDTH = 0
    DEFAULT_VISIBLE = True

    def __init__(self, conf: RectangleConf) -> None:
        super().__init__(conf['x'] if 'x' in conf else Rectangle.DEFAULT_X, conf['y'] if 'y' in conf else Rectangle.DEFAULT_Y, 
            conf['z'] if 'z' in conf else Rectangle.DEFAULT_Z, conf['isVisible'] if 'isVisible' in conf else Rectangle.DEFAULT_VISIBLE)

        self.width = conf['width'] if 'width' in conf else Rectangle.DEFAULT_WIDTH
        self.height = conf['height'] if 'height' in conf else Rectangle.DEFAULT_HEIGHT
        self.color = conf['color'] if 'color' in conf else Rectangle.DEFAULT_COLOR
        self.borderWidth = conf['borderWidth'] if 'borderWidth' in conf else Rectangle.DEFAULT_BORDER_WIDTH

        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: pygame.surface.Surface) -> None:
        if not self.isVisible: return

        pygame.draw.rect(screen, self.color, self.rect, self.borderWidth)
