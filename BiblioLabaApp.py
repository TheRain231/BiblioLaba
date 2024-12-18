import tkinter as tk

from Views.LoginView import *
from Helpers.dataManager import *


class BiblioLabaApp(CTk):
    def __init__(self, dataManager):
        super().__init__()

        self.dataManager = dataManager

        self.title("Библио-Лаба")
        self.geometry("800x600")
        self.frames = {}

        # Создаем контейнер для экранов
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.current_view = None
        self.main_page = None
        self.side_panel = None
        self.open_windows = {}

        # self.show_view(LoginView, controller=self, dataManager=self.dataManager)
        self.show_view(ContentView, controller=self, dataManager=self.dataManager)

    def set_main_page(self, page):
        self.main_page = page

    def set_side_panel(self, page):
        self.side_panel = page

    def update_selected_book(self, new_book_id):
        self.dataManager.selectBook(new_book_id)
        if self.main_page:
            self.main_page.update_ui()

    def update_side_panel(self):
        if self.side_panel:
            self.side_panel.update_scrollable_checkbox_frame()

    def update_ui(self):
        if self.main_page:
            self.main_page.update_ui()
        if self.side_panel:
            self.side_panel.update_scrollable_checkbox_frame()

    def show_view(self, view_class, *args, **kwargs):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = view_class(self.container, self, dataManager=self.dataManager)
        self.current_view.pack(fill="both", expand=True)

    def open_toplevel(self, topLevel, *args, **kwargs):
        if topLevel not in self.open_windows or not self.open_windows[topLevel].winfo_exists():
            self.open_windows[topLevel] = topLevel(*args, **kwargs)
        else:
            self.open_windows[topLevel].focus()

    def close_toplevel(self, topLevel):
        if topLevel in self.open_windows and self.open_windows[topLevel].winfo_exists():
            self.open_windows[topLevel].withdraw()
            del self.open_windows[topLevel]
        else:
            print(f"Error: {topLevel} not found in open_windows.")
            print(self.open_windows)

    def loop(self):
        self.mainloop()
