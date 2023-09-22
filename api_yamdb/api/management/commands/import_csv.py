import csv
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django.db.utils import IntegrityError
from django.db.models import Model

from api_yamdb.settings import BASE_DIR
from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title, User)


class Command(BaseCommand):
    help = '''
    Команда для заполнения базы данных из csv файлов.
    загрузите файл в папку read_csv и используйте команду в формате:
    python manage.py <your_model> <your_csv_file.csv>
    '''
    folder_path: str = BASE_DIR / 'read_csv'
    names_of_models: dict[str, Model] = {
        'category': Category,
        'comment': Comment,
        'title': Title,
        'genre': Genre,
        'genretitle': GenreTitle,
        'review': Review,
        'user': User,
    }
    created_or_exists: dict[bool, str] = {
        True: 'добавлен',
        False: 'уже существует'
    }

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('model', type=str)
        parser.add_argument('file_name', type=str)

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            file = open(
                self.folder_path / options.get('file_name'), encoding='utf')
            Model = self.names_of_models[options.get('model').lower()]

        except FileNotFoundError:
            return 'Файл не найден'
        except KeyError:
            return 'Модель не найдена'

        reader = csv.DictReader(f=file)

        for row in reader:
            try:
                obj, is_created = Model.objects.get_or_create(**row)
                self.stdout.write(
                    f'Объект {obj} {self.created_or_exists[is_created]}')

            except IntegrityError as err:
                if str(err).split(' ')[0] == 'UNIQUE':
                    self.stdout.write('Пользователь уже оставил такую запись')
                elif str(err).split(' ')[0] == 'FOREIGN':
                    self.stdout.write('Объект-родитель не найден')
                else:
                    err = str(err)
                    self.stdout.write(f'Ошибка в данных: {err}')
            except ValueError as err:
                self.stdout.write(f'Ошибка в названии данных: {err}')
