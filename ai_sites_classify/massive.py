import ast
import FreeSimpleGUI as sg
import webbrowser

sg.theme('DarkGrey13') # Установка темы

def search_array(array, search_terms):
    if not search_terms:
        return array

    search_terms = search_terms.split()
    results = []
    for item in array:
        item_str = str(item)
        if all(term in item_str for term in search_terms):
            results.append(item)
    return results

def go_to(url):
    webbrowser.open(url)

def delete_from_array(array):
    """Создает GUI для удаления элементов из массива с поиском."""

    if not isinstance(array, list):
        return "Ошибка: Входные данные должны быть списком."

    if not array:
        return "Ошибка: Массив пуст."

    # Layout с поиском и шрифтом
    layout = [
        [sg.Text("Поиск:", font='Helvetica 12 bold'), sg.InputText(key='-SEARCH-', do_not_clear=True, font='Helvetica 12 bold', size=(23,1)), sg.Button('Найти', font='Helvetica 12 bold')],
        [sg.Table(values=[[str(x)] for x in array], headings=['Элемент'],
                  auto_size_columns=False, col_widths=[30], key='-TABLE-',
                  enable_events=True, select_mode=sg.TABLE_SELECT_MODE_EXTENDED, font='Helvetica 12 bold')],
        [sg.Button('Удалить', font='Helvetica 12 bold'), sg.Button('Отмена', font='Helvetica 12 bold'), sg.Button('Открыть', font='Helvetica 12 bold')]
    ]

    window = sg.Window('Удаление элементов', layout, font='Helvetica 12 bold')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Отмена':
            break
        if event == 'Найти':
            search_terms = values['-SEARCH-']
            filtered_array = search_array(array, search_terms)
            window['-TABLE-'].update(values=[[str(x)] for x in filtered_array])

        if event == 'Удалить':
            selected_indices = values['-TABLE-']
            if selected_indices:
                new_array = [array[i] for i in range(len(array)) if i not in selected_indices]
                window.close()
                return new_array
            else:
                sg.popup("Ошибка: Не выбрано ни одного элемента для удаления.", font='Helvetica 12 bold') # Добавил шрифт
                window['-TABLE-'].update(values=[[str(x)] for x in array]) #Возврат к исходному
        if event == 'Открыть':
            selected_indices = values['-TABLE-']
            if selected_indices:
                selected_values = [array[i] for i in selected_indices]
                print(selected_values)
                for selected_value in selected_values:
                    go_to(selected_value)
            else:
                sg.popup("Ошибка: Не выбрано ни одного элемента для удаления.", font='Helvetica 12 bold') # Добавил шрифт
                window['-TABLE-'].update(values=[[str(x)] for x in array]) #Возврат к исходному
    window.close()
    return None



def edit_array(array_input):
    # Пример использования (с обработкой исключений):
    try:
        result = delete_from_array(array_input)
        if isinstance(result, list):
            #print("Обновленный массив:", result)
            return result
        elif isinstance(result, str):
            print(result)
        else:
            print("Операция отменена.")
        return result
    except (ValueError, SyntaxError) as e:
        print(f"Ошибка при разборе ввода: {e}")
    except Exception as e:
        print(f"Произошла неизвестная ошибка: {e}")