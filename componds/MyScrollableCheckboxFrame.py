from customtkinter import CTkScrollableFrame, CTkButton
from Helpers.dataManager import *


class MyScrollableCheckboxFrame(CTkScrollableFrame):
    def __init__(self, master, controller, values):
        super().__init__(master)

        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in self.values:
            checkbox = CTkButton(self, text=value,
                                 fg_color="grey",
                                 hover_color="#666666",
                                 command=lambda index=i: self.select_book(index))

            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="ew")
            self.checkboxes.append(checkbox)

    def select_book(self, index):
        # Обновляем выбранный элемент
        self.controller.update_selected_book(index)
        print(self.controller.dataManager.getSelectedBook())

    def update_values(self, values):
        # Очищаем предыдущие виджеты
        for widget in self.winfo_children():
            widget.destroy()

        self.values = values
        self.checkboxes = []

        # Создаём новые кнопки
        for i, value in self.values:
            checkbox = CTkButton(self, text=value,
                                 fg_color="grey",
                                 hover_color="#666666",
                                 command=lambda index=i: self.select_book(index))

            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="ew")
            self.checkboxes.append(checkbox)
