from Views.AppendToplevelWindow import *
from Views.SettingsToplevelWindow import *
from PIL import Image
from componds.CTkUrlLabel import *
from componds.MyScrollableCheckboxFrame import *
from threading import Thread

from tkinter import messagebox


class ContentView(CTkFrame):
    def __init__(self, master, controller, dataManager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.controller = controller

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=30)
        self.grid_rowconfigure(0, weight=1)

        self.sidePanel = SidePanel(self, controller, dataManager)
        self.sidePanel.grid(row=0, column=0, sticky="nsew")

        self.mainPage = MainPage(self, controller, dataManager)
        self.mainPage.grid(row=0, column=1, sticky="nsew")


class MainPage(CTkFrame):
    def __init__(self, master, controller, dataManager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.dataManager = dataManager
        self.controller = controller
        self.configure(fg_color="transparent")

        self.controller.set_main_page(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=40)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=30)
        self.grid_rowconfigure(2, weight=0)

        # Обложка книги
        self.bookCover = CTkUrlLabel(self, text="Fetching Image", url_image_size=(150, 200))
        self.bookCover.grid(row=0, column=0, padx=25, pady=25, sticky="nw")

        # Кнопка добавления
        plusImage = CTkImage(Image.open("Assets/plus.png"), size=(23, 23))
        self.plusButton = CTkButton(self, text="", image=plusImage, width=30,
                                    text_color=("black", "white"),
                                    fg_color="transparent", hover_color=("#cfcfcf", "#222"),
                                    command=self.open_append_window)
        self.plusButton.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        # Заголовки и метаданные книги
        self.titleLabels = TitleLabels(self)
        self.titleLabels.grid(row=0, column=1, padx=0, pady=0, sticky="w")

        # Описание книги
        self.description = CTkLabel(master=self, text="")
        self.description.grid(row=1, column=0, columnspan=2, padx=25, pady=0, sticky="nw")

        # Кнопка бронирования
        self.bookButton = CTkButton(master=self, text="Забронировать", command=self.bookButtonAction)
        self.bookButton.grid(row=2, column=0, columnspan=2, pady=10)

        self.countLabel = CTkLabel(master=self, text="Количество: 0")
        self.countLabel.grid(row=2, column=1, columnspan=2, pady=10, padx=10, sticky="e")

        # Изначально обновляем интерфейс
        self.update_ui()

    def update_ui(self):
        """Обновляет интерфейс на основе текущего selectedBook."""
        # Получаем данные выбранной книги
        if len(self.controller.dataManager.booksDictionary) > 0:
            selected_book = self.controller.dataManager.booksDictionary[self.controller.dataManager.getSelectedBook()]

            # Обновляем обложку книги
            def update_cover():
                try:
                    self.bookCover.configure(url=selected_book.image, text="", compound="left")
                except:
                    self.bookCover.configure(text="Error: Check the network connection or the url specified.")

            Thread(target=update_cover).start()

            # Обновляем метаданные
            self.titleLabels.update_labels(selected_book)

            # Обновляем описание
            self.description.configure(text=selected_book.description)

            self.countLabel.configure(text=f"Количество: {selected_book.count}")

            if selected_book.count > 0:
                self.bookButton.configure(fg_color="#3669a1")
                self.bookButton.configure(hover_color="#12f")
            else:
                self.bookButton.configure(fg_color="gray")
                self.bookButton.configure(hover_color="#666")

    def bookButtonAction(self):
        selected = self.dataManager.booksDictionary[self.dataManager.getSelectedBook()]
        sql.DecreaseCount(selected.title, selected.author, selected.authorSurname, selected.image, selected.description,
                          selected.genre, selected.publisher, "1", "2", selected.count)
        messagebox.showerror("Успех", "Книга " + selected.title + " забронирована")

        self.dataManager.loadData()
        count = self.dataManager.booksDictionary[self.dataManager.getSelectedBook()].count
        if count <= 0:
            self.bookButton.configure(fg_color="gray")
        self.countLabel.configure(
            text=f"Количество: {count}")

    def open_append_window(self):
        self.controller.open_toplevel(
            AppendToplevelWindow, controller=self.controller
        )


class TitleLabels(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color="transparent")

        # Создаем виджеты для заголовков
        self.title = CTkLabel(self, text="")
        self.title.configure(font=('Helvetica bold', 25))
        self.title.grid(row=0, column=0, sticky="nsw")

        self.author = CTkLabel(self, text="")
        self.author.grid(row=1, column=0, sticky="nsw")

        self.genre = CTkLabel(self, text="")
        self.genre.grid(row=2, column=0, sticky="nsw")

        self.publisher = CTkLabel(self, text="")
        self.publisher.grid(row=3, column=0, sticky="nsw")

    def update_labels(self, book):
        """Обновляет текст метаданных книги."""
        self.title.configure(text=book.title)
        self.author.configure(text=book.author + " " + book.authorSurname)
        self.genre.configure(text=book.genre)
        self.publisher.configure(text=book.publisher)


class SidePanel(CTkFrame):
    def __init__(self, master, controller, dataManager, **kwargs):
        super().__init__(master, **kwargs)

        self.controller = controller
        self.controller.set_side_panel(self)

        self.dataManager = dataManager

        self.configure(corner_radius=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.title = CTkLabel(self, text="Библио-лаба", font=("MarkerFelt-Thin", 25))
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="new")

        self.searchBar = SearchBar(self, controller)
        self.searchBar.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        values = [(book, self.controller.dataManager.booksDictionary[book].title) for book in
                  self.controller.dataManager.booksDictionary.keys()]
        self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, controller, values=values)
        self.scrollable_checkbox_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")

        settingsImage = CTkImage(Image.open("Assets/settings.png"), size=(23, 23))
        self.settings = CTkButton(self, text="Настройки", image=settingsImage,
                                  text_color=("black", "white"),
                                  fg_color="transparent", hover_color=("#cfcfcf", "#333"),
                                  command=self.open_settings_window)
        self.settings.grid(padx=10, pady=5, sticky="ew")

    def open_settings_window(self):
        self.controller.open_toplevel(
            SettingsToplevelWindow, controller=self.controller, dataManager=self.dataManager
        )

    def update_scrollable_checkbox_frame(self):
        # Обновляем значения
        self.searchBar.searchEntry.configure(placeholder_text="Поиск")
        values = filter(lambda x: self.controller.dataManager.booksDictionary[x[0]].count != 0,
                        [(book, self.controller.dataManager.booksDictionary[book].title)
                         for book in self.controller.dataManager.booksDictionary.keys()])

        # Обновляем значения внутри существующего фрейма
        self.scrollable_checkbox_frame.update_values(values)


class SearchBar(CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.controller = controller

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
        search = self.searchEntry.get()
        values = filter(lambda x: self.controller.dataManager.booksDictionary[x[0]].count != 0 and
                        search.capitalize() in self.controller.dataManager.booksDictionary[x[0]].title.capitalize(),
                        [(book, self.controller.dataManager.booksDictionary[book].title)
                         for book in self.controller.dataManager.booksDictionary.keys()])

        # Обновляем значения внутри существующего фрейма
        self.master.scrollable_checkbox_frame.update_values(values)
