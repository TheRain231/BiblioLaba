import tkinter as tk

from Views.LoginView import *


class BiblioLabaApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("Библио-Лаба")
        self.geometry("800x600")
        self.frames = {}

        # Создаем контейнер для экранов
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.current_view = None
        self.open_windows = {}

        # self.show_view(LoginView)
        self.show_view(ContentView)

    def show_view(self, view_class):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = view_class(self.container, self)
        self.current_view.pack(fill="both", expand=True)

    def open_toplevel(self, topLevel):
        if topLevel not in self.open_windows or not self.open_windows[topLevel].winfo_exists():
            self.open_windows[topLevel] = topLevel(self)
        else:
            self.open_windows[topLevel].focus()

    def loop(self):
        self.mainloop()
