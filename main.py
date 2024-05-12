import json
import datetime
from typing import List, Tuple, Union, Dict


class DataBase():
    """Класс для подключения к БД."""

    def __init__(self, filename):
        self.filename = filename

    def open_json(self) -> Dict:
        """Открывает JSON файл."""
        file = self.filename+'.json'
        with open(file=file, mode='r', encoding='utf-8') as file:
            return json.load(file)

    def create_json(self) -> None:
        """Создает JSON файл."""
        file = self.filename+'.json'
        with open(file=file, mode='w', encoding='utf-8') as file:
            json.dump([], file, indent=4, ensure_ascii=False)

    def save_json(self, data: List[Dict]) -> None:
        """Сохраняет данные в JSON файл."""
        file = self.filename + '.json'
        with open(file=file, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class Entry():
    """Класс записи дохода или расхода."""

    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description
        self.check_args()

    def __str__(self):
        return (
            f'Дата: {self.date}\n'
            f'Категория: {self.category}\n'
            f'Сумма: {self.amount}\n'
            f'Описание: {self.description}\n'
        )

    def check_date(self):
        '''Проверяет формат полученной даты.'''
        try:
            datetime.datetime.strptime(self.date, "%Y-%m-%d")
        except:
            raise ValueError('Формат даты должен быть YYYY-MM-DD.')

    def check_category(self):
        '''Проверяет формат категории и приводит ее к одинаковому виду.'''
        if self.category.lower() not in ['расход', 'доход']:
            raise ValueError('Категория может быть только Расход или Доход')
        self.category = self.category.title()

    def check_amount(self):
        '''Проверяет сумму.'''
        try:
            self.amount = int(self.amount)
        except:
            raise ValueError('Сумма должна быть числом.')
        if self.amount < 1:
            raise ValueError('Сумма должна быть больше или равна 1.')

    def check_args(self):
        self.check_date()
        self.check_category()
        self.check_amount()


class Book():
    """Класс книги записей о даходах и расходах."""

    def __init__(self, entries):
        self.entries = entries

    def __len__(self):
        return len(self.entries)

    def add(self, entry: Entry) -> None:
        '''Добавляет новую запись.'''
        self.entries.append(entry.__dict__)

    def edit(self, number: int, entry: Entry) -> None:
        '''Заменяет старую запись на новую по номеру.'''
        edit_index = number - 1
        self.entries[edit_index] = entry.__dict__

    def delete(self, number: int) -> None:
        '''Удаляет запись по номеру.'''
        del_index = number - 1
        self.entries.pop(del_index)

    def get_all(self) -> List[Tuple[int, Entry]]:
        """Возвращает все записи."""
        index = 1
        all_data = []
        for entry in self.entries:
            current_entry = (index, Entry(**entry))
            all_data.append(current_entry)
            index += 1
        return all_data

    def get_one(self, number: int) -> Entry:
        """Возвращает одну запись по номеру."""
        return Entry(**self.entries[number - 1])

    def balance(self) -> str:
        """Возвращает строку с текущим балансом, доходами и расходами."""
        profit = 0
        expenses = 0
        for entry in self.entries:
            if entry['category'] == 'Доход':
                profit += entry['amount']
            else:
                expenses += entry['amount']
        balance = profit - expenses
        return (
            f'Текущий баланс: {balance}\n'
            f'Доходы: {profit}\n'
            f'Расходы: {expenses}\n'
        )

    def filter(self, field: str, param: Union[str, int]
               ) -> List[Tuple[int, Entry]]:
        all_entries = self.get_all()
        filtered_data = [
            entry for entry in all_entries if getattr(entry[1], field) == param
        ]
        return filtered_data


def validate_number(book: Book, number: str) -> Union[None, int]:
    """Валидирует введеный номер записи."""
    if not number:
        return
    try:
        number = int(number)
    except:
        print('Введен не корректный номер записи.')
        return
    if number < 1 or number > len(book):
        print('Введен не корректный номер записи.')
        return
    return number


def input_number(action: str) -> Union[str, None]:
    """Принимает от пользователя номер записи."""
    number = input(
        f'Введите номер записи, которую надо {action} '
         'или M для возврата в главное меню.\n'
    ).lower()
    print('\n')
    if number in ['m', 'м']:
        return
    return number


def input_data() -> Dict:
    """Принимает от пользователя новую запись."""
    entry = {}
    entry['date'] = input('Введите дату в формате YYYY-MM-DD.')
    entry['category'] = input('Введите категорию Доход или Расход.')
    entry['amount'] = input('Введите сумму.')
    entry['description'] = input('Введите описание.')
    return entry


def confirmation(book: Book, number: int, action: str) -> Union[bool, None]:
    """Запрашивает подтверждение на изменение/удаление записи."""
    print(f'Вы действительно хотите {action} запись:')
    print(book.get_one(number))
    confirmation = input(
        'Для подтверждения нажмите Y, для отмены любую кнопку.'
    ).lower()
    if confirmation not in ['y', 'у']:
        return
    return True


def filter(book: Book) -> None:
    """Принимает параметры для поиска и выводит подходящие записи."""
    print(
        'По какому параметру будем искать?\n'
        '1 - По дате.\n'
        '2 - По категории.\n'
        '3 - По сумме.\n'
    )
    find_map = {
        '1': ('date', 'в формате YYYY-MM-DD'),
        '2': ('category', 'Доход или Расход'),
        '3': ('amount', 'например: 1500'),
    }
    choice_find = input()
    field = find_map[choice_find][0]
    message = find_map[choice_find][1]
    param = input(f'Введите значение для поиска({message}):')
    if field == 'amount':
        param = int(param)
    filtered_book = book.filter(field, param)
    if not filtered_book:
        print('Записей не найдено.\n')
        return
    for entry in filtered_book:
        print(f'Номер записи: {entry[0]}')
        print(entry[1])


def select_entry_for_action(book: Book, action: str) -> Union[int, None]:
    """Проверяет введенный номер и подтверждает действие."""
    number = validate_number(book, input_number(action))
    if not number:
        return
    if not confirmation(book, number, action):
        return
    return number


def menu() -> None:
    """Выводит меню."""
    print('Выберите один из пунктов меню.')
    print('1 - Баланс.')
    print('2 - Добавить запись.')
    print('3 - Редактировать запись.')
    print('4 - Поиск записей.')
    print('5 - Все записи.')
    print('6 - Удалить запись.')
    print('выход - Выход.')

def main() -> None:
    """Основная логика программы."""
    while True:
        db = DataBase('database')
        try:
            data = db.open_json()
        except:
            db.create_json()
            data = db.open_json()
        book = Book(data)
        menu()
        choice = input('\n').lower()

        if choice == '1': # Баланс.
            print(book.balance())

        elif choice == '2': # Добавление записи.
            data = input_data()
            try:
                entry = Entry(**data)
            except Exception as e:
                print(e)
                continue
            book.add(entry)
            db.save_json(book.entries)

        elif choice == '3': # Редактирование записи.
            number = select_entry_for_action(book, 'изменить')
            if not number:
                continue
            new_data = input_data()
            try:
                entry = Entry(**new_data)
            except Exception as e:
                print(e)
                continue
            book.edit(number, entry)
            db.save_json(book.entries)

        elif choice == '4': # Поиск записи.
            filter(book)

        elif choice == '5': # Все записи.
            for entry in book.get_all():
                print(f'Номер записи: {entry[0]}')
                print(entry[1])

        elif choice == '6': # Удаление записи.
            number = select_entry_for_action(book, 'удалить')
            if not number:
                continue
            book.delete(number)
            db.save_json(book.entries)

        elif choice == 'выход':
            break
        else:
            print('Введена неизвестная команда.')

if __name__ == '__main__':
    print('Л_И_Ч_Н_Ы_Й Ф_И_Н_А_Н_С_О_В_Ы_Й К_О_Ш_Е_Л_Е_К.\n')
    main()