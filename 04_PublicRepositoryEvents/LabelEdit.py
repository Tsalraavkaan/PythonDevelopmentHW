import tkinter as tk

HEIGHT = 32
SRIF_PARAMS = ("DejaVu Sans Mono", 16)
CORRECT_CONST = 19 #Correct font and size
TAB_SIZE = 4


class coord():
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y


class InputLabel(tk.Label):
    def __init__(self, master=None):
        self.S = tk.StringVar()
        self.colors = ["white", "black"]
        super().__init__(master,
            cursor="xterm",
            font=(SRIF_PARAMS),
            takefocus=True,
            textvariable=self.S,
            anchor=tk.NW,
            bg=self.colors[0],
            fg=self.colors[1])
        self.F = tk.Frame(self, bg=self.colors[0], height=HEIGHT, width=1)
        self.strip_coords = coord(0, 1)
        self.F.place(x=self.strip_coords.x, y=self.strip_coords.y)
        self.flag = False

        self.strip_state()
        self.bind('<Key>', self.key_func)
        self.bind('<Button-1>', self.left_buttom_func)

    def set_strip_coords(self, x, y):
        if x > len(self.S.get()):
            return
        self.strip_coords.x = x
        self.strip_coords.y = y
        self.F.place(x=self.strip_coords.x * CORRECT_CONST + 1, y=self.strip_coords.y)

    def strip_state(self):
        if self.flag:
            self.F.configure(bg=self.colors[0])
            self.flag = False
        else:
            self.F.configure(bg=self.colors[1])
            self.flag = True
        self.master.after(400, self.strip_state)

    def key_func(self, event):
        if event.keysym == "Right" or event.keysym == "KP_Right":
            self.set_strip_coords(self.strip_coords.x + 1, self.strip_coords.y)
        elif event.keysym == "Left" or event.keysym == "KP_Left":
            self.set_strip_coords(self.strip_coords.x - 1, self.strip_coords.y)
        elif event.keysym == 'Tab':
            self.S.set(self.S.get()[:self.strip_coords.x] + ' ' * TAB_SIZE +
                self.S.get()[self.strip_coords.x:])
            self.set_strip_coords(self.strip_coords.x + TAB_SIZE, self.strip_coords.y)
        elif event.keysym == 'Return':
            print("Unsupported feature :)") #TO DO!
        elif event.keysym == "Home" or event.keysym == "KP_Home":
            self.set_strip_coords(0, 1)
        elif event.keysym == "End" or event.keysym == "KP_End":
            self.set_strip_coords(len(self.S.get()), 1)
        elif event.keysym == 'BackSpace':
            if self.strip_coords.x > 0:
                self.S.set(self.S.get()[:self.strip_coords.x - 1]
                    + self.S.get()[self.strip_coords.x:])
                self.set_strip_coords(self.strip_coords.x - 1, self.strip_coords.y)
        elif event.keysym == 'Delete' or event.keysym == 'KP_Delete':
                if self.strip_coords.x < len(self.S.get()):
                    self.S.set(self.S.get()[:self.strip_coords.x]
                        + self.S.get()[self.strip_coords.x + 1:])
        elif event.char.isprintable():
            self.S.set(self.S.get()[:self.strip_coords.x] + event.char +
                self.S.get()[self.strip_coords.x:])
            self.set_strip_coords(self.strip_coords.x + 1, self.strip_coords.y)

    def left_buttom_func(self, event):
        self.focus_set()
        self.set_strip_coords(event.x // CORRECT_CONST + 1, (event.y // HEIGHT) * HEIGHT)


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky='NEWS')
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.labelText = InputLabel(self)
        self.labelText.grid(sticky="EW")
        self.buttonQuit = tk.Button(self, text="Quit", command=self.master.quit)
        self.buttonQuit.grid()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1, uniform='col')
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1, uniform='row')


app = Application()
app.master.title('LabelText')
app.mainloop()