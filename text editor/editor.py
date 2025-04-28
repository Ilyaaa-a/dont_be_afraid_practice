import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import Menu

# Создаем главное окно
root = tk.Tk()
root.title("Simple Text Editor")

# Создаем текстовое поле
text = tk.Text(root)
text.grid(row=0, column=0, sticky="nsew")

# Настройка сетки для масштабирования текстового поля
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Функция для сохранения текста в файл
def save_as():
    global text
    content = text.get("1.0", "end-1c")  # Получаем текст из текстового поля
    file_location = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_location:  # Если пользователь выбрал файл
        with open(file_location, "w") as file:
            file.write(content)

# Кнопка для сохранения файла
save_button = tk.Button(root, text="Save", command=save_as)
save_button.grid(row=1, column=0, sticky="ew")

# Функции для изменения шрифта
def set_font_helvetica():
    global text
    text.config(font=("Helvetica", 12))

def set_font_courier():
    global text
    text.config(font=("Courier", 12))

# Создаем меню для выбора шрифта
font_menu = Menu(root, tearoff=0)
font_menu.add_command(label="Helvetica", command=set_font_helvetica)
font_menu.add_command(label="Courier", command=set_font_courier)

# Кнопка для открытия меню шрифтов
font_button = tk.Menubutton(root, text="Font", menu=font_menu)
font_button.grid(row=2, column=0, sticky="ew")

# Запуск главного цикла
root.mainloop()
