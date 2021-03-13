import tkinter as tk
import tkinter.messagebox
import random

LEN = 4

def to_two_coords(coord):
    return coord // LEN, coord % LEN

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.grid(sticky = 'NEWS')
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight = 1)
        top.columnconfigure(0, weight = 1)
        for i in range(LEN):
            self.columnconfigure(i, weight = 1, uniform = 'col')
            self.rowconfigure(i + 1, weight = 1, uniform = 'row')
        self.createWidgets()

    def createWidgets(self):
        self.newButton = tk.Button(self, text = 'New', command = self.new_field)
        self.quitButton = tk.Button(self, text = 'Exit', command = self.quit)
        self.newButton.grid(row = 0, column = 0, columnspan = LEN // 2, sticky = 'NEWS')
        self.quitButton.grid(row = 0, column = LEN // 2, columnspan = LEN // 2, sticky = 'NEWS')
        self.buttons = list()
        for i in range(1, LEN ** 2):
            button = tk.Button(self, text = str(i))
            button['command'] = lambda button = button, index = i - 1: self.change_pos(button, index)
            self.buttons.append(button)
        self.new_field()

    def new_field(self):
        self.positions = list(range(LEN ** 2))
        random.shuffle(self.positions)
        for position, button in zip(self.positions, self.buttons):
            row, column = to_two_coords(position)
            button.grid(row = row + 1, column = column, sticky = 'NEWS')
        if not self.check_field():
            self.new_field()

    def check_field(self):
        past_positions = []
        control_sum = 0
        for position in self.positions:
            temp = position
            for elem in past_positions:
                if elem < position:
                    temp -= 1
            control_sum += temp
            past_positions.append(position)
        if control_sum % 2 == 0:
            return True
        return False


    def change_pos(self, button, index):
        row, column = to_two_coords(self.positions[index])
        empty_row, empty_column = to_two_coords(self.positions[-1])
        if abs(row - empty_row) + abs(column - empty_column) == 1:
            self.positions[-1], self.positions[index] = self.positions[index], self.positions[-1]
            button.grid(row = empty_row + 1, column = empty_column, sticky = 'NEWS')
            if self.positions == list(range(LEN ** 2)):
                tk.messagebox.showinfo(message = 'You win!')
                self.new_field()

app = Application()
app.master.title('15 Game')
app.mainloop()