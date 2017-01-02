"""
Simple move pieces on a board
Use sprites to represent everything
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

GRID = 50
DIM = 10

gFont25 = object

class Board:
    def __init__(self, xDim, yDim):
        self.boardSprites = pygame.sprite.Group()
        self.tiles = []
        yPos = 0
        for y in range(yDim):
            tileRow = []
            idType = ((y + 1) % 2) + 2
            xPos = 0
            for x in range(xDim):
                tile = Tile(xPos, yPos, GRID, GRID, idType)
                self.boardSprites.add(tile)
                xPos += GRID
                idType = ((idType + 1) % 2) + 2
                tileRow.append(idType)
            yPos += GRID
            self.tiles.append(tileRow)
    
    def draw(self, screen):
        self.boardSprites.draw(screen)

    def debugPrint(self):
        for row in self.tiles:
            for cell in row:
                print (cell, end=" ")
            print ("")

class Piece(pygame.sprite.Sprite):
    def __init__(self, xt, yt, clr, name):
        super().__init__() # Call the parent's constructor
        self.image = pygame.Surface([GRID, GRID])
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        self.clr = clr
        self.name = name
        self.selected = False

        self.drawSprite()

        self.rect.x = xt * GRID
        self.rect.y = yt * GRID
    
    def drawSprite(self):
        # instead of the blit of an image
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, self.clr, [GRID//2,GRID//2], GRID//2-2)
        text = gFont25.render(self.name, True, BLACK)
        self.image.blit(text, [GRID//3, GRID//3])

    def select(self):
        self.selected = not self.selected
        self.drawSprite()

        if self.selected:
            pygame.draw.line(self.image, RED, [0, 0], [GRID, GRID], 3)
        #print ("Selected " + self.name + " as " + str(self.selected))

    def moveTo(self, gridX, gridY):
        self.rect.x = gridX * GRID
        self.rect.y = gridY * GRID

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, idType):
        # Call the parent's constructor
        super().__init__()
 
        self.idType = idType
        colors = [RED, BLUE, BLACK, GREEN, YELLOW, GREY]
        if idType >= 0 and idType < len(colors):
            color = colors[idType]
        else:
            color = WHITE

        # Make a wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

def main():
    global gFont25
    pygame.init()
    pygame.font.init()

     
    # Set the width and height of the screen [width, height]
    size = (GRID*DIM, GRID*DIM)
    screen = pygame.display.set_mode(size)
    width, height = screen.get_size()
     
    pygame.display.set_caption("My Game")
     
    # Loop until the user clicks the close button.
    done = False
    gFont25 = pygame.font.SysFont(pygame.font.get_default_font(), 25)
    board = Board(DIM, DIM)

    aTile = Tile(GRID*DIM/2+GRID/2, GRID*DIM/2+GRID/2, GRID, GRID, 4) #idType)

    movingSprites = pygame.sprite.Group()
    movingSprites.add( aTile )

    aPiece = Piece(3, 2, BLUE, "x1")
    pieceSprites = pygame.sprite.Group()
    pieceSprites.add( aPiece )
    aPiece = Piece(5, 3, BLUE, "x2")
    pieceSprites.add( aPiece )
     
    #board.debugPrint()
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
     
    onSprite = None

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                if onSprite is None:
                    for sprite in pieceSprites:
                        if sprite.rect.collidepoint(mpos[0], mpos[1]):
                            onSprite = sprite
                            onSprite.select()
                else:
                    #a sprite is selected, check not on another piece
                    otherSprite = None
                    for sprite in pieceSprites:
                        if sprite.rect.collidepoint(mpos[0], mpos[1]):
                            otherSprite = sprite
                    if otherSprite is None:
                        onSprite.moveTo(mpos[0] // GRID, mpos[1]//GRID)
                        onSprite.select()
                        onSprite = None
                    elif otherSprite == onSprite:
                        onSprite.select()
                        onSprite = None
            #elif event.type == pygame.MOUSEBUTTONUP:
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                else:
                    print ("Unknown key " + str(event.key))
     
        # --- Game logic should go here
        #movingSprites.update(trackSprites)
     
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
     
        # --- Drawing code should go here
        board.draw(screen)
        #board.boardSprites.draw(screen)
        #movingSprites.draw(screen)
        pieceSprites.draw(screen)

     
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)
     
    # Close the window and quit.
    pygame.quit()

if __name__ == '__main__':
    main()
