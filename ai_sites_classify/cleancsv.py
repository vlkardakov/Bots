import pandas as pd
from urllib.parse import unquote

def remove_rows_containing_words_and_duplicates_pandas(input_file, output_file, bad_words):
    try:
        df = pd.read_csv(input_file, encoding='utf-8')

        # Удаление строк с указанными словами
        df = df[~df.apply(lambda row: any(word in str(val).lower() for val in row for word in bad_words), axis=1)]

        # Декодирование URL-адресов (предполагается, что URL находятся в столбце с именем 'url')
        if 'url' in df.columns:
          df['url'] = df['url'].apply(lambda x: unquote(x) if isinstance(x, str) else x)


        # Удаление дубликатов
        df.drop_duplicates(subset=None, inplace=True)

        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Результат сохранен в {output_file}")
    except FileNotFoundError:
        print(f"Файл {input_file} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def clean():
    # Пример использования:
    input_file = "1.csv"
    output_file = "1_fixed.csv"
    bad_words = ["singkat", "google.com", "facebook.com", "co.kr", "virustotal.com",'yahoo.com','flip-up.fun',"s343981.world","meinturnierplan.de","kw1","KW1","ya.ru","whatsapp.com"]
    remove_rows_containing_words_and_duplicates_pandas(input_file, output_file, bad_words)

if __name__ == "__main__":
    clean()