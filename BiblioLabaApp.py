from Views.LoginView import *


class BiblioLabaApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("Библио-Лаба")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login = LoginView(self)
        self.login.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.login.configure(fg_color="transparent")
        # self.main = MainPage(self.window)
        self.login.pack()

    def loop(self):
        self.mainloop()
