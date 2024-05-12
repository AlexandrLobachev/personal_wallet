from main import *


def test_get_empty_book(test_db):
    db = test_db.open_json()
    book = Book(db)
    assert book.get_all() == []


def test_get_balance_empty_book(test_db):
    db = test_db.open_json()
    book = Book(db)
    balance = book.balance()
    assert isinstance(balance, str)
    assert balance == (
            f'Текущий баланс: 0\n'
            f'Доходы: 0\n'
            f'Расходы: 0\n'
        )


def test_add_entry(test_db, get_entry):
    db = test_db.open_json()
    book = Book(db)
    book.add(get_entry)
    entries = book.entries
    assert isinstance(entries, list)
    assert entries == [{
        'date': '2000-01-01',
        'category': 'Доход',
        'amount': 1000,
        'description': 'тест добавления записи без сохранения в файл'
    }]


def test_save_book(test_db, get_book):
    test_db.save_json(get_book.entries)
    db = test_db.open_json()
    book = Book(db)
    entries = book.get_all()
    assert len(entries) == 1
    assert entries[0][0] == 1
    assert entries[0][1].__dict__ == {
        'date': '2000-01-01',
        'category': 'Доход',
        'amount': 1000,
        'description': 'тест сохранения записи в файл'
    }


def test_get_balance(filling_db):
    db = filling_db
    book = Book(db)
    balance = book.balance()
    assert isinstance(balance, str)
    assert balance == (
            f'Текущий баланс: 0\n'
            f'Доходы: 100000\n'
            f'Расходы: 100000\n'
        )


def test_edit(filling_db, get_entry_for_edit):
    book = Book(filling_db)
    entry_before_edit = book.entries[0]
    assert entry_before_edit == {
        "date": "2024-01-01",
        "category": "Доход",
         "amount": 100000,
         "description": "Запись №1"
    }
    book.edit(1, get_entry_for_edit)
    entry_after_edit = book.entries[0]
    assert isinstance(entry_after_edit, dict)
    assert entry_after_edit == {
        'date': '2000-01-01',
        'category': 'Доход',
        'amount': 1000,
        'description': 'измененная запись'
    }


def test_find_date(filling_db):
    book = Book(filling_db)
    assert len(book.get_all()) == 5
    filtered_enties = book.filter('date', '2024-05-01')
    assert len(filtered_enties) == 2
    numbers = [entry[0] for entry in filtered_enties]
    assert numbers == [3, 5]


def test_find_category(filling_db):
    book = Book(filling_db)
    assert len(book.get_all()) == 5
    filtered_enties = book.filter('category', 'Расход')
    assert len(filtered_enties) == 4
    numbers = [entry[0] for entry in filtered_enties]
    assert numbers == [2, 3, 4, 5]


def test_find_amount(filling_db):
    book = Book(filling_db)
    assert len(book.get_all()) == 5
    filtered_enties = book.filter('amount', 20000)
    assert len(filtered_enties) == 2
    numbers = [entry[0] for entry in filtered_enties]
    assert numbers == [3, 4]
