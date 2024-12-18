from Views.ContentView import *
from tkinter import messagebox

USER = "tester"
PASSWORD = "12345"


class LoginView(CTkFrame):
    def __init__(self, master, controller, dataManager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.controller = controller
        self.dataManager = dataManager

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)

        self.welcome = CTkLabel(self, text="Добро пожаловать!", font=("arial", 30))
        self.welcome.grid(row=0, column=1, pady=100)

        self.entries = LoginEntries(self, controller, dataManager)
        self.entries.grid(row=1, column=1, padx=10, pady=10, sticky="new")


class LoginEntries(CTkFrame):
    def __init__(self, master, controller, dataManager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.controller = controller
        self.dataManager = dataManager

        self.loginEntry = CTkEntry(self, placeholder_text="Логин", width=300)
        self.loginEntry.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="n")
        self.loginEntry.bind('<Return>', self.selectNext)

        self.passwordEntry = CTkEntry(self, placeholder_text="Пароль", width=300, show='*')
        self.passwordEntry.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w")
        self.passwordEntry.bind('<Return>', self.loginCommand)

        self.radio_var = IntVar(value=1)
        self.radio = CTkRadioButton(self, text="Вход",
                                    variable=self.radio_var, value=1)
        self.radio2 = CTkRadioButton(self, text="Регистрация",
                                     variable=self.radio_var, value=2)
        self.radio.grid(row=2, column=0, padx=10, pady=10, sticky="")
        self.radio2.grid(row=2, column=1, padx=10, pady=10, sticky="")

        self.button = CTkButton(self, text="Войти", command=self.loginButtonAction)
        self.button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="")

        self.loginEntry.insert(0, USER)
        self.passwordEntry.insert(0, PASSWORD)

    def loginButtonAction(self):
        self.loginCommand()

    def loginCommand(self, event=None):
        login = self.loginEntry.get()
        password = self.passwordEntry.get()
        # Log in
        if self.radio_var.get() == 1:
            clients = sql.TakeDataClient()

            flag = False
            for (idd, loginn, passwordd) in clients:
                if login == loginn:
                    flag = True
                    if password == passwordd:
                        self.dataManager.login = login
                        self.dataManager.password = password
                        self.controller.show_view(ContentView)
                        print("pass")
                        break
                    else:
                        messagebox.showerror("Ошибка", "Неверный пароль!")
            if not flag:
                messagebox.showerror("Ошибка", "Такого пользователя не существут")

        # Registration
        elif self.radio_var.get() == 2:
            if validate(login) and validate(password):
                if sql.Registration(login, password):
                    print("pass")
                    self.dataManager.login = login
                    self.dataManager.password = password
                    self.controller.show_view(ContentView)
                else:
                    messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует")
            else:
                messagebox.showerror("Ошибка", "Логин или пароль не введен или содержит символы")

    def selectNext(self, event=None):
        self.passwordEntry.focus_set()


def validate(word):
    if len(word) < 1 or len(word) > 20:
        return False
    # Проверяем, состоит ли логин только из букв и цифр
    for char in word:
        if not char.isalnum():
            return False
    return True
