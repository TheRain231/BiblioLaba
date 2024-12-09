from customtkinter import *
from PIL import Image


class ContentView(CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.controller = controller

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=30)
        self.grid_rowconfigure(0, weight=1)

        self.sidePanel = SidePanel(self)
        self.sidePanel.grid(row=0, column=0, sticky="nsew")

        self.mainPage = MainPage(self)
        self.mainPage.grid(row=0, column=1, sticky="nsew")


class MainPage(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=40)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=30)
        self.grid_rowconfigure(2, weight=0)

        BookImage = CTkImage(Image.open("Assets/mockCover.png"),
                             size=(150, 200))
        self.BookCover = CTkLabel(master=self,
                                  text="",
                                  image=BookImage)
        self.BookCover.grid(row=0, column=0, padx=25, pady=25, sticky="nw")

        self.titleLabels = TitleLabels(self)
        self.titleLabels.grid(row=0, column=1, padx=0, pady=0, sticky="w")

        self.description = CTkLabel(master=self, text="Описание")
        self.description.grid(row=1, column=0, columnspan=2, padx=25, pady=0, sticky="nw")

        self.bookButton = CTkButton(master=self, text="Забронировать")
        self.bookButton.grid(row=2, column=0, columnspan=2, pady=10)

class TitleLabels(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color="transparent")

        self.title = CTkLabel(self, text="Книга")
        self.title.configure(font=('Helvetica bold', 25))

        self.title.grid(row=0, column=0, sticky="nsw")
        self.author = CTkLabel(self, text="Автор")
        self.author.grid(row=1, column=0, sticky="nsw")
        self.genre = CTkLabel(self, text="Жанр")
        self.genre.grid(row=2, column=0, sticky="nsw")
        self.publisher = CTkLabel(self, text="Издательство")
        self.publisher.grid(row=3, column=0, sticky="nsw")


class SidePanel(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(corner_radius=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.title = CTkLabel(self, text="Библио-лаба", font=("MarkerFelt-Thin", 25))
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="new")

        self.searchBar = SearchBar(self)
        self.searchBar.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        values = ["value 1", "value 2", "value 3", "value 4", "value 5", "value 6",
                  "value 7", "value 8", "value 9", "value 10", "value 11", "value 12",
                  "value 13", "value 14", "value 15", "value 16", "value 17", "value 18"]
        self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, values=values)
        self.scrollable_checkbox_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")

        settingsImage = CTkImage(Image.open("Assets/settings.png"),
                                 size=(23, 23))
        self.settings = CTkButton(self, text="Настройки", image=settingsImage, text_color=("black", "white"))
        self.settings.configure(fg_color="transparent", hover_color=("#cfcfcf", "#333"))
        self.settings.grid(padx=10, pady=5, sticky="ew")


class SearchBar(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        magnifyingGlassImage = CTkImage(Image.open("Assets/magnifyingglass.png"),
                                        size=(23, 23))
        magnifyingGlass = CTkLabel(master=self,
                                   text="",
                                   image=magnifyingGlassImage)
        magnifyingGlass.grid(row=0, column=0, padx=2, pady=0, sticky="nsew")

        self.searchEntry = CTkEntry(self, placeholder_text="Поиск")
        self.searchEntry.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="nsew")
        self.searchEntry.bind('<Return>', self.searchBooks)

    def searchBooks(self, event=None):
        print(f"i probably should search smth like \"{self.searchEntry.get()}\"")


class MyScrollableCheckboxFrame(CTkScrollableFrame):
    def __init__(self, master, values):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = CTkButton(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="ew")
            self.checkboxes.append(checkbox)
