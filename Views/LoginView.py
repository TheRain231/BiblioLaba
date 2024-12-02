from Views.ContentView import *

USER = "tester"
PASSWORD = "12345"


class LoginView(CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.controller = controller

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.welcome = CTkLabel(self, text="Добро пожаловать!", font=("arial", 30))
        self.welcome.grid(row=0, column=0, pady=100)

        self.entries = LoginEntries(self)
        self.entries.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


class LoginEntries(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.loginEntry = CTkEntry(self, placeholder_text="Логин", width=300)
        self.loginEntry.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="n")
        self.loginEntry.bind('<Return>', self.selectNext)

        self.passwordEntry = CTkEntry(self, placeholder_text="Пароль", width=300, show='*')
        self.passwordEntry.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.passwordEntry.bind('<Return>', self.loginCommand)

        self.button = CTkButton(self, text="Войти", command=self.loginButtonAction)
        self.button.grid(row=2, column=0, padx=10, pady=10, sticky="")

    def loginButtonAction(self):
        self.loginCommand()

    def loginCommand(self, event=None):
        if self.loginEntry.get() == USER and self.passwordEntry.get() == PASSWORD:
            print("pass")
            self.master.controller.show_view(ContentView)
        else:
            print("not pass")

    def selectNext(self, event=None):
        self.passwordEntry.focus_set()
