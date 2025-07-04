# Инструмент сравнения логов сборки

Консольное приложение на Python для сравнения логов сборки C/C++ проектов с игнорированием различий во времени сборки и путях к файлам.

---

## Описание

Скрипт предназначен для сравнения логов сборки проектов, написанных на C/C++, которые создаются с помощью утилит **make** или **CMake**. Логи сборки могут различаться только по времени и месту выполнения сборки, поэтому приложение нормализует временные метки и пути к файлам, заменяя их на стандартный плейсхолдер (`/path/`).

Если после нормализации логи отличаются только по временным меткам и путям, скрипт выводит сообщение:

```
Файлы отличаются только временем и местом сборки.
```

В противном случае, выводится подробный дифф в формате, похожем на стандартную утилиту `diff` в Unix-системах, с подсветкой добавленных и удалённых строк.

---

## Обзор кода

**Функция normalize_log(log_content):**  
- **Назначение:** Нормализует содержимое логов, удаляя временные метки и заменяя пути к файлам на стандартный плейсхолдер (`/path/`), что позволяет игнорировать различия, не влияющие на суть сборки.  
- **Реализация:**  
  - Удаляются все строки, соответствующие формату временных меток `DD-MM-YYYY HH:MM:SS` с помощью регулярного выражения.  
  - Применяются регулярные выражения для поиска и замены Linux-подобных путей и Windows-путей на строку `/path/`.

**Функция compare_logs(file1, file2):**  
- **Назначение:** Сравнивает два лог-файла после нормализации их содержимого.  
- **Реализация:**  
  - Чтение файлов построчно с использованием модуля `pathlib` для работы с путями.  
  - Применение функции `normalize_log` к каждой строке обоих логов.  
  - Если нормализованные логи идентичны, выводится сообщение:  
    ```
    Файлы отличаются только временем и местом сборки.
    ```  
  - Если обнаружены отличия, используется функция `unified_diff` из модуля `difflib` для формирования подробного диффа, где:  
    - Строки с добавлениями выводятся зелёным цветом.  
    - Строки с удалениями — красным.  
    - Служебные строки (например, номера строк) — голубым.

**Константы:**  
- `TIMESTAMP_FORMAT`: определён как `'%d-%m-%Y %H:%M:%S'` и служит для документирования формата временных меток в логах.

---

## Начало работы

### Требования

- **Python 3.6+**
- **Устанавливаемые библиотеки:**
  - `colorama` (для установки: `pip install colorama`)
- Стандартные библиотеки: `re`, `sys`, `pathlib`, `difflib` (устанавливаются вместе с Python)

### Установка

1. Скачайте или клонируйте репозиторий с файлом `myscript.py` и данным `readme.md`.
2. Установите необходимые библиотеки.

### Использование

Запустите скрипт из командной строки, передав два пути к лог файлам в качестве аргументов:

```bash
python3 myscript.py <путь/к/файлу1> <путь/к/файлу2>
```

