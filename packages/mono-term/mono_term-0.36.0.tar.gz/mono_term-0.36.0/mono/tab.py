import tkinter as tk

ICONS = {
    "cmd": "terminal-cmd",
    "bash": "terminal-bash",
    "powershell": "terminal-powershell"
}

class Tab(tk.Frame):
    def __init__(self, master, terminal, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base = master.base
        self.theme = self.base.theme

        self.terminal = terminal
        self.selected = False

        self.bg, self.fg, self.hbg, self.hfg = self.theme.tab
        self.config(bg=self.theme.border)

        self.container = tk.Frame(self, bg=self.bg)
        self.container.pack(side=tk.LEFT, fill=tk.X, expand=True) # for lines bw set pady=(0,1)

        self.name_label = tk.Label(self, text=terminal.name  or terminal.__class__.__name__, padx=5, 
                             font=('Segoe UI', 11), anchor=tk.W, bg=self.bg, fg=self.fg)
        self.name_label.pack(in_=self.container, side=tk.LEFT, expand=True, fill=tk.X)

        self.closebtn = tk.Label(self, text='×', font=('Arial', 15), fg=self.fg, bg=self.bg)
        self.closebtn.bind("<Button-1>", self.close)
        self.closebtn.pack(in_=self.container, padx=5)

        self.bind("<Button-1>", self.select)
        self.name_label.bind("<Button-1>", self.select)

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.off_hover)

    def close(self, *_) -> None:
        self.master.close_tab(self)

    def on_hover(self, *_) -> None:
        if not self.selected:
            self.name_label.config(bg=self.hbg)
            self.container.config(bg=self.hbg)
            self.closebtn.config(bg=self.hbg)

            self.hovered = True

    def off_hover(self, *_) -> None:
        if not self.selected:
            self.name_label.config(bg=self.bg)
            self.container.config(bg=self.bg)
            self.closebtn.config(bg=self.bg)
            self.hovered = False

    def deselect(self, *_) -> None:
        if self.selected:
            self.terminal.grid_remove()

            self.name_label.config(bg=self.bg, fg=self.fg)
            self.container.config(bg=self.bg)
            self.closebtn.config(bg=self.bg, activeforeground=self.fg)
            self.selected = False

    def select(self, *_) -> None:
        if not self.selected:
            self.master.set_active_tab(self)
            self.terminal.grid(column=0, row=0, sticky=tk.NSEW)

            self.name_label.config(bg=self.hbg, fg=self.hfg)
            self.container.config(bg=self.hbg)
            self.closebtn.config(bg=self.hbg, activeforeground=self.hfg)
            self.selected = True
