+++
date = '2025-03-18T12:30:45+03:00'
draft = false
title = 'Создание и модификация текстового редактора.'
description = 'Туториал'
image = ''
tags = ["Анализ"]
+++

# Создание и модификация текстового редактора

## Введение

В этом туториале мы создадим простой текстовый редактор, поддерживающий форматирование Markdown. Мы научимся работать с библиотекой tkinter для создания графического интерфейса и интегрируем поддержку Markdown с помощью библиотеки markdown. Этот проект включает функциональность сохранения, открытия файлов, предпросмотра Markdown и различных инструментов для форматирования текста.

---

## Исследование предметной области

Для создания текстового редактора нам потребуется изучить следующие концепции:
- **Tkinter**: Библиотека Python для создания графических интерфейсов.
- **Markdown**: Легкий язык разметки для форматирования текста.
- **Файловые операции**: Чтение и запись файлов на диск.


## Подготовка к работе

1. Установите Python (версия 3.6 или выше).
2. Установите необходимые библиотеки:
   
```bash
   pip install markdown tkhtmlview
```

3. Создайте новый файл с названием text_editor.py.

---

## Практическая реализация


### Шаг 1: Создание окна

```python
import tkinter as tk  # Импорт библиотеки для создания графического интерфейса

root = tk.Tk()  # Создаем главное окно приложения
root.title("Simple Text (Markdown) Editor")  # Устанавливаем заголовок окна

# Создаем текстовое поле, куда пользователь будет вводить текст
text = tk.Text(root)
text.grid(row=0, column=0, sticky="nsew")  # Размещаем текстовое поле и растягиваем его по окну

# Настройка сетки: делаем текстовое поле адаптивным по размеру окна
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()  # Запускаем главный цикл окна — программа будет ждать действий пользователя
```

> ✅ *Этот код создает базовое окно с возможностью ввода текста. Оно ещё не умеет сохранять или открывать файлы.*

---

### Шаг 2: Сохранение и открытие файлов

```python
from tkinter import filedialog  # Импорт модуля для открытия и сохранения файлов

def save_as():
    # Получаем весь текст от первой строки до последнего символа (без последнего переноса строки)
    content = text.get("1.0", "end-1c")
    
    # Открываем диалог сохранения файла
    file_location = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    # Если пользователь выбрал место для сохранения
    if file_location:
        # Сохраняем текст в выбранный файл
        with open(file_location, "w") as file:
            file.write(content)

def open_as():
    # Открываем диалог выбора файла
    file_location = filedialog.askopenfilename(
        filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
    )
    if file_location:
        # Читаем содержимое файла и вставляем его в текстовое поле
        with open(file_location, "r", encoding="utf-8") as file:
            content = file.read()
            text.delete("1.0", "end")  # Очищаем текстовое поле
            text.insert("1.0", content)  # Вставляем содержимое
```

**Кнопки для вызова функций:**

```python
button_frame = tk.Frame(root)  # Создаем отдельную панель (фрейм) для кнопок
button_frame.grid(row=1, column=0, sticky="ew")  # Размещаем панель под текстовым полем

# Кнопки для открытия и сохранения
open_button = tk.Button(button_frame, text="Открыть", command=open_as)
save_button = tk.Button(button_frame, text="Сохранить", command=save_as)

# Размещаем кнопки в строку
open_button.grid(row=0, column=0, padx=2, pady=2)
save_button.grid(row=0, column=1, padx=2, pady=2)
```

> ✅ *Теперь мы можем открывать и сохранять файлы — удобно для работы с текстом.*

---

### Шаг 3: Предпросмотр Markdown

```python
from tkhtmlview import HTMLLabel  # Импорт виджета для отображения HTML
import markdown  # Библиотека преобразует Markdown в HTML

# Создаем виджет для предпросмотра HTML
preview = HTMLLabel(root, html="<h1>Предпросмотр Markdown</h1>")
preview.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Функция для обновления предпросмотра
def update_preview(event=None):
    md_text = text.get("1.0", "end-1c")  # Получаем текущий текст
    html_content = markdown.markdown(md_text)  # Преобразуем Markdown в HTML
    preview.set_html(html_content)  # Отображаем HTML в правой части окна

# Привязываем обновление предпросмотра к событию изменения текста
text.bind("<<Modified>>", lambda e: (update_preview(), text.edit_modified(False)))
```

> ✅ *Теперь каждое изменение в текстовом поле автоматически отображается справа в виде HTML-версии Markdown.*

---

### Шаг 4: Форматирование текста

```python
# Общая функция применения форматирования
def apply_format(tag_start, tag_end):
    try:
        # Получаем выделенный текст
        selection = text.get(tk.SEL_FIRST, tk.SEL_LAST)
        text.delete(tk.SEL_FIRST, tk.SEL_LAST)  # Удаляем его
        # Вставляем с нужным Markdown-обрамлением
        text.insert(tk.INSERT, f"{tag_start}{selection}{tag_end}")
        update_preview()
    except tk.TclError:
        # Если ничего не выделено — ничего не делаем
        pass

# Частные функции форматирования
def make_bold():
    apply_format("**", "**")  # **жирный**

def make_italic():
    apply_format("*", "*")  # *курсив*

def make_underline():
    apply_format("<u>", "</u>")  # HTML-тег <u>

def make_header(level):
    try:
        selection = text.get(tk.SEL_FIRST, tk.SEL_LAST)
        text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        text.insert(tk.INSERT, f"{'#' * level} {selection}")  # # Заголовок
        update_preview()
    except tk.TclError:
        pass
```

**Кнопки для форматирования:**

```python
bold_button = tk.Button(button_frame, text="Жирный", command=make_bold)
italic_button = tk.Button(button_frame, text="Курсив", command=make_italic)
underline_button = tk.Button(button_frame, text="Подчеркнуть", command=make_underline)

header1_button = tk.Button(button_frame, text="H1", command=lambda: make_header(1))
header2_button = tk.Button(button_frame, text="H2", command=lambda: make_header(2))
header3_button = tk.Button(button_frame, text="H3", command=lambda: make_header(3))

bold_button.grid(row=0, column=2, padx=2, pady=2)
italic_button.grid(row=0, column=3, padx=2, pady=2)
underline_button.grid(row=0, column=4, padx=2, pady=2)
header1_button.grid(row=0, column=5, padx=2, pady=2)
header2_button.grid(row=0, column=6, padx=2, pady=2)
header3_button.grid(row=0, column=7, padx=2, pady=2)
```

> ✅ *Теперь можно выделить текст и сделать его жирным, курсивным, заголовком и т. п. — как в обычных редакторах.*

---

### Шаг 5: Выбор шрифта

```python
# Список доступных шрифтов
fonts = ["Helvetica", "Arial", "Courier", "Times New Roman", "Verdana", "Comic Sans MS"]
selected_font = tk.StringVar(value=fonts[0])  # Переменная для хранения выбранного шрифта

# Функция для изменения шрифта текста
def set_font_courier(selected_font):
    text.config(font=(selected_font, 12))  # Устанавливаем шрифт и размер

# Выпадающее меню со шрифтами
font_dropdown = tk.OptionMenu(button_frame, selected_font, *fonts, command=set_font_courier)
font_dropdown.grid(row=0, column=8, padx=2, pady=2)
```

> ✅ *Пользователь может выбрать удобный шрифт — удобно для визуального восприятия.*

---

## Модификация проекта

Мы добавили:
- Поддержку Markdown.
- Предпросмотр Markdown.
- Инструменты для форматирования текста.

---

## Заключение

Мы создали простой текстовый редактор Markdown с возможностью сохранения, открытия файлов, предпросмотра и форматирования текста. 

---

## Итоговый код

```python
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
    content = text.get("1.0", "end-1c")  # Получаем текст из текстового поля
    file_location = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_location:  # Если пользователь выбрал файл
        with open(file_location, "w") as file:
            file.write(content)

# Функция для открытия файла
def open_as():
    file_location = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
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
```
