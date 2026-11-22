import sys
import sqlite3
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'coffee.sqlite'

HEADERS = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах',
           'Описание вкуса', 'Цена', 'Объем упаковки']

SAMPLE_DATA = [
    ('Эфиопия Иргачефф', 'Светлая', 'В зернах',
     'Цветочные ноты с оттенками бергамота и лимона', 850.0, 250),
    ('Бразилия Сантос', 'Средняя', 'Молотый',
     'Мягкий вкус с нотами жареного ореха и молочного шоколада', 650.0, 250),
    ('Колумбия Супремо', 'Средняя', 'В зернах',
     'Сбалансированный вкус с карамельной сладостью и легкой кислинкой', 790.0, 500),
    ('Итальянский Эспрессо', 'Темная', 'Молотый',
     'Насыщенный крепкий вкус с горчинкой какао и специй', 1200.0, 1000),
]


def load_coffee():
    con = sqlite3.connect(DB_PATH)
    try:
        with con:
            con.execute('''
                CREATE TABLE IF NOT EXISTS coffee (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    roast_degree TEXT NOT NULL,
                    ground_or_beans TEXT NOT NULL,
                    taste_description TEXT,
                    price REAL NOT NULL,
                    package_volume INTEGER NOT NULL
                )
            ''')
            is_empty = not con.execute('SELECT COUNT(*) FROM coffee').fetchone()[0]
            if is_empty:
                con.executemany('''
                    INSERT INTO coffee (title, roast_degree, ground_or_beans,
                                        taste_description, price, package_volume)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', SAMPLE_DATA)
        return con.execute('SELECT * FROM coffee').fetchall()
    finally:
        con.close()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(BASE_DIR / 'UI.ui', self)

        data = load_coffee()

        self.tableWidget.setColumnCount(len(HEADERS))
        self.tableWidget.setHorizontalHeaderLabels(HEADERS)
        self.tableWidget.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, val in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


app = QApplication(sys.argv)
ex = CoffeeApp()
ex.show()
sys.exit(app.exec())
