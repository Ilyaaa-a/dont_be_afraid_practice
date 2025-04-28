import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk 

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
fonts = ["Helvetica", "Arial", "Courier", "Times New Roman", "Verdana", "Comic Sans MS"]
selected_font = tk.StringVar(value=fonts[0])

def set_font_courier():
    global text
    text.config(font=("Courier", 12))

def update_font():
    text.config(font=(selected_font.get(), 12))

font_selector = ttk.Combobox(
    root,
    textvariable=selected_font,
    values=fonts,
    state='readonly'
)
font_selector.grid(row=2, column=0, sticky="ew")
font_selector.bind("<<ComboboxSelected>>", lambda e: update_font())

# Запуск главного цикла
root.mainloop()