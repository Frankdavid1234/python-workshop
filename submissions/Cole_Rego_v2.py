import tkinter
import random  


ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS #25*25 = 625
WINDOW_HEIGHT = TILE_SIZE * ROWS #25*25 = 625

BOMB_FUSE_LENGTH = 15
BOMB_RADIUS = 2 * TILE_SIZE

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = BOMB_FUSE_LENGTH
        self.affected_tiles = []

        for x in range(-BOMB_RADIUS, BOMB_RADIUS + TILE_SIZE, TILE_SIZE):
            for y in range(-BOMB_RADIUS, BOMB_RADIUS + TILE_SIZE, TILE_SIZE):
                self.affected_tiles.append(Tile(
                    (self.x + x) % WINDOW_WIDTH,
                    (self.y + y) % WINDOW_HEIGHT
                ))

    def explode(self):
        global snake, snake_body, game_over
        for affected in self.affected_tiles:
            for tile in snake_body:
                if (tile.x == affected.x and tile.y == affected.y):
                    game_over = True
                    return

            # check for head separately
            if (snake.x == affected.x and snake.y == affected.y):
                game_over = True
                return

#game window
window = tkinter.Tk()
window.title("American Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

#format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) #single tile, snake's head
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = [] #multiple snake tiles
bombs = []
game_started = False
game_over = False
score = 0

#game loop

def change_direction(e): #e = event
    # print(e)
    # print(e.keysym)

    global velocityX, velocityY, game_over, game_started

    if (game_over):
        # reset_game() 
        return #edit this code to reset game variables to play again

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
        
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1

    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

    # start game when player moves
    if (velocityX != 0 or velocityY != 0):
        game_started = True


def move():
    global snake, food, snake_body, bombs, game_over, score
    if (game_over):
        return

    # loop around edges
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        snake.x = snake.x % WINDOW_WIDTH
        snake.y = snake.y % WINDOW_HEIGHT
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    
    #collision
    if (snake.x == food.x and snake.y == food.y): 
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    #update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def update_bombs():
    global bombs
    for bomb in bombs:
        bomb.timer -= 1
        if bomb.timer <= 0:
            bomb.explode()
            bombs.remove(bomb)
            print("boom")

    # 15% chance per update to spawn a bomb
    if random.randint(0, 100) < 15:
        bombs.append(Bomb(
            random.randint(0, COLS-1) * TILE_SIZE,
            random.randint(0, ROWS-1) * TILE_SIZE
        ))


def draw():
    global snake, food, snake_body, bombs, game_over, score, game_started
   
    move()

    if game_started:
        update_bombs()

    canvas.delete("all")

    # draw bombs and affected tiles
    for bomb in bombs:
        canvas.create_rectangle(bomb.x, bomb.y, bomb.x + TILE_SIZE, bomb.y + TILE_SIZE, fill = 'gray')

        for tile in bomb.affected_tiles:
            if not (tile.x == bomb.x and tile.y == bomb.y):
                value = int(255 * (1 - (bomb.timer / BOMB_FUSE_LENGTH)))
                color = f"#{value:02x}{value:02x}00"
                canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = color)

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = 'red')

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = 'green')
    
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'green')

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill = "white")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "white")
    
    window.after(100, draw) #call draw again every 100ms (1/10 of a second) = 10 frames per second
def run():
    
    draw()
    
    window.bind("<KeyRelease>", change_direction) #when you press on any key and then let go
    window.mainloop() #used for listening to window events like key presses
    
while True:
    run()

# Start game
gameloop()

# Start Tkinter
window.mainloop()

# Start Tkinter
window.mainloop()