import glob
import os
def save_memory(nick, memory, erase):
    try:
        if erase:
            print(f"Стереть = Да, пытаемся записать в память о {nick} {memory}")
            with open(f"memories/{nick}.txt", 'w') as file:
                file.write(str(memory))
                return "OK"
        else:
            try:
                with open(f"memories/{nick}.txt", 'r') as file:
                    context = file.read()
            except Exception as e:
                print("error handled")
                context = ""
            with open(f"memories/{nick}.txt", 'w') as file:
                file.write(f"{context};  {str(memory)}")
                return "OK"
    except Exception as e:
        return e
def all_memories():
    memory_files = glob.glob('memories/*.txt')  # Получаем все .txt файлы в каталоге
    memory_files_names = [os.path.basename(file)[:-4] for file in memory_files]  # Получаем названия без расширения
    return memory_files_names
def erase_memory(list):
    is_clean = 0
    for el in list:
        res = save_memory(el, "", True)
        if res.startswith("error"):
            print(f"couldnt erase: {el}"),
            is_clean -=1
        else: is_clean +=1
    if is_clean >0: return "OK"
def get_few_memories(file_list):
    memories = {}
    memory_folder = 'memories/'

    for filename in file_list:
        file_path = os.path.join(memory_folder, f"{filename}.txt")
        if os.path.isfile(file_path):  # Проверяем, существует ли файл
            with open(file_path, 'r') as file:
                content = file.read()  # Читаем содержимое файла
                memories[filename] = content  # Добавляем в словарь с именем файла как ключ

    return memories
def load_memory(nick):
    try:
        with open(f"memories/{nick}.txt", 'r') as file:
            return str(file.read())
    except Exception as e:
        return ""
