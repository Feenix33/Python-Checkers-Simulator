"""
BoardB.py
checkers simulator

B uses grid to represent the board with a piece dictionary
piece database:
    sym name        side    vel
    v   valid       --      --
    i   invalid     --      --
    r   red normal  r       1
    R   red king    r       1, -1
    b   black norm  b       -1
    B   black king  b       1, -1

velocity is vertical, horizontal is always 1, -1
"""
     
import pygame
     
# Define some colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
BROWN = (170, 85, 0)
GREY = (170, 170, 170)
DKGREY = (85, 85, 85)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
     
# global constants
DIM = 8  # spaces in a row/col
GRID = 60  # for drawing

PieceDict = {
    'v' : {'name': 'valid', 'sym': '#'},
    'i' : {'name': 'invalid', 'sym': '.'},
    'r' : {'name': 'Red Norm', 'sym': 'r', 'side': 'r', 'vel':[1]},
    'R' : {'name': 'Red King', 'sym': 'R', 'side': 'r', 'vel':[1, -1]},
    'b' : {'name': 'Blk Norm', 'sym': 'b', 'side': 'b', 'vel':[-1]},
    'B' : {'name': 'Blk King', 'sym': 'B', 'side': 'b', 'vel':[1, -1]}
    }

class Board:
    def __init__(self, dim):
        self.dim = dim
        self.board = []
        for j in range(self.dim):
            row = []
            for k in range(self.dim):
                space = 'v' if (j+k)%2==0 else 'i'
                row.append(space)
            self.board.append(row)
        self.reset()
        #self.resetFoxR()

    def reset(self):
        self.select = []
        self.turn = 'r'
        self.preventDeselect = False
        for y in range(3):
            for x in range(DIM):
                if (x+y)%2 == 0:
                    self.board[y][x] = 'r'
        for y in range(DIM-3, DIM):
            for x in range(DIM):
                if (x+y)%2 == 0:
                    self.board[y][x] = 'b'

    def resetFoxR(self):
        self.select = []
        self.turn = 'r'
        for x in range(DIM):
            if (x)%2 == 0:
                self.board[0][x] = 'r'
        for x in range(2):
            if (x+DIM-1)%2 == 0:
                self.board[DIM-1][x] = 'B'

    def processMouse(self, mx, my):
        """ mouse is in grid coordinates """
        #nothing is selected, find a piece to select
        if len(self.select) == 0:
            if self.board[my][mx].lower() == self.turn:
                self.select = [mx, my]

        #There is a selected piece, deselect?
        elif mx == self.select[0] and my == self.select[1] and \
                not self.preventDeselect:
            self.select = []

        else:
            if self.attemptingCapture(mx, my):
                if self.tryCapture(mx, my):
                    self.tryMakeKing()
                    if not self.canSelectCapture():
                        self.switchTurn()
            elif self.attemptingMove(mx, my) and \
                not self.preventDeselect: #have to do a capture
                if self.tryMove(mx, my):
                    self.tryMakeKing()
                    self.switchTurn()

    def canSelectCapture(self):
        sx = self.select[0]
        sy = self.select[1]
        yOffs = PieceDict[self.board[sy][sx]]['vel']
        xOffs = [-2, 2]
        for y in yOffs:
            for x in xOffs:
                if self.validCapture(sx+x, sy+2*y):
                    return True
        return False


    def attemptingCapture(self, mx, my):
        if mx >= 0 and mx < self.dim and my >= 0 and my < self.dim \
                and abs(mx - self.select[0]) == 2 \
                and abs(my - self.select[1]) == 2 \
                and self.board[my][mx] == 'v':
            return True
        return False

    def tryCapture(self, mx, my):
        if self.validCapture(mx, my):
            self.executeCapture(mx, my)
            return True
        return False

    def validCapture(self, mx, my):
        if mx < 0 or mx >= self.dim or my < 0 or my >= self.dim \
                or abs(mx - self.select[0]) != 2 \
                or abs(my - self.select[1]) != 2 \
                or self.board[my][mx] != 'v':
            return False
        sx = self.select[0]
        sy = self.select[1]
        vel = PieceDict[self.board[sy][sx]]['vel']
        validMove = False
        tgtOffy = 0
        for yoff in vel:
            if (sy + 2*yoff) == my:
                tgtOffy = yoff
        if tgtOffy == 0: return False
        tgtOffx = 1 if mx > sx else -1

        tgtSide = self.board[sy+tgtOffy][sx+tgtOffx].lower()
        if (tgtSide == 'r' and self.board[sy][sx].lower() == 'b') \
                or (tgtSide == 'b' and self.board[sy][sx].lower() == 'r'):
            return True
        return False

    def executeCapture(self, mx, my):
        sx = self.select[0]
        sy = self.select[1]
        tgtOffx = 1 if mx > sx else -1
        tgtOffy = 1 if my > sy else -1
        self.board[my][mx] = self.board[sy][sx]
        self.board[sy][sx] = 'v'
        self.board[sy+tgtOffy][sx+tgtOffx] = 'v'
        self.select = [mx, my]
        self.preventDeselect = True

    def attemptingMove(self, mx, my):
        if mx >= 0 and mx < self.dim and my >= 0 and my < self.dim \
                and abs(mx - self.select[0]) == 1 \
                and abs(my - self.select[1]) == 1 \
                and self.board[my][mx] == 'v':
            return True
        return False

    def tryMove(self, mx, my):
        if abs(mx - self.select[0]) == 1 \
                and abs(my - self.select[1]) == 1 \
                and self.board[my][mx] == 'v':
            sx = self.select[0]
            sy = self.select[1]
            vel = PieceDict[self.board[sy][sx]]['vel']
            validMove = False
            for yoff in vel:
                if (sy + yoff) == my:
                    validMove = True
            if validMove:
                self.board[my][mx] = self.board[self.select[1]][self.select[0]]
                self.board[self.select[1]][self.select[0]] = 'v'
                self.select = [mx, my]
                return True
        return False

    def tryMakeKing(self):
        sx = self.select[0]
        sy = self.select[1]
        pt = self.board[sy][sx]
        if pt == 'r' or pt == 'b':
            ky = 0 if pt.lower() == 'b' else DIM-1
            if sy == ky:
                self.board[sy][sx] = self.board[sy][sx].upper()

    def switchTurn(self):
        self.select = []
        self.turn = 'r' if self.turn == 'b' else 'b'
        self.preventDeselect = False

    def __repr__(self):
        rtnStr = ""
        for j in range(self.dim):
            for k in range(self.dim):
                rtnStr += PieceDict[self.board[j][k]]['sym']
            rtnStr += '\n'
        return rtnStr

    def draw(self, scrn):
        sy = 0
        half = GRID//2
        rad = (half*8)//10
        rad2 = half//2
        rad3 = half//4
        for y in range(self.dim):
            sx = 0
            for x in range(self.dim):
                if self.board[y][x] == 'v':
                    pygame.draw.rect(scrn, GREY, [sx, sy, GRID, GRID])
                elif self.board[y][x] == 'i':
                    pygame.draw.rect(scrn, WHITE, [sx, sy, GRID, GRID])
                elif self.board[y][x] == 'r':
                    pygame.draw.rect(scrn, GREY, [sx, sy, GRID, GRID])
                    pygame.draw.circle(scrn, RED, [sx+half,sy+half], rad)
                elif self.board[y][x] == 'b':
                    pygame.draw.rect(scrn, GREY, [sx, sy, GRID, GRID])
                    pygame.draw.circle(scrn, BLACK, [sx+half,sy+half], rad)
                elif self.board[y][x] == 'R':
                    pygame.draw.rect(scrn, GREY, [sx, sy, GRID, GRID])
                    pygame.draw.circle(scrn, RED, [sx+half,sy+half], rad)
                    pygame.draw.circle(scrn, GREY, [sx+half,sy+half], rad2)
                    pygame.draw.circle(scrn, RED, [sx+half,sy+half], rad3)
                elif self.board[y][x] == 'B':
                    pygame.draw.rect(scrn, GREY, [sx, sy, GRID, GRID])
                    pygame.draw.circle(scrn, BLACK, [sx+half,sy+half], rad)
                    pygame.draw.circle(scrn, GREY, [sx+half,sy+half], rad2)
                    pygame.draw.circle(scrn, BLACK, [sx+half,sy+half], rad3)
                else:
                    pygame.draw.rect(scrn, YELLOW, [sx, sy, GRID, GRID])
                sx += GRID
            sy += GRID
        if len(self.select) > 0:
            sx = self.select[0]*GRID
            sy = self.select[1]*GRID
            pygame.draw.rect(scrn, YELLOW, [sx, sy, GRID, GRID], 5)


def main():
    pygame.init()
     
    # Set the width and height of the screen [width, height]
    size = (DIM*GRID, DIM*GRID)
    screen = pygame.display.set_mode(size)
    width, height = screen.get_size()
     
    pygame.display.set_caption("My Game")
     
    # -------- Global Initializations -------- 

    # -------- Local Initializations -------- 
    done = False # Loop until the user clicks the close button.
    clock = pygame.time.Clock() # Used to manage how fast the screen updates
    board = Board(DIM)
     
     
    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                mx = mpos[0]
                board.processMouse(mpos[0]//GRID, mpos[1]//GRID)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_SPACE:
                    print (board)
                else:
                    print ("Unknown key " + str(event.key))
     
        # --- Game logic should go here
     
        # --- Screen-clearing code goes here
        screen.fill(WHITE)
     
        # --- Drawing code should go here
        board.draw(screen)
     
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)
     
    # Close the window and quit.
    pygame.quit()

if __name__ == '__main__':
    main()
