from tkinter import *


class Player:
    def __init__(self, queen_x, queen_y, n):
        self.__queen_x = queen_x
        self.__queen_y = queen_y
        self.__n = n

    def decrease_pieces(self):
        self.__n -= 1

    def get_queen_coordinates(self):
        return self.__queen_x, self.__queen_y

    def set_queen_coordinates(self, queen_x, queen_y):
        self.__queen_x = queen_x
        self.__queen_y = queen_y


class Game:
    CANVA_PADDING_X = 10
    CANVA_PADDING_Y = 10

    def __init__(self, n, pixel_size):
        self.__w = n * pixel_size + 1  # car sinon outline ne fonctionne pas sur les case à droites
        self.__h = n * pixel_size + 1  # pareil mais pour les cases en bas
        self.__rows = 1
        self.__columns = n
        self.__root = Tk()
        self.__root.title("Game")
        self.__running = False
        self.__pixel_size = pixel_size

        self.__frame1 = Frame(self.__root)
        self.__frame1.grid(row=0, column=0, rowspan=4)
        self.__canvas = Canvas(self.__frame1)
        self.__canvas.config(width=self.__w, height=self.__h, highlightthickness=0, bd=0, bg="white")
        self.__canvas.pack(padx=Game.CANVA_PADDING_X, pady=Game.CANVA_PADDING_Y)

        self.__current_player_text = StringVar()
        self.__text1 = Label(self.__frame1, textvariable=self.__current_player_text, fg="black")
        self.__text1.pack(padx=20, pady=20)

        self.__n = n
        self.__current_player = []
        self.__board = self.init_board()
        self.__current_player_index = 0
        self.__selected_pawn = (-1, -1)

        self.__grid = []

        for i in range(self.__n):
            row = []
            for j in range(self.__n):
                self.__canvas.create_rectangle(
                    i * pixel_size, j * pixel_size, (i + 1) * pixel_size, (j + 1) * pixel_size, outline="black"
                )
                circle_parent = self.__canvas.create_oval(i * pixel_size + 4, j * pixel_size + 4,
                                                          (i + 1) * pixel_size - 4, (j + 1) * pixel_size - 4,
                                                          outline="black",
                                                          width=4)
                self.__canvas.create_oval(i * pixel_size + 6, j * pixel_size + 6,
                                          (i + 1) * pixel_size - 6, (j + 1) * pixel_size - 6, outline="white",
                                          width=2)
                row.append(circle_parent)
            self.__grid.append(row)

        self.__canvas.bind('<Button-1>', self.on_click)

        self.update()
        self.__root.mainloop()

    def get_color_at(self, x, y):
        if self.__board[x][y] == 0:
            return "white"
        if self.__board[x][y] == 1:
            return "blue"
        if self.__board[x][y] == 2:
            return "pink"
        if self.__board[x][y] == 3:
            return "red"
        if self.__board[x][y] == 4:
            return "orange"
        return "black"

    def init_board(self):
        board = []
        for i in range(self.__n):
            row = []
            for j in range(self.__n):
                row.append(0)
            board.append(row)

        for i in range(self.__n // 2):
            for j in range(self.__n // 2, self.__n):
                board[i][j] = 1
        board[0][self.__n - 1] = 2

        for i in range(self.__n // 2, self.__n):
            for j in range(self.__n // 2):
                board[i][j] = 3
        board[self.__n - 1][0] = 4

        self.__current_player = [Player(0, self.__n - 1, self.__n), Player(self.__n - 1, 0, self.__n)]
        return board

    def on_click(self, event):
        x = event.x // self.__pixel_size
        y = event.y // self.__pixel_size
        if y >= self.__pixel_size:
            return
        if x >= self.__pixel_size * self.__columns:
            return
        if x < 0:
            return
        if y < 0:
            return
        if self.__board[x][y] == 0:
            if self.__selected_pawn == (-1, -1):
                return
            selected_x, selected_y = self.__selected_pawn
            if self.is_pawn_a_tower(selected_x, selected_y):
                if not (selected_x == x or selected_y == y):
                    return
                if selected_x == x:
                    for i in range(min(y, selected_y) + 1, max(y, selected_y)):
                        if self.__board[x][i] != 0:
                            return
                else:
                    for i in range(min(x, selected_x) + 1, max(x, selected_x)):
                        if self.__board[i][y] != 0:
                            return
            else:
                if not abs(x - selected_x) == abs(y - selected_y):
                    return
                x_step = 1 if x > selected_x else -1
                y_step = 1 if y > selected_y else -1

                for i in range(1, abs(x - selected_x)):
                    if self.__board[x + i * x_step][y + i * y_step] != 0:
                        return

            self.move(selected_x, selected_y, x, y, self.__board[selected_x][selected_y])
            self.__selected_pawn = (-1, -1)
            self.invert_player()
            self.update()
            return
        if self.__selected_pawn == (x, y):
            self.__selected_pawn = (-1, -1)
            self.update()
            return
        if not self.is_player(x, y):
            return
        self.__selected_pawn = (x, y)

        self.update_circles()
        # game cycle

    def update(self):
        self.update_circles()
        self.update_labels()

    def update_circles(self):
        for row in range(self.__n):
            for column in range(self.__n):
                selected = "black" if self.__selected_pawn[0] == row and self.__selected_pawn[1] == column else "white"
                self.__canvas.itemconfig(self.__grid[row][column], fill=self.get_color_at(row, column),
                                         outline=selected)

    def get_current_player(self):
        return self.__current_player_index

    def is_player(self, x, y):
        if self.__current_player_index == 0:
            return self.__board[x][y] == 1 or self.__board[x][y] == 2
        if self.__current_player_index == 1:
            return self.__board[x][y] == 3 or self.__board[x][y] == 4
        return False

    def invert_player(self):
        self.__current_player_index = 1 if self.__current_player_index == 0 else 0

    def is_pawn_a_tower(self, x, y):
        return self.__board[x][y] == 1 or self.__board[x][y] == 3

    def move(self, old_x, old_y, new_x, new_y, type):
        self.__board[old_x][old_y] = 0
        self.__board[new_x][new_y] = type

    def update_labels(self):
        self.__current_player_text.set(f"Player {self.get_current_player() + 1}")


game = Game(8, 60)
