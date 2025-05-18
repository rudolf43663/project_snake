import tkinter as tk
from tkinter import messagebox
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20
DELAY = 150

BACKGROUND_COLOR = "black"
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
TEXT_COLOR = "white"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Змейка")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = None
        self.running = False
        self.score = 0
        self.paused = True

        self.create_food()
        self.bind_keys()
        self.show_start_screen()

    def bind_keys(self):
        self.root.bind("<Up>", lambda e: self.change_direction("Up"))
        self.root.bind("<Down>", lambda e: self.change_direction("Down"))
        self.root.bind("<Left>", lambda e: self.change_direction("Left"))
        self.root.bind("<Right>", lambda e: self.change_direction("Right"))
        self.root.bind("<Return>", lambda e: self.start_game())

    def change_direction(self, new_dir):
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_dir != opposites[self.direction]:
            self.direction = new_dir

    def create_food(self):
        while True:
            x = random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def draw(self):
        try:
            self.canvas.delete(tk.ALL)

            #змейка
            for x, y in self.snake:
                self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=SNAKE_COLOR)

            #еда
            x, y = self.food
            self.canvas.create_oval(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=FOOD_COLOR)

            #счёт
            self.canvas.create_text(50, 10, text=f"Счёт: {self.score}", fill=TEXT_COLOR, font=("Arial", 12))
        except:
            pass
    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            new_head = (head_x, head_y - CELL_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + CELL_SIZE)
        elif self.direction == "Left":
            new_head = (head_x - CELL_SIZE, head_y)
        elif self.direction == "Right":
            new_head = (head_x + CELL_SIZE, head_y)

        #проверка на столкновение со стенами
        if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
            new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT):
            self.game_over()
            return

        #проверка на столкновения змейки с собой же
        if new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        #еда съедена?
        if new_head == self.food:
            self.score += 1
            self.create_food()
        else:
            self.snake.pop()

    def game_over(self):
        self.running = False
        messagebox.showinfo("Игра окончена", f"Вы проиграли!\nСчёт: {self.score}")
        self.root.destroy()

    def update(self):
        if self.running and not self.paused:
            self.move_snake()
            self.draw()
            self.root.after(DELAY, self.update)
        elif self.running:
            self.root.after(DELAY, self.update)

    def show_start_screen(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 40,
                                text="ЗМЕЙКА", fill=TEXT_COLOR, font=("Arial", 30, "bold"))
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                                text="Нажмите ENTER для начала", fill=TEXT_COLOR, font=("Arial", 16))
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 30,
                                text="Управление: Стрелки", fill=TEXT_COLOR, font=("Arial", 14))

    def start_game(self):
        if self.paused:
            self.paused = False
            self.running = True
            self.update()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
