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
        self.grid_rowconfigure(4, weight=1)

        self.dropButton = CTkButton(self, text="Drop Database", command=self.dropButtonAction)
        self.dropButton.grid(row=1, column=1, sticky="nsew")

        self.updateButton = CTkButton(self, text="Update UI", command=self.updateButtonAction)
        self.updateButton.grid(row=3, column=1, pady=10, sticky="nsew")

    def updateButtonAction(self):
        self.controller.update_ui()

    def dropButtonAction(self):
        sql.DeleteDB()
        self.controller.update_side_panel()
