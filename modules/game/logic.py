class GameLogic:
    ROWS = 9
    COLS = 9

    DIV = 3

    EMPTY_VALUE = -1

    def __init__(self) -> None:
        self.board = [[GameLogic.EMPTY_VALUE for _ in range(GameLogic.COLS)] for _ in range(GameLogic.ROWS)]

    def setCell(self, value: str, row: int, col: int) -> None:
        self.board[row][col] = int(value)

    def isValidBoard(self) -> bool:
        checkRow = {}
        checkCol = {}
        checkBox = {}
        for i in range(GameLogic.ROWS):
            for j in range(GameLogic.COLS):
                if self.board[i][j] == GameLogic.EMPTY_VALUE: continue
                if str(i) not in checkRow:
                    checkRow[str(i)] = set()
                if str(j) not in checkCol:
                    checkCol[str(j)] = set()
                if str(self.getBox(i, j)) not in checkBox:
                    checkBox[str(self.getBox(i, j))] = set()
                rowSet: set[int] = checkRow[str(i)]   
                colSet: set[int] = checkCol[str(j)]
                boxSet: set[int] = checkBox[str(self.getBox(i, j))]
                value: int = self.board[i][j]
                if value in rowSet or value in colSet or value in boxSet: return False
                rowSet.add(value)
                colSet.add(value)
                boxSet.add(value)
        return True

    def startSolve(self) -> None:
        self.solve(0, 0)

    def solve(self, row: int, col: int) -> bool:
        if row == GameLogic.ROWS: return True
        if col == GameLogic.COLS: return self.solve(row + 1, 0)
        if self.board[row][col] != GameLogic.EMPTY_VALUE: return self.solve(row, col + 1)
        for k in range(1, 10):
            self.board[row][col] = k
            if self.isValidBoard():
                if self.solve(row, col + 1): return True
                self.board[row][col] = GameLogic.EMPTY_VALUE
                continue
            self.board[row][col] = GameLogic.EMPTY_VALUE

    def getBox(self, row: int, col: int) -> int:
        bRow, bCol = row // GameLogic.DIV, col // GameLogic.DIV
        return bRow * GameLogic.DIV + bCol

    def getCell(self, row: int, col: int) -> int:
        return self.board[row][col]

