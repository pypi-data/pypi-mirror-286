import tkinter as tk

from ..terminal import Terminal


class Bash(Terminal):
    """Linux Bash - Checks for bash executable in path and opens that in terminal. 
    Shows Not Available in case variable is not set."""

    shell = "/bin/bash"
    name = "Bash"
    icon = "bash"
    
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        self.available = self.check_shell()
        if not self.available:
            tk.Label(self, text="Bash not available, report an issue otherwise.").grid()
            self.name = "Not Available"
            self.icon = "error"
            return

        self.start_service()
