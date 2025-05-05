import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import markdown
from tkhtmlview import HTMLLabel

# Создаем главное окно
root = tk.Tk()
root.title("Simple Text (Markdown) text")

# Создаем текстовое поле
text = tk.Text(root)
text.grid(row=0, column=0, sticky="nsew")

# Настройка сетки для масштабирования текстового поля
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Функция для сохранения текста в файл
def save_as():
    global text
    content = text.get("1.0", "end-1c")
    file_location = filedialog.asksaveasfilename(
        defaultextension=".md",  # ← Здесь поменял на .md
        filetypes=[
            ("Markdown files", "*.md"),  # ← Приоритетный тип
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )
    if file_location:
        with open(file_location, "w", encoding="utf-8") as file:
            file.write(content)
            
# Функция для открытия файла
def open_as():
    file_location = filedialog.askopenfilename(
        filetypes=[
            ("Markdown files", "*.md"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )
    if file_location:
        with open(file_location, "r", encoding="utf-8") as file:
            content = file.read()
            text.delete("1.0", "end")
            text.insert("1.0", content)
            update_preview()

# Список доступных шрифтов
fonts = ["Helvetica", "Arial", "Courier", "Times New Roman", "Verdana", "Comic Sans MS"]
selected_font = tk.StringVar(value=fonts[0])

# Функции для изменения шрифта
def set_font_courier(selected_font):
    text.config(font=(selected_font, 12))  # Устанавливаем шрифт и размер 12

# Фрейм для кнопок
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

# Создаем HTML-предпросмотр
preview = HTMLLabel(root, html="<h1>Предпросмотр Markdown</h1>")
preview.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Обновление предпросмотра
def update_preview(event=None):
    md_text = text.get("1.0", "end-1c")
    html_content = markdown.markdown(md_text)
    preview.set_html(html_content)

text.bind("<<Modified>>", lambda e: (update_preview(), text.edit_modified(False)))

# Функции для форматирования текста
def apply_format(tag_start, tag_end):
    try:
        selection = text.get(tk.SEL_FIRST, tk.SEL_LAST)
        text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        text.insert(tk.INSERT, f"{tag_start}{selection}{tag_end}")
        update_preview()
    except tk.TclError:
        pass

def make_bold():
    apply_format("**", "**")

def make_italic():
    apply_format("*", "*")

def make_underline():
    apply_format("<u>", "</u>")

def make_header(level):
    try:
        selection = text.get(tk.SEL_FIRST, tk.SEL_LAST)
        text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        text.insert(tk.INSERT, f"{'#' * level} {selection}")
        update_preview()
    except tk.TclError:
        pass

# Кнопки
open_button = tk.Button(button_frame, text="Открыть", command=open_as)
save_button = tk.Button(button_frame, text="Сохранить", command=save_as)
bold_button = tk.Button(button_frame, text="Жирный", command=make_bold)
italic_button = tk.Button(button_frame, text="Курсив", command=make_italic)
underline_button = tk.Button(button_frame, text="Подчеркнуть", command=make_underline)
# Выпадающий список для выбора шрифта
font_dropdown = tk.OptionMenu(button_frame, selected_font, *fonts, command=set_font_courier)

header1_button = tk.Button(button_frame, text="H1", command=lambda: make_header(1))
header2_button = tk.Button(button_frame, text="H2", command=lambda: make_header(2))
header3_button = tk.Button(button_frame, text="H3", command=lambda: make_header(3))
font_dropdown.grid(row=0, column=8, padx=2, pady=2)


# Расположение кнопок
open_button.grid(row=0, column=0, padx=2, pady=2)
save_button.grid(row=0, column=1, padx=2, pady=2)
bold_button.grid(row=0, column=2, padx=2, pady=2)
italic_button.grid(row=0, column=3, padx=2, pady=2)
underline_button.grid(row=0, column=4, padx=2, pady=2)
header1_button.grid(row=0, column=5, padx=2, pady=2)
header2_button.grid(row=0, column=6, padx=2, pady=2)
header3_button.grid(row=0, column=7, padx=2, pady=2)

# Запуск главного цикла
root.mainloop()
