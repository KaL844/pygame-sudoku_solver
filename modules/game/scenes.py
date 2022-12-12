import pygame
from components.label import Label
from components.scene import Scene, SceneManager
from components.panel import Panel
from components.shape import Line, Rectangle
from components.button import Button
from modules.game.logic import GameLogic
from utils.enum_types import MouseEvent, MouseEventContext
from utils.json_reader import JsonReader
import utils.constants as constants


class GameScene(Scene):
    CONFIG_FILE = 'conf/game/GameScene.json'

    VALID_KEYS = {pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_BACKSPACE}
    INPUT_COLOR = (255, 255, 0)

    def __init__(self) -> None:
        self.conf = JsonReader.load(GameScene.CONFIG_FILE)

        self.sceneMgr = SceneManager.getInstance()
        self.logic = GameLogic()
        self.boardPanel = Panel(conf=self.conf['boardPanel'])
        self.solveBtn = Button(conf=self.conf['solveBtn'])

        self.width, self.height = self.boardPanel.getSize()
        self.cellWidth, self.cellHeight = self.width // GameLogic.COLS, self.height // GameLogic.ROWS

        self.currRow = -1
        self.currCol = -1

        self.init()

    def init(self) -> None:
        self.addCells()
        self.addLines()
        self.boardPanel.addEventListener(MouseEvent.ON_TOUCH_END, self.onBoardClick)
        self.solveBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onSolveClick)

    def addLines(self) -> None:
        for i in range(GameLogic.COLS + 1):
            offset = 0 if i == 0 else -2
            width = 4 if i % 3 == 0 else 1
            self.boardPanel.addChild(f"verticalLine{i}", Line({'startX': i * self.cellWidth + offset, 'endX': i * self.cellWidth + offset, 
                'startY': 0, 'endY': self.height, "width": width}))
        for i in range(GameLogic.ROWS + 1):
            offset = 0 if i == 0 else -2
            width = 4 if i % 3 == 0 else 1
            self.boardPanel.addChild(f"horizontalLine{i}", Line({'startX': 0, 'endX': self.width, 'startY': i * self.cellHeight + offset, 
                'endY': i * self.cellHeight + offset, "width": width}))

    def addCells(self) -> None:
        for i in range(GameLogic.ROWS):
            for j in range(GameLogic.COLS):
                self.boardPanel.addChild(f"rect_{i}_{j}", Rectangle({'x': j * self.cellWidth, 'y': i * self.cellHeight, 
                    'color': (50, 50, 50), 'width': self.cellWidth, 'height': self.cellHeight, 'isVisible': False}))
                self.boardPanel.addChild(f"label_{i}_{j}", Label({'x': (j + 0.5) * self.cellWidth, 'y': (i + 0.5) * self.cellHeight, 
                    'anchor': 'MID_CENTER'}))

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)
        
        self.boardPanel.draw(screen)
        self.solveBtn.draw(screen)

    def input(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN: return

        if event.key not in GameScene.VALID_KEYS: return

        if self.currCol == -1 or self.currRow == -1: return

        cell: Label = self.boardPanel.getChild(f'label_{self.currRow}_{self.currCol}')
        rect: Rectangle = self.boardPanel.getChild(f'rect_{self.currRow}_{self.currCol}')

        if event.key == pygame.K_BACKSPACE:
            cell.setText('')
            cell.setColor(Label.DEFAULT_COLOR)
            self.logic.setCell(GameLogic.EMPTY_VALUE, self.currRow, self.currRow)
            return

        cell.setText(event.unicode)
        cell.setColor(GameScene.INPUT_COLOR)
        self.logic.setCell(event.unicode, self.currRow, self.currCol)

    def onBoardClick(self, context: MouseEventContext) -> None:
        x, y = context['x'], context['y']
        localX, localY = self.boardPanel.getLocalPosition(x, y)
        row, col = localY // self.cellHeight, localX // self.cellWidth
        
        if self.currCol != -1 and self.currRow != -1:
            self.boardPanel.getChild(f"rect_{self.currRow}_{self.currCol}").setVisible(False)

        if self.currCol == col and self.currRow == row:
            self.currCol = -1
            self.currRow = -1
            return
        self.boardPanel.getChild(f"rect_{row}_{col}").setVisible(True)
        self.currCol = col
        self.currRow = row

    def onSolveClick(self, _: MouseEventContext) -> None:
        self.logic.startSolve()

        for i in range(GameLogic.ROWS):
            for j in range(GameLogic.COLS):
                cell: Label = self.boardPanel.getChild(f'label_{i}_{j}')
                cell.setText(str(self.logic.getCell(i, j)))