"""
BoardA.py
Second experiment in a board
Board is a grid, not an bunch of sprites
Board is square for simplification

does a capture
does a normal move
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

DIM = 8
GRID = 60

gBoard = None

class Board:
    def __init__(self, dim):
        self.board = [] # the type of board grid
        # ^^^^^ don't think we need this var
        self.dim = dim
        for y in range(dim):
            row = []
            for x in range(dim):
                row.append((y + x)%2)
            self.board.append(row)
        self.clearBoard()
        #self.pieces = []
        #self.pieceSelect = None
        self.turnType = 'T'
        self.capturePossible = False

    def clearBoard(self):
        self.pieces = []
        self.pieceSelect = None
        self.capturePossible = False
        Piece.reset()

    def RealsetupBoard(self):
        self.clearBoard()
        for y in range(3):
            for x in range(DIM):
                if (x+y)%2 == 1:
                    self.addPiece( Piece('T', y, x) )
        for y in range(DIM-3, DIM):
            for x in range(DIM):
                if (x+y)%2 == 1:
                    self.addPiece( Piece('B', y, x) )

    def setupBoard(self):
        self.clearBoard()
        y = 2
        for x in range(DIM):
            if (x+y)%2 == 1:
                self.addPiece( Piece('T', y, x) )
        y = DIM-3
        for x in range(DIM):
            if (x+y)%2 == 1:
                self.addPiece( Piece('B', y, x) )

    def addPiece(self, piece):
        self.pieces.append(piece)

    def removePieceByNdex(self, ndex):
        """ don't need yet """
        print ("Remove by index")

    def removePiece(self, piece):
        self.pieces.remove(piece)

    def log(self):
        for piece in self.pieces:
            piece.log()

    def draw(self, scrn):
        sy = 0
        for y in range(self.dim):
            sx = 0
            for x in range(self.dim):
                if self.board[y][x] == 0:
                    pygame.draw.rect(scrn, RED, [sx, sy, GRID, GRID])
                elif self.board[y][x] == 1:
                    pygame.draw.rect(scrn, BLACK, [sx, sy, GRID, GRID])
                else:
                    pygame.draw.rect(scrn, BLUE, [sx, sy, GRID, GRID])
                sx += GRID
            sy += GRID
        for piece in self.pieces:
            piece.draw(scrn)

    def processMouse(self, mx, my):
        mgx = mx//GRID
        mgy = my//GRID
        if self.pieceSelect is None:
            self.capturePossible = False
            for piece in self.pieces:
                if self.turnType == piece.ptype and \
                        mgx == piece.gx and mgy == piece.gy:
                    piece.select = True
                    self.pieceSelect = piece
                    if self.canCapture():
                        print ("capture possible")
                        self.capturePossible = True
        else:
            self.tryMove(mgx, mgy)
      
    def tryMove(self, mgx, mgy):
        """
        check if can capture
            if yes, is this piece doing a capture
                take the capture
                move the piece
                eval new situation
            no, reject move
        if no capture, then try a regular move
            if valid then move
                else reject

        TODO:
        revisit  the hit self and .capture var
        """
        if self.capturePossible:
            if self.executeCapture(mgx, mgy):
                self.pieceSelect.moveTo(mgx, mgy)
                self.pieceSelect.select = False
                self.pieceSelect = None
                self.capturePossible = False
                self.turnType = 'B' if self.turnType == 'T' else 'T'
            else:
                print ("Failed capture attempt")
        elif self.tryDeselect(mgx, mgy):
            self.pieceSelect.select = False
            self.pieceSelect = None
            self.capturePossible = False
            return
        elif self.moveValid(mgx, mgy):
            self.pieceSelect.moveTo(mgx, mgy)
            self.pieceSelect.select = False
            self.pieceSelect = None
            self.capturePossible = False
            self.turnType = 'B' if self.turnType == 'T' else 'T'

    def tryDeselect(self, mgx, mgy):
        if (mgx - self.pieceSelect.gx) == 0 and \
                (mgy - self.pieceSelect.gy) == 0:
            return True
        return False

    def moveValid(self, mgx, mgy):
        """ mgx/y = target coords 
            checks the pieceSelect
            only checks if it is a single move
            returns true or false
        """
        # valid board space?
        if (mgx + mgy) % 2 != 1: return False

        # only one space away
        if abs(mgx - self.pieceSelect.gx) != 1 or \
                abs(mgy - self.pieceSelect.gy) != 1:
            return False

        # vertical the correct direction
        vDist = 1 if self.pieceSelect.ptype == 'T' else -1
        if mgy - self.pieceSelect.gy != vDist:
            return False

        # hitting another piece?
        illegal = False
        for piece in self.pieces:
            if piece != self.pieceSelect: #don't check self
                if piece.gx == mgx and piece.gy == mgy:
                    illegal = True
                    return False
        return True

    def executeCapture(self, mgx, mgy):
        """ to to execute a capture move, true if success """
        # new place two spaces away
        if abs(mgx - self.pieceSelect.gx) != 2 or \
                abs(mgy - self.pieceSelect.gy) != 2:
            #print ("eC: failing test 1")
            return False

        # in the right direction
        if self.pieceSelect.ptype == 'T' and mgy < self.pieceSelect.gy:
            #print ("eC: failing test 2")
            return False
        if self.pieceSelect.ptype == 'B' and mgy > self.pieceSelect.gy:
            #print ("eC: failing test 3")
            return False

        # capture target in between?
        cx = mgx-1 if mgx > self.pieceSelect.gx else mgx+1
        cy = mgy-1 if mgy > self.pieceSelect.gy else mgy+1
        #print ("ec target test")
        #print ("  select ", self.pieceSelect.info())
        #print ("  cy cx  ", cy, cx)
        #print ("  my mx  ", mgy, mgx)
        capturePiece = self.getPiece (cx, cy)
        if capturePiece is not None and \
            capturePiece.ptype != self.pieceSelect.ptype:

            # do the capture
            #print ("Removing piece ", capturePiece.info())
            self.removePiece(capturePiece)
            return True

        # no capture
        #print ("eC: failing test final")
        return False


    def canCapture(self):
        dbgIn = "cc    "
        """ can the selected piece capture another piece """
        # two possible moves
        # check if target is clear
        # if clear, is there an target in between?
        #print (dbgIn)
        #print (dbgIn, "Test capture for", self.pieceSelect.info())
        xyOffsets = [[2, 2, 1, 1], [-2, 2, -1, 1]] 
        pDir = 1 if self.pieceSelect.ptype == 'T' else -1
        for offset in xyOffsets:
            gxoff = offset[0]
            gyoff = offset[1] * pDir
            txoff = offset[2] # for the target
            tyoff = offset[3] * pDir
            newx = self.pieceSelect.gx + gxoff
            newy = self.pieceSelect.gy + gyoff
            if self.isEmpty(newx, newy): #possible empty space
                #print (dbgIn, "open spot 2 squares away yx", newy, newx)
                tx = self.pieceSelect.gx + txoff
                ty = self.pieceSelect.gy + tyoff
                capturePiece = self.getPiece(tx, ty)
                if capturePiece is not None and \
                        capturePiece.ptype != self.pieceSelect.ptype:
                    #print (dbgIn, "can grab piece ", capturePiece.info())
                    return True
                #else:
                #    print (dbgIn, "no good at yx ", ty, tx)
        return False

    def isEmpty(self, gx, gy):
        """ return true if the x,y spot is empty else false """
        if gx < 0 or gx >= DIM or gy < 0 or gy >= DIM:
            return False
        for piece in self.pieces:
            if piece.gx == gx and piece.gy == gy:
                return False
        return True

    def getPiece(self, gx, gy):
        """ returns the piece at gx gy or None """
        for piece in self.pieces:
            if piece.gx == gx and piece.gy == gy:
                return piece
        return None

class Piece:
    ndex = 0
    def __init__(self, ptype, gy, gx):
        """ ptype is type of piece, dim is grid dimension """
        self.ptype = ptype
        self.id = Piece.ndex
        self.rad = (GRID * 4)//10
        self.half = GRID//2
        self.cx = gx * GRID + GRID//2
        self.cy = gy * GRID + GRID//2
        self.gx = gx
        self.gy = gy
        Piece.ndex += 1
        self.select = False
        self.capture = False # this piece just did a capture

    def reset():
        Piece.ndex = 0

    def log(self):
        print ("Piece #", self.id, " t=", self.ptype, " at (",self.gy, self.gx,")")

    def info(self):
        return str(self.ptype) + "[" + str(self.id) + "]@(" + str(self.gy)+ ", " + str(self.gx)+ ")"

    def draw(self, scrn):
        """ x,y upper right corner, w is grid dimension """
        if self.ptype == 'T':
            clr = YELLOW
        else:
            clr = GREY
        #pygame.draw.circle(scrn, clr, [self.x+self.half,self.y+self.half], self.rad)
        pygame.draw.circle(scrn, clr, [self.cx,self.cy], self.rad)
        if self.select:
            pygame.draw.circle(scrn, RED, [self.cx,self.cy], self.rad, 4)
            pygame.draw.circle(scrn, BLACK, [self.cx,self.cy], self.rad, 1)

    def moveTo(self, gx, gy):
        self.gx = gx
        self.gy = gy
        self.cx = gx * GRID + GRID//2
        self.cy = gy * GRID + GRID//2


def main():
    pygame.init()
     
    # Set the width and height of the screen [width, height]
    size = (DIM*GRID, DIM*GRID)
    screen = pygame.display.set_mode(size)
    width, height = screen.get_size()
     
    pygame.display.set_caption("My Game")
     
    # -------- Global Initializations -------- 
    global gBoard
    gBoard = Board(DIM)
    #gBoard.addPiece( Piece('T', 1, 2) )
    #gBoard.addPiece( Piece('B', DIM-2, DIM-1) )
    gBoard.setupBoard()

    # -------- Local Initializations -------- 
    done = False
    clock = pygame.time.Clock() # Used to manage how fast the screen updates
     

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                gBoard.processMouse(mpos[0], mpos[1])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_SPACE:
                    gBoard.log()
                elif event.key == pygame.K_r:
                    print ("Resetting board....")
                    gBoard.setupBoard()
                else:
                    print ("Unknown key " + str(event.key))
     
        # --- Game logic should go here
     
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)
     
        # --- Drawing code should go here
        gBoard.draw(screen)
        #pieceA.draw(screen)
        #pieceB.draw(screen)
     
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)
     
    # Close the window and quit.
    pygame.quit()

if __name__ == '__main__':
    main()
