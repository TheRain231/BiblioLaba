from customtkinter import *
from Helpers.dataManager import *


class SettingsToplevelWindow(CTkToplevel):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = controller

        self.geometry("400x300")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.dropButton = CTkButton(self, text="Drop Database", command=self.dropButtonAction)
        self.dropButton.grid(row=1, column=1, sticky="nsew")

        self.updateButton = CTkButton(self, text="Update UI", command=self.updateButton)
        self.updateButton.grid(row=2, column=1, pady=10, sticky="nsew")

    def updateButton(self):
        self.controller.update_ui()

    def dropButtonAction(self):
        # selected = booksDictionary[selectedBook]
        # sql.DecreaseCount(selected.title, selected.author, selected.author, selected.image, selected.description, selected.genre, selected.publisher, "1", "2", selected.count)
        # self.controller.update_selected_book(booksDictionary.keys()[0])
        sql.DeleteDB()
        self.controller.update_side_panel()
