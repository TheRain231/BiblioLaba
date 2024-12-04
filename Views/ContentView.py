from customtkinter import *


class ContentView(CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.controller = controller

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=10)

        self.sidePanel = SidePanel(self)
        self.sidePanel.grid(row=0, column=0, pady=10, sticky="w")


class SidePanel(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, **kwargs)

        self.welcome = CTkLabel(self, text="Добро пожаловать!", font=("arial", 30))
        self.welcome.pack(padx=10, pady=20)
