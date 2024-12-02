from Views.LoginView import *
import tkinter as tk

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

        self.show_view(LoginView)

    def show_view(self, view_class):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = view_class(self.container, self)
        self.current_view.pack(fill="none", expand=True)

    def loop(self):
        self.mainloop()
