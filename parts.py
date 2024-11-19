import os
import re
import codecs

def process_files(directory):
    """
    Reads all .cs files in a directory and its subdirectories,
    extracts code blocks, and writes them to a file.

    Args:
        directory: The directory to process.
    """
    try:
        all_code = ""
        for root, _, files in os.walk(directory):
            for file in files:
                if True:
                    filepath = os.path.join(root, file)
                    try:
                        with codecs.open(filepath, 'r', encoding='utf-8', errors='replace') as f:  # Обработка ошибок кодировки
                            content = f.read()
                            all_code += f"Название: {file}\n{content}\n\n"
                    except UnicodeDecodeError as e:
                        print(f"Ошибка декодирования файла {filepath}: {e}")
                        continue  # Пропускаем файл, если не удалось декодировать
        if all_code:
            with codecs.open("des.txt", 'w', encoding='utf-8', errors='replace') as outfile:  # Обработка ошибок кодировки
                outfile.write(all_code)
            print("Данные успешно записаны в des.txt")
        else:
            print("В директории не найдено ни одного файла .cs")


    except FileNotFoundError:
        print(f"Директория {directory} не найдена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    directory_to_process = "MalumMenu"  # Укажите точный путь
    process_files(directory_to_process)