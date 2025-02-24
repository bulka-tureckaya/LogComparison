import re
import sys
from pathlib import Path
from difflib import unified_diff
from colorama import Fore, Style, init

# Инициализация colorama
init()

# Константа для формата даты/времени
TIMESTAMP_FORMAT = '%d-%m-%Y %H:%M:%S'

def normalize_log(log_content):
    # Удаление временных меток и путей
    log_content = re.sub(r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}', '', log_content)

    # Замена Linux-подобных путей
    log_content = re.sub(r'(?<!\w)(?:[\w\-.]+/)+[\w\-.]+', '/path/', log_content)
    
    # Замена Windows-путей
    log_content = re.sub(r'[A-Za-z]:\\(?:[\w \-.]+\\)+[\w \-.]+', '/path/', log_content)
    return log_content

def compare_logs(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        log1 = f1.readlines()
        log2 = f2.readlines()

        # Нормализация строк
        normalized_log1 = [normalize_log(line) for line in log1]
        normalized_log2 = [normalize_log(line) for line in log2]

        if normalized_log1 == normalized_log2:
            print(Fore.GREEN + "Файлы отличаются только временем и местом сборки." + Style.RESET_ALL)
            return

        # Использую unified_diff для сравнения
        diff = unified_diff(normalized_log1, normalized_log2, fromfile=str(file1), tofile=str(file2), lineterm='')

        # Вывод различий с цветами
        for line in diff:
            if line.startswith('+'):
                print(Fore.GREEN + line + Style.RESET_ALL)  # Добавленные строки
            elif line.startswith('-'):
                print(Fore.RED + line + Style.RESET_ALL)    # Удалённые строки
            elif line.startswith('@'):
                print(Fore.CYAN + line + Style.RESET_ALL)  # Служебные строки
            else:
                print(line)  # Обычные строки

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python3 myscript.py <файл1> <файл2>")
        sys.exit(1)

    file1 = Path(sys.argv[1])
    file2 = Path(sys.argv[2])

    if not file1.exists() or not file2.exists():
        print("Один из файлов не существует.")
        sys.exit(1)

    compare_logs(file1, file2)