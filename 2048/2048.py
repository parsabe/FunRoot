import tkinter as tk
from tkinter import messagebox
import random







SIZE = 4
TILE_COLORS = {
    0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
    16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
    256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
}
FONT = ("Helvetica", 24, "bold")

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0

        self.canvas = tk.Canvas(self.root, bg="#bbada0", width=400, height=400)
        self.canvas.pack()
        self.root.bind("<Key>", self.key_handler)

        self.tile_ids = [[None]*SIZE for _ in range(SIZE)]
        self.spawn_tile()
        self.spawn_tile()
        self.draw_board()

    def spawn_tile(self):
        empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if self.board[i][j] == 0]
        if not empty:
            return
        i, j = random.choice(empty)
        self.board[i][j] = 4 if random.random() < 0.1 else 2

    def draw_board(self):
        self.canvas.delete("all")
        self.tile_ids = [[None]*SIZE for _ in range(SIZE)]
        tile_size = 100
        padding = 10
        for i in range(SIZE):
            for j in range(SIZE):
                val = self.board[i][j]
                color = TILE_COLORS.get(val, "#3c3a32")
                x1 = j * tile_size + padding
                y1 = i * tile_size + padding
                x2 = x1 + tile_size - padding * 2
                y2 = y1 + tile_size - padding * 2

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#bbada0")
                if val != 0:
                    text_id = self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(val), font=FONT, fill="#776e65")
                    self.tile_ids[i][j] = text_id

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
        return row

    def move_left(self):
        moved = False
        new_board = []
        for row in self.board:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final = self.compress(merged)
            if final != row:
                moved = True
            new_board.append(final)
        self.board = new_board
        return moved

    def move_right(self):
        self.board = [row[::-1] for row in self.board]
        moved = self.move_left()
        self.board = [row[::-1] for row in self.board]
        return moved

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def animate_move(self, old_board):
        duration = 100  # total animation in ms
        steps = 5
        delay = duration // steps
        tile_size = 100
        padding = 10

        def get_coords(i, j):
            x = j * tile_size + padding + tile_size // 2 - padding
            y = i * tile_size + padding + tile_size // 2 - padding
            return x, y

        moving_tiles = []
        matched = set()
        for i in range(SIZE):
            for j in range(SIZE):
                old_val = old_board[i][j]
                new_val = self.board[i][j]
                if new_val != 0 and old_val != new_val:
                    for ni in range(SIZE):
                        for nj in range(SIZE):
                            if old_board[ni][nj] == new_val and (ni, nj) not in matched:
                                moving_tiles.append(((ni, nj), (i, j), new_val))
                                matched.add((ni, nj))
                                break

        for step in range(1, steps + 1):
            self.canvas.delete("all")
            factor = step / steps
            for i in range(SIZE):
                for j in range(SIZE):
                    val = self.board[i][j]
                    if val != 0:
                        sx, sy = get_coords(i, j)
                        self.canvas.create_rectangle(sx - 45, sy - 45, sx + 45, sy + 45,
                                                     fill=TILE_COLORS.get(val, "#3c3a32"))
                        self.canvas.create_text(sx, sy, text=str(val), font=FONT)

            for (start, end, val) in moving_tiles:
                sx, sy = get_coords(*start)
                ex, ey = get_coords(*end)
                cx = sx + (ex - sx) * factor
                cy = sy + (ey - sy) * factor
                color = TILE_COLORS.get(val, "#3c3a32")
                self.canvas.create_rectangle(cx - 45, cy - 45, cx + 45, cy + 45, fill=color)
                self.canvas.create_text(cx, cy, text=str(val), font=FONT)

            self.root.update()
            self.root.after(delay)

    def key_handler(self, event):
        old_board = [row[:] for row in self.board]
        moved = False
        if event.keysym == "Left":
            moved = self.move_left()
        elif event.keysym == "Right":
            moved = self.move_right()
        elif event.keysym == "Up":
            moved = self.move_up()
        elif event.keysym == "Down":
            moved = self.move_down()
        else:
            return

        if moved:
            self.animate_move(old_board)
            self.spawn_tile()
            self.draw_board()
            if self.check_win():
                messagebox.showinfo("2048", "🎉 You win!")
                self.root.quit()
            elif self.check_game_over():
                messagebox.showinfo("2048", "💀 Game Over!")
                self.root.quit()

    def check_win(self):
        return any(any(cell == 2048 for cell in row) for row in self.board)

    def check_game_over(self):
        if any(0 in row for row in self.board):
            return False
        for i in range(SIZE):
            for j in range(SIZE - 1):
                if self.board[i][j] == self.board[i][j + 1]:
                    return False
                if self.board[j][i] == self.board[j + 1][i]:
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
