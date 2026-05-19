from datetime import datetime
from enum import Enum
from pathlib import Path
import json


DB_PATH = Path(__file__).parent / "books.json"
MENU_SEP = "#" * 50
FUNC_SEP = "-" * 25
DATE_FORMAT = "%d-%m-%Y"


class MenuEntry(Enum):
    add_book = "Добавить книгу"
    list_books = "Показать все книги"
    avg_rating = "Показать среднюю оценку"
    author_stats = "Статистика по авторам"
    remove_book = "Удалить книгу"
    exit_program = "Выход"


class Author:
    """Класс для описания автора и дальнейшего подсчета статистики по авторам"""
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book:
    """Класс для описания книги перед записью в базу"""
    def __init__(self, name, rating, author, date):
        self.name = name
        self.rating = self.define_rating(rating)
        self.date = self.define_date(date)
        self.author = author

    @staticmethod
    def define_rating(rating):
        try:
            rating = int(rating)
        except Exception:
            rating = 1
        return  rating if rating >= 1 <= 5 else 5

    @staticmethod
    def define_date(date):
        try:
            parsed_date = datetime.strptime(date, DATE_FORMAT)
        except Exception:
            parsed_date = datetime.now()
        return parsed_date

    def __str__(self):
        return (f"{datetime.strftime(self.date, DATE_FORMAT)}: "
                f"{self.author.last_name} {self.author.first_name} - "
                f"`{self.name}`. Рейтинг: {self.rating}")

    def __dict__(self):
        return {
            "date": datetime.strftime(self.date, DATE_FORMAT),
            "name": self.name,
            "rating": self.rating,
            "author": self.author.__dict__
        }


def read_db():
    print("Чтение файла базы данных...")
    file = open(DB_PATH, "r", encoding="utf-8")
    parsed_data = []
    try:
        data = json.load(file)
        for item in data:
            parsed_data.append(
                Book(date=datetime.strptime(item["date"], DATE_FORMAT),
                     name=item["name"],
                     rating=item["rating"],
                     author=Author(
                         first_name=item["author"]["first_name"],
                         last_name=item["author"]["last_name"])
                     )
            )
            print("База данных успешно загружена")
        return parsed_data
    except Exception as error:
        print(f"Не удалось прочитать файл базы данных. Ошибка `{error}`")
        return []
    finally:
        file.close()

def write_db(data: list):
    print("Запись изменений в базу данных...")
    file = open(DB_PATH, "w", encoding="utf-8")
    data_to_write = []
    try:
        for item in data:
            data_to_write.append(item.__dict__())
        file.write(json.dumps(data_to_write, ensure_ascii=False))
        print(f"Файл базы данных успешно записан")
    except Exception as error:
        print(f"Не удалось записать файл базы данных. Ошибка `{error}`")
    finally:
        file.close()


def add_book():
    print(f"{FUNC_SEP}\nДобавление книги\n{MENU_SEP}")
    try:
        date = input("Введите дату прочтения в формате ДД-ММ-ГГГГ...\n")
        author_first_name = input("Введите имя автора...\n")
        author_last_name = input("Введите фамилию автора...\n")
        book_name = input("Введите название книги...\n")
        book_rating = int(input("Введите рейтинг книги (1-5)...\n"))
    except Exception as error:
        print(f"Не удалось получить введенные данные. Причина `{error}`.")
        return
    try:
        book_author = Author(first_name=author_first_name, last_name=author_last_name)
        new_book = Book(name=book_name, rating=book_rating, author=book_author, date=date)
    except Exception as error:
        print(f"Не удалось создать книгу по введенным данным. Причина `{error}`.")
        return
    try:
        db = read_db()
        db.append(new_book)
        write_db(db)
    except Exception as error:
        print(f"Не удалось записать в базу новую книгу. Причина `{error}`.")


def list_books(): ...


def avg_rating(): ...


def author_stats(): ...


def remove_book(): ...


def exit_program(): ...


MENU_ENTRY_MAP = {
    MenuEntry.add_book:      add_book,
    MenuEntry.list_books:    list_books,
    MenuEntry.avg_rating:    avg_rating,
    MenuEntry.author_stats:  author_stats,
    MenuEntry.remove_book:   remove_book,
    MenuEntry.exit_program:  exit_program,
}


def run_menu():
    while True:
        print(MENU_SEP)
        numbered_map = {i: item for i, item in enumerate(MenuEntry, start=1)}
        for i, item in numbered_map.items():
            print(f"{i}\t{item.value}")
        print(MENU_SEP)

        try:
            choice = int(input("Введите номер пункта меню:\n"))
        except Exception:
            print("Некорректный ввод. Попробуйте снова.")
            continue

        menu_item = numbered_map.get(choice)
        function = MENU_ENTRY_MAP.get(menu_item)
        if function is None:
            print(f"Не удалось найти соответствующий пункт меню `{choice}`. Попробуйте снова.")
            continue

        function()


if __name__ == '__main__':
    run_menu()
