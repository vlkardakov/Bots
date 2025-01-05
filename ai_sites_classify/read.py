import pandas as pd

def pandas_column_to_array(filename):
    try:
        df = pd.read_csv(filename, encoding='utf-8')
        if df.empty:  # Проверка на пустой DataFrame
          print(f"Файл пуст.")
          return []
        first_column_name = df.columns[0]  # Получение имени первого столбца
        column_array = df[first_column_name].tolist()
        return column_array
    except FileNotFoundError:
        print(f"Файл не найден.")
        return None
    except Exception as e:
        print(f"{e}")
        return None

def read():
    filename = "1_fixed.csv"
    column_array = pandas_column_to_array(filename)

    if column_array is not None:
        print(column_array)
        return column_array
    else:
        return []