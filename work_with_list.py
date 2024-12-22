import FreeSimpleGUI as sg
import pickle

# Загружаем данные
with open('chat_history_edit.pkl', 'rb') as cs:
    raw_data = pickle.load(cs)

# Преобразуем данные в нужный формат
data = []
for item in raw_data:
    if hasattr(item, 'role') and hasattr(item, 'parts'):
        # Если parts это объект с атрибутом text
        if hasattr(item.parts, 'text'):
            data.append({
                'role': str(item.role),
                'parts': str(item.parts.text)
            })
        # Если parts это список
        elif isinstance(item.parts, list):
            data.append({
                'role': str(item.role),
                'parts': str(item.parts[0])
            })
        # Если parts это строка
        else:
            data.append({
                'role': str(item.role),
                'parts': str(item.parts)
            })


def create_window():
    headers = ['Роль', 'Сообщение']
    table_data = [[item['role'], item['parts']] for item in data]

    layout = [
        [sg.Table(values=table_data,
                  headings=headers,
                  key='-TABLE-',
                  enable_events=True,
                  select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                  expand_x=True,
                  expand_y=True,
                  num_rows=min(len(data), 10))],
        [sg.Text('Role:'), sg.Input(key='-ROLE-', size=(20, 1))],
        [sg.Text('Parts:'), sg.Input(key='-PARTS-', size=(20, 1))],
        [sg.Button('Добавить'), sg.Button('Удалить выбранные'), sg.Button('Сохранить')]
    ]

    return sg.Window('Просмотр диалога', layout, resizable=True)


def main():
    window = create_window()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == '-TABLE-' and values['-TABLE-']:
            selected_index = values['-TABLE-'][0]
            window['-ROLE-'].update(data[selected_index]['role'])
            window['-PARTS-'].update(data[selected_index]['parts'])

        if event == 'Удалить выбранные':
            if values['-TABLE-']:
                for index in sorted(values['-TABLE-'], reverse=True):
                    data.pop(index)
                window['-ROLE-'].update('')
                window['-PARTS-'].update('')
                window['-TABLE-'].update([[item['role'], item['parts']] for item in data])

        if event == 'Добавить':
            if values['-ROLE-'] and values['-PARTS-']:
                data.append({
                    'role': values['-ROLE-'],
                    'parts': values['-PARTS-']
                })
                window['-TABLE-'].update([[item['role'], item['parts']] for item in data])
                window['-ROLE-'].update('')
                window['-PARTS-'].update('')

        if event == 'Сохранить':
            with open('chat_history_edit.pkl', 'wb') as f:
                pickle.dump(data, f)
            sg.popup('Данные успешно сохранены в chat_history_edit.pkl!')

    window.close()


if __name__ == '__main__':
    main()