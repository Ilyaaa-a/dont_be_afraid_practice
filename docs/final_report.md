# Финальный отчёт по проекту «Markdown-редактор»

## Хронология этапов работы

### 1. Исследование предметной области
- Анализ возможностей библиотеки **Tkinter** для создания графического интерфейса
- Изучение синтаксиса **Markdown** и способов его преобразования в HTML
- Сравнение библиотек для отображения HTML в Tkinter (выбрана `tkhtmlview`)

### 2. Подготовка окружения
  Установка зависимостей:
  ```bash
  pip install markdown tkhtmlview
````

* Настройка структуры проекта
* Создание базового файла `text_editor.py`

### 3. Разработка базового функционала

* Создание главного окна приложения:

  ```python
  root = tk.Tk()
  root.title("Simple Text (Markdown) text")
  ```
* Реализация текстового поля с адаптивным размещением:

  ```python
  text = tk.Text(root)
  text.grid(row=0, column=0, sticky="nsew")
  ```

### 4. Работа с файлами

* Функция сохранения:

  ```python
  def save_as():
    global text
    content = text.get("1.0", "end-1c")
    file_location = filedialog.asksaveasfilename(
        defaultextension=".md",
        filetypes=[
            ("Markdown files", "*.md"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )
    if file_location:
        with open(file_location, "w", encoding="utf-8") as file:
            file.write(content)
  ```
* Функция открытия:

  ```python
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
  ```
* Добавлены кнопки для открытия и сохранения файлов

  ```python
  open_button = tk.Button(button_frame, text="Открыть", command=open_as)
  save_button = tk.Button(button_frame, text="Сохранить", command=save_as)

  open_button.grid(row=0, column=0, padx=2, pady=2)
  save_button.grid(row=0, column=1, padx=2, pady=2)
  ```

### 5. Система предпросмотра Markdown

* Использование `HTMLLabel` для отображения HTML:

  ```python
  import markdown
  from tkhtmlview import HTMLLabel

  preview = HTMLLabel(root, html="<h1>Предпросмотр Markdown</h1>")
  ```
* Функция автоматического обновления:

  ```python
  def update_preview(event=None):
    md_text = text.get("1.0", "end-1c")
    html_content = markdown.markdown(md_text)
    preview.set_html(html_content)
    
    text.bind("<<Modified>>", lambda e: (update_preview(), text.edit_modified(False)))
  ```
* Реализован двупанельный интерфейс

### 6. Инструменты форматирования

* Универсальная функция:

  ```python
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
  ```
* Отдельные кнопки для:

 ```python
bold_button = tk.Button(button_frame, text="Жирный", command=make_bold) # жирного
italic_button = tk.Button(button_frame, text="Курсив", command=make_italic) # курсива
underline_button = tk.Button(button_frame, text="Подчеркнуть", command=make_underline) # подчеркнутого
header1_button = tk.Button(button_frame, text="H1", command=lambda: make_header(1)) # заголовков
header2_button = tk.Button(button_frame, text="H2", command=lambda: make_header(2))
header3_button = tk.Button(button_frame, text="H3", command=lambda: make_header(3))
  ```

* Расположение кнопок форматирования
  
 ```python
bold_button.grid(row=0, column=2, padx=2, pady=2) # жирного
italic_button.grid(row=0, column=3, padx=2, pady=2) # курсива
underline_button.grid(row=0, column=4, padx=2, pady=2) # подчеркнутого
header1_button.grid(row=0, column=5, padx=2, pady=2) # заголовков
header2_button.grid(row=0, column=6, padx=2, pady=2)
header3_button.grid(row=0, column=7, padx=2, pady=2)
 ```

### 7. Дополнительные функции

* Выбор шрифта через выпадающий список

  ```python
  fonts = ["Helvetica", "Arial", "Courier", "Times New Roman", "Verdana", "Comic Sans MS"]
  selected_font = tk.StringVar(value=fonts[0])

  def set_font_courier(selected_font):
    text.config(font=(selected_font, 12))  # Устанавливаем шрифт и размер 12

  font_dropdown = tk.OptionMenu(button_frame, selected_font, *fonts, command=set_font_courier)

  font_dropdown.grid(row=0, column=8, padx=2, pady=2)


  ```
* Автоматическое обновление предпросмотра при изменении текста:

  ```python
  def update_preview(event=None):
    md_text = text.get("1.0", "end-1c")
    html_content = markdown.markdown(md_text)
    preview.set_html(html_content)
    
    text.bind("<<Modified>>", lambda e: (update_preview(), text.edit_modified(False)))

  ```


## Индивидуальные планы участников

### Комарова Алиса Алексеевна — интерфейс и базовая логика

1. Проектирование интерфейса в Tkinter
2. Создание главного окна и текстового поля
3. Реализация работы с файлами
4. Внедрение выбора шрифта
5. Тестирование и отладка

### Конарев Илья Александрович — Markdown и предпросмотр

1. Обработка Markdown
2. Реализация панели предпросмотра
3. Функции форматирования
4. Кнопки форматирования и панель быстрого доступа
5. Тестирование и отладка

---

## Итоговый функционал

**Markdown-редактор с предпросмотром**, включающий:

* Двупанельный интерфейс (редактирование + HTML-предпросмотр)
* Основные элементы форматирования:
  * Заголовки H1, H2, H3
  * Жирный, курсив, подчёркнутый текст
* Выбор из 6 шрифтов
* Работа с `.md` файлами
* Автоматическое обновление предпросмотра
* Удобный, минималистичный интерфейс

[Исходный код][editor.py]
[Видеопрезентация работы][video_p.mp4]
