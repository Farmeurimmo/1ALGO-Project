from tkinter import *
from tkinter import messagebox


class Player:
    def __init__(self, queen_x, queen_y, n):
        self.__queen_x = queen_x
        self.__queen_y = queen_y
        self.__n = n

    def decrease_pieces(self):
        self.__n -= 1

    def increase_pieces(self):
        self.__n += 1

    def get_pieces(self):
        return self.__n

    def get_queen_coordinates(self):
        return self.__queen_x, self.__queen_y

    def set_queen_coordinates(self, queen_x, queen_y):
        self.__queen_x = queen_x
        self.__queen_y = queen_y


class Game:
    CANVA_PADDING_X = 10
    CANVA_PADDING_Y = 10

    def __init__(self, pixel_size=60):
        self.__w = 0
        self.__h = 0
        self.__root = Tk()
        self.__root.title("Game")
        self.__running = False
        self.__pixel_size = pixel_size

        self.__n = 8
        self.__current_player = []
        self.__current_player_index = 0
        self.__selected_pawn = (-1, -1)
        self.__board = []
        self.__grid = []

        # Frame du jeux
        self.__game_frame = Frame(self.__root)
        self.__canvas = Canvas(self.__game_frame)

        self.__current_player_text_content = StringVar()
        self.__current_player_text = Label(self.__game_frame, textvariable=self.__current_player_text_content,
                                           fg="black")
        self.__current_player_text.pack(padx=20, pady=20)

        self.__canvas.bind('<Button-1>', self.on_click)

        # Frame menu d'attente
        self.__menu_frame = Frame(self.__root)
        self.__scale = Scale(self.__menu_frame, orient='horizontal', from_=6, to=12, length=200,
                             label='Dimension du plateau',
                             showvalue=True, width=10, command=self.zoom)
        self.__scale.set(self.__n)
        self.__scale.pack()

        self.__button_start = Button(self.__menu_frame, text='Démarrer la partie', command=self.start)
        self.__button_start.pack()

        self.toggle_game_display(False)

        self.update()
        self.__root.mainloop()

    def start(self):
        self.__w = self.__n * self.__pixel_size + 1  # car sinon outline ne fonctionne pas sur les case à droites
        self.__h = self.__n * self.__pixel_size + 1  # pareil mais pour les cases en bas

        self.__canvas.config(width=self.__w, height=self.__h, highlightthickness=0, bd=0, bg="white")
        self.__canvas.pack(padx=Game.CANVA_PADDING_X, pady=Game.CANVA_PADDING_Y)

        self.__board = self.init_board()
        for i in range(self.__n):
            row = []
            for j in range(self.__n):
                self.__canvas.create_rectangle(
                    i * self.__pixel_size, j * self.__pixel_size, (i + 1) * self.__pixel_size,
                    (j + 1) * self.__pixel_size, outline="black"
                )
                circle_parent = self.__canvas.create_oval(i * self.__pixel_size + 4, j * self.__pixel_size + 4,
                                                          (i + 1) * self.__pixel_size - 4,
                                                          (j + 1) * self.__pixel_size - 4,
                                                          outline="black",
                                                          width=4)
                self.__canvas.create_oval(i * self.__pixel_size + 6, j * self.__pixel_size + 6,
                                          (i + 1) * self.__pixel_size - 6, (j + 1) * self.__pixel_size - 6,
                                          outline="white",
                                          width=2)
                row.append(circle_parent)
            self.__grid.append(row)

        self.__running = True
        self.toggle_game_display(True)
        self.update()

    def zoom(self, event):
        self.__n = self.__scale.get()
        self.update()

    def toggle_game_display(self, state):
        if state:
            self.__game_frame.grid(row=0, column=0, rowspan=4)
            self.__menu_frame.grid_forget()
        else:
            self.__game_frame.grid_forget()
            self.__menu_frame.grid(row=0, column=0, rowspan=4)
            # show menu

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
        player_1 = Player(0, self.__n - 1, 0)
        player_2 = Player(self.__n - 1, 0, 0)
        for i in range(self.__n):
            row = []
            for j in range(self.__n):
                row.append(0)
            board.append(row)

        for i in range(self.__n // 2):
            for j in range(self.__n // 2, self.__n):
                board[i][j] = 1
                player_1.increase_pieces()
        board[0][self.__n - 1] = 2

        for i in range(self.__n // 2, self.__n):
            for j in range(self.__n // 2):
                board[i][j] = 3
                player_2.increase_pieces()
        board[self.__n - 1][0] = 4

        self.__current_player = [player_1, player_2]
        return board

    def on_click(self, event):
        if not self.__running:
            return
        x = event.x // self.__pixel_size
        y = event.y // self.__pixel_size
        if y >= self.__pixel_size:
            return
        if x >= self.__pixel_size * self.__n:
            return
        if x < 0:
            return
        if y < 0:
            return
        if self.__board[x][y] == 0:
            if self.__selected_pawn == (-1, -1):
                return
            selected_x, selected_y = self.__selected_pawn
            print("select x", selected_x, "selected y", y)
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
                    print("x", x + i * x_step, "y", y + i * y_step)
                    if self.__board[x + i * x_step][y + i * y_step] != 0:
                        return

            self.move(selected_x, selected_y, x, y, self.__board[selected_x][selected_y])
            self.__selected_pawn = (-1, -1)
            self.invert_player()

            if self.has_lost():
                self.invert_player()
                print("Victoire du joueur", (self.__current_player_index + 1))
                self.update()
                self.__running = False
                messagebox.showinfo("Victoire", "Victoire de " + str(self.get_current_player() + 1))
                return

            self.update()
            return
        if self.__selected_pawn == (x, y):
            self.__selected_pawn = (-1, -1)
            self.update()
            return
        if not self.is_player(x, y):
            return
        self.__selected_pawn = (x, y)
        print("clicked on x", x, "y", y)

        self.update_circles()

    def update(self):
        if self.__running:
            self.update_circles()
        self.update_labels()

    def update_circles(self):
        for row in range(self.__n):
            for column in range(self.__n):
                selected = "black" if self.__selected_pawn[0] == row and self.__selected_pawn[1] == column else "white"
                self.__canvas.itemconfig(self.__grid[row][column], fill=self.get_color_at(row, column),
                                         outline=selected)

    def has_lost(self):
        player = self.__current_player[self.__current_player_index]
        if player.get_pieces() <= 2:
            return True
        return False

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

    def decrease_other_player_pawn_count(self):
        self.__current_player[self.__current_player_index - 1].decrease_pieces()

    def move(self, old_x, old_y, new_x, new_y, type):
        self.__board[old_x][old_y] = 0
        self.__board[new_x][new_y] = type
        player = self.__current_player[self.__current_player_index]
        if player is not None:
            queen_x, queen_y = player.get_queen_coordinates()
            if queen_x == old_x and queen_y == old_y:
                player.set_queen_coordinates(new_x, new_y)
            else:
                min_x, min_y, max_x, max_y = min(queen_x, new_x), min(queen_y, new_y), max(queen_x, new_x), max(queen_y,
                                                                                                                new_y)
                for row in range(min_x, max_x + 1):
                    for column in range(min_y, max_y + 1):
                        if not self.is_player(row, column) and self.__board[row][column] != 0:
                            if self.__board[row][column] == 2 or self.__board[row][column] == 4:  # Si c'est une reine
                                return
                            self.__board[row][column] = 0
                            self.decrease_other_player_pawn_count()

    def update_labels(self):
        self.__current_player_text_content.set(f"Player {self.get_current_player() + 1}")


game = Game()
