from customtkinter import *
import time


class AppendToplevelWindow(CTkToplevel):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = controller

        self.geometry("400x400")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=0)

        self.titleEntry = CTkEntry(self, placeholder_text="Название")
        self.authorEntry = CTkEntry(self, placeholder_text="Автор")
        self.genreEntry = CTkEntry(self, placeholder_text="Жанр")
        self.publisherEntry = CTkEntry(self, placeholder_text="Издательство")
        self.coverEntry = CTkEntry(self, placeholder_text="Обложка")
        self.descriptionEntry = CTkEntry(self, placeholder_text="Описание")

        self.titleEntry.grid(padx=10, pady=5, columnspan=2, sticky="ew")
        self.authorEntry.grid(padx=10, pady=5, columnspan=2, sticky="ew")
        self.genreEntry.grid(padx=10, pady=5, columnspan=2, sticky="ew")
        self.publisherEntry.grid(padx=10, pady=5, columnspan=2, sticky="ew")
        self.coverEntry.grid(padx=10, pady=5, columnspan=2, sticky="ew")
        self.descriptionEntry.grid(row=6, padx=10, pady=5, columnspan=2, sticky="nsew")

        self.counter = CTkButton(self, text="Append", command=self.appendButtonAction)
        self.counter.grid(row=7, column=0, padx=10, pady=5, sticky="sw")

        self.counter = Counter(self)
        self.counter.grid(row=7, column=1, padx=10, pady=5, sticky="se")

    def appendButtonAction(self):
        self.controller.dataManager.insertNewBook(title=self.titleEntry.get(),
                                                  authorName=self.authorEntry.get(),
                                                  genre=self.genreEntry.get(),
                                                  publishngHouseLabel=self.publisherEntry.get(),
                                                  image=self.coverEntry.get(),
                                                  description=self.descriptionEntry.get(),
                                                  count=self.counter.getCount())
        self.controller.update_ui()
        self.controller.close_toplevel(AppendToplevelWindow)


class Counter(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.decreaseButton = CTkButton(self, text="-", command=self.decrease, width=25)
        self.counterLabel = CTkLabel(self, text="1", width=80)
        self.increaseButton = CTkButton(self, text="+", command=self.increase, width=25)

        self.decreaseButton.grid(row=0, column=0)
        self.counterLabel.grid(row=0, column=1)
        self.increaseButton.grid(row=0, column=2)

    def decrease(self):
        if int(self.counterLabel.cget("text")) > 1:
            self.counterLabel.configure(text=str(int(self.counterLabel.cget("text")) - 1))

    def increase(self):
        self.counterLabel.configure(text=str(int(self.counterLabel.cget("text")) + 1))

    def getCount(self):
        return int(self.counterLabel.cget("text"))
