import csv
import os

folder_path = '/Users/nikitasolovev/Dev/api_yamdb/api_yamdb/static/data'
# Получите список файлов в папке
file_list = os.listdir(folder_path)
# Проход по каждому файлу и чтение его содержимого
for file_name in file_list:
    print(f'Содержимое файла {file_name}:')

    with open(file_name, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
    print('\n')