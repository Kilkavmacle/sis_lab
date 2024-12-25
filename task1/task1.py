import json

def get_json_value(file_path, row_key, col_index):
    with open(file_path) as jsonfile:
        data = json.load(jsonfile)
        row_values = data["nodes"][str(row_key)]
        return row_values[col_index]

if __name__ == "__main__":
    file_path = input()
    row_key = input()
    col_index = int(input())

    try:
        value = get_json_value(file_path, row_key, col_index)
        print(f'Значение в строке {row_key} и колонке {col_index}: {value}')
    except KeyError:
        print(f'Строка {row_key} не найдена.')
    except IndexError:
        print(f'Колонка {col_index} не найдена.')
    except Exception as e:
        print(f'Произошла ошибка: {e}')
