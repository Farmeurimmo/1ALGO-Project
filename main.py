from random import randint
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
        self.__root.config(padx=self.CANVA_PADDING_X * 4, pady=self.CANVA_PADDING_Y * 4)
        self.__running = False
        self.__pixel_size = pixel_size

        self.__directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.__directions_pawns = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        self.__n = 8
        self.__current_player = []
        self.__current_player_index = 0
        self.__selected_pawn = (-1, -1)
        self.__board = []
        self.__grid = []
        self.__toggled_blows = False
        self.__toggled_playable = False
        self.__against_bot = True

        # Frame du jeux
        self.__game_frame = Frame(self.__root)
        self.__canvas = Canvas(self.__game_frame)

        self.__button_home = Button(self.__game_frame, text='Quitter la partie',
                                    command=self.stop)
        self.__button_home.pack(padx=10, pady=5)

        self.__button_save_game = Button(self.__game_frame, text='Sauvegarder la partie',
                                         command=self.save_game)
        self.__button_save_game.pack(padx=10, pady=5)

        self.__button_display_playable = Button(self.__game_frame, text='Afficher le(s) pion(s) jouable(s)',
                                                command=self.toggle_playable,
                                                bg="red")
        self.__button_display_playable.pack(padx=10, pady=5)

        self.__button_display_blows = Button(self.__game_frame,
                                             text='Afficher le(s) cases jouable(s) pour le pion séléctionné',
                                             command=self.toggle_blows,
                                             bg="red")
        self.__button_display_blows.pack(padx=10, pady=5)

        self.__button_against_bot = Button(self.__game_frame, text='Jouer contre un robot (aléatoire)',
                                           command=self.toggle_against_bot,
                                           bg="red")
        self.__button_against_bot.pack(padx=10, pady=5)

        self.__current_player_text_content = StringVar()
        self.__current_player_text = Label(self.__game_frame, textvariable=self.__current_player_text_content,
                                           fg="black")
        self.__current_player_text.pack(padx=10, pady=10)

        self.__canvas.bind('<Button-1>', self.on_click)

        # Frame menu d'attente
        self.__waiting_frame = Frame(self.__root)
        self.__scale = Scale(self.__waiting_frame, orient='horizontal', from_=6, to=12, length=130,
                             label='Dimension du plateau', resolution=2, tickinterval=6,
                             showvalue=True, width=10, command=self.zoom)
        self.__scale.set(self.__n)
        self.__scale.pack()

        self.__button_start = Button(self.__waiting_frame, text='Démarrer la partie', command=self.start)
        self.__button_start.pack()

        self.__button_start = Button(self.__waiting_frame, text='Charger la dernière partie sauvegardée',
                                     command=self.start_game_from_file)
        self.__button_start.pack()

        self.toggle_against_bot()
        self.toggle_game_display(False)

        self.update()
        self.__root.mainloop()

    def save_game(self):
        with open('game', 'w'):  # Permet de vider le fichier
            pass

        with open("game", "w") as file:
            for row in self.__board:
                for col in row:
                    file.write(str(col))
                file.write("\n")

        messagebox.showinfo("Sauvegarde réussie",
                            "La partie a été sauvegardée et pourra être rechargée via le bouton à l'accueil.")

    def start_game_from_file(self):
        self.__board = []
        with open("game", "r") as file:
            for line in file:
                temp_list = []
                for char in line:
                    if char == '\n':
                        continue
                    temp_list.append(int(char))
                self.__board.append(temp_list)

        self.__n = len(self.__board)
        self.start(False)

    def start(self, generate_board=True):
        self.__w = self.__n * self.__pixel_size + 1  # car sinon outline ne fonctionne pas sur les case à droites
        self.__h = self.__n * self.__pixel_size + 1  # pareil mais pour les cases en bas

        self.__canvas.config(width=self.__w, height=self.__h, highlightthickness=0, bd=0, bg="white")
        self.__canvas.pack(padx=Game.CANVA_PADDING_X, pady=Game.CANVA_PADDING_Y)

        self.__current_player = self.create_players()
        if generate_board:
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

        for player in range(2):
            self.__current_player_index = player
            for row in range(self.__n):
                for col in range(self.__n):
                    if self.is_player(row, col):
                        if self.is_player_queen(row, col):
                            self.__current_player[player].set_queen_coordinates(row, col)
                            continue
                        self.__current_player[player].increase_pieces()
        self.__current_player_index = 0

        self.__against_bot = True
        self.toggle_against_bot()
        self.__running = True
        self.toggle_game_display(True)
        self.update()

    def toggle_playable(self):
        self.__toggled_playable = not self.__toggled_playable
        if not self.__toggled_playable:
            self.__button_display_playable.config(bg="red")
        else:
            self.__button_display_playable.config(bg="green")
        self.update_circles()

    def get_moves_for_pawn(self, pawn_row, pawn_col):
        moves = []
        for try_row in range(self.__n):
            for try_col in range(self.__n):
                if pawn_row == try_row and pawn_col == try_col:
                    continue
                if self.can_move(pawn_row, pawn_col, try_row, try_col):
                    moves.append((pawn_row, pawn_col, try_row, try_col))
        return moves

    def bot_move(self):
        if self.get_current_player() != 1:
            return
        can_be_took = []
        for pawn_row in range(self.__n):
            for pawn_col in range(self.__n):
                if not self.is_player(pawn_row, pawn_col):
                    continue
                can_be_took += self.get_moves_for_pawn(pawn_row, pawn_col)

        took = can_be_took[randint(0, len(can_be_took) - 1)]

        self.move(took[0], took[1], took[2], took[3], self.__board[took[0]][took[1]])

        if self.should_end():
            return

        self.invert_player()

        self.update()

    def toggle_against_bot(self):
        self.__against_bot = not self.__against_bot
        if not self.__against_bot:
            self.__button_against_bot.config(bg="red")
        else:
            self.__button_against_bot.config(bg="green")
            if self.get_current_player() == 1:
                self.bot_move()

    def toggle_blows(self):
        self.__toggled_blows = not self.__toggled_blows
        if not self.__toggled_blows:
            self.__button_display_blows.config(bg="red")
        else:
            self.__button_display_blows.config(bg="green")
        self.update_selected_blow()

    def update_selected_blow(self):
        if len(self.__grid) <= 0:
            return
        for row in range(self.__n):
            for col in range(self.__n):
                if self.__board[row][col] == 0:
                    self.__canvas.itemconfig(self.__grid[row][col], fill="white")
        if self.__selected_pawn == (-1, -1):
            return
        if not self.__toggled_blows:
            return
        moves = self.get_moves_for_pawn(self.__selected_pawn[0], self.__selected_pawn[1])
        for move in moves:
            self.__canvas.itemconfig(self.__grid[move[2]][move[3]], fill="green")

    def stop(self):
        self.__running = False
        self.toggle_game_display(False)
        self.__board = []
        self.__grid = []

    def zoom(self, event):
        self.__n = self.__scale.get()
        self.update()

    def create_players(self):
        return Player(0, self.__n - 1, 0), Player(self.__n - 1, 0, 0)

    def toggle_game_display(self, state):
        if state:
            self.__game_frame.grid(row=0, column=0, rowspan=4)
            self.__waiting_frame.grid_forget()
        else:
            self.__game_frame.grid_forget()
            self.__waiting_frame.grid(row=0, column=0, rowspan=4)

    def get_color_at(self, x, y):
        if self.__board[x][y] == 0:
            return "white"
        if self.__board[x][y] == 1:
            return "blue"
        if self.__board[x][y] == 2:
            return "purple"
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

            if not self.can_move(selected_x, selected_y, x, y):
                return

            self.move(selected_x, selected_y, x, y, self.__board[selected_x][selected_y])
            self.__selected_pawn = (-1, -1)
            self.update_selected_blow()
            self.invert_player()

            if self.should_end():
                return

            self.update()
            if self.__against_bot:
                self.bot_move()
            return
        if self.__selected_pawn == (x, y):
            self.__selected_pawn = (-1, -1)
            self.update_selected_blow()
            self.update()
            return
        if not self.is_player(x, y):
            return
        self.__selected_pawn = (x, y)

        self.update_circles()
        self.update_selected_blow()

    def should_end(self):
        if self.has_lost():
            self.invert_player()
            print("Victoire du joueur", (self.__current_player_index + 1))
            self.update()
            messagebox.showinfo("Victoire", "Victoire du joueur " + str(self.get_current_player() + 1))
            self.stop()
            return True
        return False

    def can_move(self, selected_x, selected_y, x, y):
        def is_clear_path(x1, y1, x2, y2):
            if x1 == x2:
                step = 1 if y1 < y2 else -1
                for i in range(y1 + step, y2 + step, step):
                    if self.__board[x1][i] != 0:
                        return False
            elif y1 == y2:
                step = 1 if x1 < x2 else -1
                for i in range(x1 + step, x2 + step, step):
                    if self.__board[i][y1] != 0:
                        return False
            return True

        if self.is_pawn_a_tower(selected_x, selected_y):
            if selected_x != x and selected_y != y:
                return False
            return is_clear_path(selected_x, selected_y, x, y)

        if abs(x - selected_x) == abs(y - selected_y):
            x_step = 1 if x > selected_x else -1
            y_step = 1 if y > selected_y else -1
            for i in range(1, abs(x - selected_x) + 1):
                if self.__board[selected_x + i * x_step][selected_y + i * y_step] != 0:
                    return False
            return True

        if selected_x == x or selected_y == y:
            return is_clear_path(selected_x, selected_y, x, y)

        return False

    def update(self):
        if self.__running:
            self.update_circles()
        self.update_labels()

    def has_lost(self):
        player = self.__current_player[self.__current_player_index]
        if player.get_pieces() < 2:
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

    def is_player_queen(self, x, y):
        if self.__current_player_index == 0:
            return self.__board[x][y] == 2
        if self.__current_player_index == 1:
            return self.__board[x][y] == 4
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
                                continue
                            self.__board[row][column] = 0
                            self.decrease_other_player_pawn_count()

    def update_circles(self):
        for row in range(self.__n):
            for column in range(self.__n):
                selected = "black" if self.__selected_pawn[0] == row and self.__selected_pawn[1] == column else "white"
                self.__canvas.itemconfig(self.__grid[row][column], fill=self.get_color_at(row, column),
                                         outline=selected)
                if selected == "white" and self.__toggled_playable:
                    for dr, dc in (
                            self.__directions if not self.is_pawn_a_tower(row, column) else self.__directions_pawns):
                        new_row = row + dr
                        new_col = column + dc

                        if new_row >= self.__n or new_row < 0:
                            continue
                        if new_col >= self.__n or new_col < 0:
                            continue

                        if self.is_player(row, column) and self.can_move(row, column, new_row, new_col):
                            self.__canvas.itemconfig(self.__grid[row][column], outline="lime")
                            break

    def update_labels(self):
        self.__current_player_text_content.set(f"Joueur {self.get_current_player() + 1}")


game = Game()
