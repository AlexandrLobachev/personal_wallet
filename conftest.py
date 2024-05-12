import pytest

from main import *


@pytest.fixture()
def create_test_db():
    db = DataBase('test_database')
    db.create_json()


@pytest.fixture()
def test_db(create_test_db):
    db = DataBase('test_database')
    yield db
    db.create_json()


@pytest.fixture()
def get_entry():
    return Entry(
        '2000-01-01',
        'доход',
        1000,
        'тест добавления записи без сохранения в файл'
    )


@pytest.fixture()
def get_book():
    return Book([{
        'date': '2000-01-01',
        'category': 'Доход',
        'amount': 1000,
        'description': 'тест сохранения записи в файл'
    }])


@pytest.fixture()
def get_entry_for_edit():
    return Entry(
        '2000-01-01',
        'доход',
        1000,
        'измененная запись'
    )


@pytest.fixture()
def filling_db(create_test_db):
    db = DataBase('test_database')
    data = [
        {"date": "2024-01-01",
         "category": "Доход",
         "amount": 100000,
         "description": "Запись №1"},
        {"date": "2024-01-01",
         "category": "Расход",
         "amount": 50000,
         "description": "Запись №2"},
        {"date": "2024-05-01",
         "category": "Расход",
         "amount": 20000,
         "description": "Запись №3"},
        {"date": "2024-01-01",
         "category": "Расход",
         "amount": 20000,
         "description": "Запись №4"},
        {"date": "2024-05-01",
         "category": "Расход",
         "amount": 10000,
         "description": "Запись №5"},
    ]
    db.save_json(data)
    yield db.open_json()
    db.create_json()
