from customtkinter import *


class SettingsToplevelWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)


        self.dropButton = CTkButton(self, text="Drop Database", command=self.dropButtonAction)
        self.dropButton.grid(row=1, column=1, sticky="nsew")

    def dropButtonAction(self):
        print("dropped")
