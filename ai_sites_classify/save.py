import csv

def save(table_name, data):
    """
    Сохраняет список словарей в CSV-файл, отсортированный по ключу 'danger' в убывающем порядке.

    Args:
        table_name: Имя файла CSV (без расширения .csv).
        data: Список словарей. Каждый словарь представляет собой строку данных,
              где ключи - имена столбцов, а значения - данные для столбцов.  Должен содержать ключ 'danger'.
    """

    if not data:
        print("Список данных пуст. Ничего не сохранено.")
        return

    if not all(data[0].keys() == d.keys() for d in data) or 'danger' not in data[0].keys():
        print("Ошибка: Словари в списке должны иметь одинаковые ключи, включая ключ 'danger'.")
        return

    try:
        # Преобразуем значения 'danger' в целые числа для корректной сортировки
        for row in data:
            try:
                row['danger'] = int(row['danger'])
            except:
                row['danger'] = 11
        # Сортируем данные по ключу 'danger' в убывающем порядке
        data.sort(key=lambda x: x['danger'], reverse=True)


        with open(f"{table_name}.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Данные успешно сохранены в файл {table_name}.csv")
    except ValueError as e:
        print(f"Ошибка: Значение 'danger' должно быть целым числом: {e}")
    except Exception as e:
        print(f"Ошибка при сохранении в CSV: {e}")


#save_to_csv("casinos", casinos)
#save_to_csv("scams", scams)
#save_to_csv("goods", goods)
#save_to_csv("adult_contents", adult_contents)