import tkinter
import random 

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS #25*25 = 625
WINDOW_HEIGHT = TILE_SIZE * ROWS #25*25 = 625

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window
window = tkinter.Tk()
window.title("Snake")
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
bullet = Tile(TILE_SIZE * -1, TILE_SIZE * random.randint(0, ROWS-1))
bulletDir = 0
snake_body = [] #multiple snake tiles
size = 1
game_over = False
score = 0
playing = False


#game l
def reset_game():
    global snake, food, velocityX, velocityY, snake_body, game_over, score
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) #single tile, snake's head
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 0
    velocityY = 0
    snake_body = [] #multiple snake tiles
    game_over = False
    score = 0

def change_direction(e): #e = event
    # print(e)
    # print(e.keysym)

    global velocityX, velocityY, game_over, playing
    if (game_over):
        reset_game() 
        return #edit this code to reset game variables to play again

    if (playing == False):
        playing = True

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


def move():
    global snake, food, snake_body, game_over, score, bullet, size
    if (game_over):
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT): # hit wall
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    if (snake.x == bullet.x and snake.y == bullet.y):
        game_over = True
        return
    
    #collision
    if (snake.x == food.x and snake.y == food.y): 
        snake_body.append(Tile(food.x, food.y))
        size += 1
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

    for i in range(len(snake_body)):
        if (snake_body[i].x == bullet.x and snake_body[i].y == bullet.y):
            size = i
            score = i
            print(i)
        if (i >= size):
            snake_body.remove(snake_body[i])
            return

def bullet_move():
    global snake, food, snake_body, game_over, score, bullet, bulletDir

    if bulletDir == 0:
        bullet.x += 1 * TILE_SIZE
    elif bulletDir == 1:
        bullet.x -= 1 * TILE_SIZE
    elif bulletDir == 2:
        bullet.y += 1 * TILE_SIZE
    elif bulletDir == 3:
        bullet.y -= 1 * TILE_SIZE

    if (bullet.x > WINDOW_WIDTH or bullet.x < 0 or bullet.y > WINDOW_HEIGHT or bullet.y < 0):
        bulletDir = random.randint(0, 3)
        if (bulletDir == 0):
            bullet.x = 0
            bullet.y = random.randint(0, ROWS-1) * TILE_SIZE
        elif (bulletDir == 1):
            bullet.x = (COLS - 1) * TILE_SIZE
            bullet.y = random.randint(0, ROWS-1) * TILE_SIZE
        elif (bulletDir == 2):
            bullet.x = random.randint(0, COLS-1) * TILE_SIZE
            bullet.y = 0
        elif (bulletDir == 3):
            bullet.x = random.randint(0, COLS-1) * TILE_SIZE
            bullet.y = (ROWS - 1) * TILE_SIZE
    
    

def draw():
    global snake, food, snake_body, game_over, score, bullet
   
    move()

    if playing and game_over != True:
        bullet_move()

    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = 'red')

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = 'palegreen')
    
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'darkgreen')

    canvas.create_rectangle(bullet.x, bullet.y, bullet.x + TILE_SIZE, bullet.y + TILE_SIZE, fill = 'gray')

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
