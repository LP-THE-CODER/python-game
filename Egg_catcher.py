from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font, Button, simpledialog

# Constants
canvas_width = 800
canvas_height = 600
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 100
egg_interval = 2050

catcher_width = 100
catcher_height = 100
catcher_color = 'white'

root = Tk()
root.geometry("800x600")
c = Canvas(root, width=canvas_width, height=canvas_height, background='deep sky blue')
c.create_rectangle(-5, canvas_height - 100, canvas_width + 5, canvas_height + 5,
                  fill='sea green', width=0)

# Draw "LP" on the background
lp_text = c.create_text(400, 300, text='LP', font=("Lucida", 100), fill='white')

c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()

color_cycle = cycle(['blue', 'red', 'black', 'magenta', 'yellow', 'purple'])
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height - catcher_height - 20
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height

catcher = c.create_arc(catcher_start_x, catcher_start_y,
                      catcher_start_x2, catcher_start_y2, start=200, extent=140,
                      style='arc', outline=catcher_color, width=3)

game_font = font.Font(family="Lucida", size=18)
score = 0
score_text = c.create_text(10, 10, anchor='nw', font=game_font, fill='darkblue',
                          text='Score: ' + str(score))
lives_remaining = 3
lives_text = c.create_text(canvas_width - 10, 10, anchor='ne', font=game_font, fill='darkblue',
                           text='Lives: ' + str(lives_remaining))
eggs = []

# Function to get the player's name
def get_player_name():
    name = simpledialog.askstring("Player Name", "Enter your name:")
    if name:
        start_game(name)

# Function to start the game with the player's name
def start_game(player_name):
    messagebox.showinfo("Egg Catcher", f"Welcome, {player_name}! Press ->{OK} to start.")
    root.after(1000, create_egg)
    root.after(1000, move_eggs)
    root.after(1000, check_catch)

# Create an "Enter Name" button
enter_name_button = Button(root, text="Enter Name", command=get_player_name)
enter_name_button.pack()

# Rest of your game code remains the same



def create_egg():
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

def move_eggs():
    for egg in eggs:
        (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
        c.move(egg, 0, 10)
        if egg_y2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text='Lives: ' + str(lives_remaining))

    if lives_remaining == 0:
        end_game()

def end_game():
    game_over_message = 'Game Over!'
    messagebox.showinfo(game_over_message, 'Final Score: ' + str(score))
    root.quit()  # Exit the game

def check_catch():
    (catcher_x, catcher_y, catcher_x2, catcher_y2) = c.coords(catcher)
    for egg in eggs:
        (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
        if catcher_x < egg_x and egg_x2 < catcher_x2 and catcher_y2 - egg_y2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    root.after(100, check_catch)

def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    c.itemconfigure(score_text, text='Score: ' + str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

c.bind('<a>', move_left)
c.bind('<d>', move_right)
c.bind('<Left>', move_left)
c.bind('<Right>', move_right)
c.focus_set()

# Create a function to start the game
def start_game():
    messagebox.showinfo("Egg Catcher", "Welcome to the 'Egg Catcher' game!\nPress ->{OK} to start.")
    root.after(1000, create_egg)
    root.after(1000, move_eggs)
    root.after(1000, check_catch)

# Create a "Start Game" button
start_button = Button(root, text="Start Game", command=start_game)
start_button.pack()

# Create a function to show game information
def show_game_info():
    creator_name = "LP"
    game_info = f"Egg Catcher Game\n\nCreated by {creator_name}"
    messagebox.showinfo("Game Info", game_info)

# Create a "Game Info" button to show the game information
info_button = Button(root, text="Game Info", command=show_game_info)
info_button.pack()

root.mainloop()
