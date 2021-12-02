import pygame
import random
pygame.init()

''' ============================================================ '''
# SERVER
import socket
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.bind((host, port))
mySocket.setblocking(0)
print("UDP server listening on port {0}.\n".format(port))
''' ============================================================ '''

bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

#game_width = 10    # Change this to increase size
#game_height = 10   # Change this to increase size
game_width = 7      # Change this to increase size
game_height = 7     # Change this to increase size
numMine = 48    # Number of mines
grid_size = 32  # Size of grid (WARNING: macke sure to change the images dimension as well)
border = 16     # Top border
top_border = 100  # Left, Right, Bottom border
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height
gameDisplay = pygame.display.set_mode((display_width, display_height))  # Create display
timer = pygame.time.Clock()  # Create timer
pygame.display.set_caption("Minesweeper")  # S Set the caption of window
address = None # holds address to return value to
resetESP32 = False

# Import files
spr_emptyGrid = pygame.image.load("Sprites/empty.png")
spr_flag = pygame.image.load("Sprites/flag.png")
spr_grid = pygame.image.load("Sprites/Grid.png")
spr_grid1 = pygame.image.load("Sprites/grid1.png")
spr_grid2 = pygame.image.load("Sprites/grid2.png")
spr_grid3 = pygame.image.load("Sprites/grid3.png")
spr_grid4 = pygame.image.load("Sprites/grid4.png")
spr_grid5 = pygame.image.load("Sprites/grid5.png")
spr_grid6 = pygame.image.load("Sprites/grid6.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_grid8 = pygame.image.load("Sprites/grid8.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_mine = pygame.image.load("Sprites/mine.png")
spr_mineClicked = pygame.image.load("Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("Sprites/mineFalse.png")


# Create global values
grid = []  # The main grid
mines = []  # Pos of the mines


# Create funtion to draw texts
def drawText(txt, s, yOff=0):
    screen_text = pygame.font.SysFont("Calibri", s, True).render(txt, True, (0, 0, 0))
    rect = screen_text.get_rect()
    rect.center = (game_width * grid_size / 2 + border, game_height * grid_size / 2 + top_border + yOff)
    gameDisplay.blit(screen_text, rect)


# Create class grid
class Grid:
    def __init__(self, xGrid, yGrid, type):
        self.xGrid = xGrid  # X pos of grid
        self.yGrid = yGrid  # Y pos of grid
        self.clicked = False  # Boolean var to check if the grid has been clicked
        self.mineClicked = False  # Bool var to check if the grid is clicked and its a mine
        self.mineFalse = False  # Bool var to check if the player flagged the wrong grid
        self.flag = False  # Bool var to check if player flagged the grid
        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(border + self.xGrid * grid_size, top_border + self.yGrid * grid_size, grid_size, grid_size)
        self.val = type  # Value of the grid, -1 is mine

    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        if self.mineFalse:
            gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(spr_grid5, self.rect)
                    elif self.val == 6:
                        gameDisplay.blit(spr_grid6, self.rect)
                    elif self.val == 7:
                        gameDisplay.blit(spr_grid7, self.rect)
                    elif self.val == 8:
                        gameDisplay.blit(spr_grid8, self.rect)

            else:
                if self.flag:
                    gameDisplay.blit(spr_flag, self.rect)
                else:
                    gameDisplay.blit(spr_grid, self.rect)

    def revealGrid(self):
        self.clicked = True
        # Auto reveal if it's a 0
        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if not grid[self.yGrid + y][self.xGrid + x].clicked:
                                grid[self.yGrid + y][self.xGrid + x].revealGrid()
        elif self.val == -1:
            # Auto reveal all mines if it's a mine
            for m in mines:
                if not grid[m[1]][m[0]].clicked:
                    grid[m[1]][m[0]].revealGrid()

    def updateValue(self):
        # Update the value when all grid is generated
        if self.val != -1:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if grid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1

''' ============================================================ '''
# added here [Fade] 
def check_input_udp_socket():
    msg = None
    addr = 0
    try:
        msg, addr = mySocket.recvfrom(1024) # receive 1024 bytes
        msg = msg.decode('utf-8')
    except BlockingIOError:
        pass # do nothing if there's no data
    return msg, addr
# additions ended here
''' ============================================================ '''

def gameLoop():
    gameState = "Playing"  # Game state
    mineLeft = numMine  # Number of mine left
    global grid  # Access global var
    grid = []
    global mines
    t = 0  # Set time to 0

    # Generating mines
    mines = [[random.randrange(0, game_width),
              random.randrange(0, game_height)]]

    for c in range(numMine - 1):
        pos = [random.randrange(0, game_width),
               random.randrange(0, game_height)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:
                    pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
                    break
                if i == len(mines) - 1:
                    same = False
        mines.append(pos)

    # Generating entire grid
    for j in range(game_height):
        line = []
        for i in range(game_width):
            if [i, j] in mines:
                line.append(Grid(i, j, -1))
            else:
                line.append(Grid(i, j, 0))
        grid.append(line) # grid is a list of Grid objects [commented: Fade]

    # Update of the grid
    for i in grid:
        for j in i:
            j.updateValue()

    # Main Loop
    while gameState != "Exit":
        # Reset screen
        gameDisplay.fill(bg_color)

        ''' ============================================================ '''
        # added here [Fade][justin]
        msg, addr = check_input_udp_socket()
        clickstat = None
        if msg is not None:
            if msg == "R" and (gameState == "Game Over" or gameState == "Win"):
                gameState = "Exit"
                gameLoop()
                break;


            try:
                address = addr
                (clickstat, x, y) = msg.split(',')
                print("You selected tile at " + str(x) + ", " + str(y))
                x_shifted = int(x) * 31 + 34  # conversion equations
                y_shifted = int(y) * 33 + 116

            except ValueError:  # if corrupted data, skip the sample
                continue


        # User inputs
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"
            # Check if player restart the game
            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN:
                    # check if there's a key physically pressed down [commented: Fade]
                    if event.key == pygame.K_r:
                        # check if that key is the key 'r' [commented: Fade]
                        gameState = "Exit"
                        gameLoop()
                        # if it is, exit this game by exiting this while loop
                        # and make a recursion call by calling gameLoop()
                        # [commented: Fade]


        if clickstat == "click":
            for i in grid:
                for j in i:
                    #coord = pygame.mouse.get_pos()
                    if j.rect.collidepoint((x_shifted,y_shifted)):
                        #print("coordinate: " + str(coord))
                        j.revealGrid()
                        # Toggle flag off
                        if j.flag:
                            mineLeft += 1
                            j.flag = False
                        # If it's a mine
                        if j.val == -1:
                            gameState = "Game Over"
                            j.mineClicked = True
        # additions ended here
        ''' ============================================================ '''

        # Check if won
        w = True
        for i in grid:
            for j in i:
                j.drawGrid()
                if j.val != -1 and not j.clicked:
                    w = False
        if w and gameState != "Exit":
            gameState = "Win"
            mySocket.sendto(("Won").encode("utf-8"),address)  # sends Score and life notification to socket

        # Draw Texts
        if gameState != "Game Over" and gameState != "Win":
            t += 1
        elif gameState == "Game Over":
            drawText("Game Over!", 50)
            mySocket.sendto(("Loss").encode("utf-8"),address)  # sends W/L to python code
            drawText("R to restart", 35, 50)
            for i in grid:
                for j in i:
                    if j.flag and j.val != -1:
                        j.mineFalse = True
        else:
            drawText("You WON!", 50)
            drawText("R to restart", 35, 50)
        # Draw time
        s = str(t // 15)
        screen_text = pygame.font.SysFont("Calibri", 50).render(s, True, (0, 0, 0))
        gameDisplay.blit(screen_text, (border, border))
        # Draw mine left
        screen_text = pygame.font.SysFont("Calibri", 50).render(mineLeft.__str__(), True, (0, 0, 0))
        gameDisplay.blit(screen_text, (display_width - border - 50, border))

        pygame.display.update()  # Update screen

        timer.tick(15)  # Tick fps

if __name__ == '__main__':
    try:
        gameLoop()
        pygame.quit()
        quit()
    finally:
        ''' ============================================================ '''
        mySocket.close()
        ''' ============================================================ '''
