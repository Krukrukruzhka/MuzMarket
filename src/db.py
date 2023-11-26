import hashlib
import json
from datetime import datetime, timedelta
from random import choice, choices, randint
import sqlite3
import string
from typing import Optional
import sqlite3 as sql3


class DatabaseController:
    def __init__(self, connection: sqlite3.Connection = sql3.connect(f'src/MusMarket.db', timeout=7, check_same_thread=False)):
        self.connection = connection
        self.cursObj = self.connection.cursor()

    def _drop_table(self, table_name: str) -> None:
        self.cursObj.execute(f"DROP TABLE IF EXISTS {table_name}")

    def _create_table(self, table_name: str, params: dict[str, str], foreign: Optional[dict[str, str]] = None):
        separator = ', \n\t'
        query = f"CREATE TABLE IF NOT EXISTS {table_name}(\n\t{separator.join([f'{i} {params[i]}' for i in params])}"
        if foreign:
            query += ', \n\n\t' + separator.join([f'FOREIGN KEY ({foreign[i]}) REFERENCES {i}({foreign[i][-2:]})' for i in foreign])
        query += '\n);'
        # print(query, end='\n\n\n\n')
        self.cursObj.execute(query)
        self.connection.commit()

    def _email_is_exits(self, email: str) -> bool:
        query = f"""
                    SELECT * FROM user
                    WHERE email = "{email}";    
                """
        return bool(self.cursObj.execute(query).fetchone())

    def registrate_new_user(self, name: str, email: str, password: str, id_region: Optional[int] = None) -> bool:
        if self._email_is_exits(email):
            print('This email exists')
            return False
        else:
            query = f"""
                        INSERT INTO user(firstname, email, hashed_password, region_id) VALUES (?, ?, ?, ?);
                    """
            self.cursObj.execute(query, (name, email, password, id_region))
            self.connection.commit()
            return True

    def _get_password(self, email: str) -> Optional[str]:
        if not self._email_is_exits(email):
            print('This email not exist')
            return None
        query = f"""
                   SELECT hashed_password FROM user
                   WHERE email = "{email}"; 
                """
        return self.cursObj.execute(query).fetchone()[0]

    def get_all_regions(self) -> tuple[str]:
        query = """
            SELECT title FROM region;
        """
        return tuple(map(lambda x: str(x[0]), self.cursObj.execute(query).fetchall()))

    def _fast_create_database(self):
        def _fill_regions() -> None:
            current_regions = set([i[0] for i in self.cursObj.execute("SELECT title FROM region;").fetchall()])
            with open('src/regions.txt', 'r', encoding='utf-8') as file:
                regions = set([i[:-1] for i in file.readlines()]).difference(current_regions)
            if len(regions) == 0:
                return None
            values = ', \n\t\t\t\t'.join([f'("{region}")' for region in regions])
            query = f"""
                   INSERT INTO region (title) VALUES 
                       {values};
               """
            self.cursObj.execute(query)

        def _fill_users(n: int) -> None:
            def generate_email() -> str:
                words = ['cat', 'dog', 'sun', 'breath', 'moon', 'jupyter', 'salt', 'coal', 'diamond', 'iron', 'cooper',
                         'stone', 'mouse', 'lake', 'river', 'nirvana', 'numb', 'medium', 'solid', 'chicken', 'rule',
                         'black', 'rambler', 'gold', 'red', 'word', 'war', 'piano', 'magazine', 'gravity', 'trace',
                         'price',
                         'redstone', 'wood', 'cobblestone', 'button', 'brain', 'look', 'guitar', 'computer']
                domains = ['mail.ru', 'gmail.com', 'yandex.ru', 'ya.ru', 'rambler.com', 'outlook.com']
                name = '_'.join([choice(words) for _ in range(randint(1, 4))])
                flag = randint(0, 5)
                if flag == 1 or flag == 3:
                    name += '_'
                if flag == 1 or flag == 2:
                    name += str(randint(1950, 2020))
                elif flag == 3 or flag == 4:
                    name += str(randint(50, 120) % 100 + 1)
                return name + '@' + choice(domains)

            def generate_password() -> str:
                password = ''.join([choice(string.ascii_letters + string.digits) for _ in range(randint(6, 16))])
                return hashlib.sha256(password.encode('utf-8')).hexdigest()

            regions = list(map(lambda x: x[0], self.cursObj.execute("SELECT id FROM region;").fetchall()))
            regions.append('Null')
            roles = list(map(lambda x: x[0], self.cursObj.execute("SELECT id FROM role;").fetchall()))
            roles.append('Null')
            roles = choices(roles, weights=(57, 3, 30, 9, 1), k=n)
            with open("src/firstnames.txt", "r", encoding="utf-8") as file:
                firstnames = tuple(map(lambda x: x[:-1], file.readlines()))
            emails = set()
            while len(emails) != n:
                emails.add(generate_email())
            emails = list(emails)
            users = [(choice(roles), choice(regions), choice(firstnames), emails[i], generate_password()) for i in
                       range(n)]
            separator = ',\n\t\t\t\t'
            query = f"""
                   INSERT INTO user (role_id, region_id, firstname, email, hashed_password) VALUES
                       {separator.join(map(lambda x: str(x), users))};
               """
            self.cursObj.execute(query)

        def _fill_stores(n: int) -> None:
            def generate_address(region: str) -> str:
                streets = ['Беговая', 'Центральная', 'Мололодежная', 'Школьная', 'Мира', 'Советская', 'Садовая',
                           'Лесная',
                           'Ленина', 'Новая', 'Набережная', 'Солнечная', 'Смоленская', 'Сельская', 'Кузнецкая',
                           'Правды',
                           'Победы', 'Славы', 'Врубеля', 'Музыкальная']
                return region + ', ул. ' + choice(streets) + ', д. ' + str(randint(1, 50)) + ', к. ' + str(
                    randint(1, 9))

            def format_to_number(number: int) -> str:
                number = str(number)
                return f"+{number[0]}({number[1:4]}){number[4:7]}-{number[7:9]}-{number[9:11]}"

            available_regions = dict(
                map(lambda x: x[0:2], self.cursObj.execute("SELECT id, title FROM region;").fetchall()))
            region_id = tuple(choices(tuple(available_regions.keys()), k=n))
            addresses = set()
            while addresses.__len__() != n:
                addresses.add(generate_address(available_regions[region_id[len(addresses)]]))
            numbers = set()
            while len(numbers) != n:
                numbers.add(randint(7_000_000_00_00, 8_000_000_00_00))
            numbers = tuple(map(format_to_number, numbers))
            work_hours = ['Мы открыты всегда' if i % 2 == 0 else 'NULL' for i in range(n)]
            separator = ', \n\t\t\t\t'
            query = f"""
                   INSERT INTO store (region_id, address, phone, work_hours) VALUES
                       {separator.join(map(str, zip(region_id, addresses, numbers, work_hours)))};
               """
            self.cursObj.execute(query)

        def _fill_items() -> None:
            subcategories = {subcategory[2]: subcategory[0] for subcategory in
                             self.cursObj.execute("SELECT * FROM subcategory;")}
            with open('src/items/instruments/common.json', 'r', encoding='utf-8') as file:
                items = json.load(file)
            separator = ', \n\t\t\t\t'
            values = [
                f"({subcategories[item['subcategory']]}, {item['title'].__repr__()}, {item['price']}, {item['rate']}, {item['href'].split('/')[-1].__repr__()})"
                for item in items]
            query = f"""
                   INSERT INTO item (subcategory_id, title, price, rate, article) VALUES
                   {separator.join(values)};
               """
            self.cursObj.execute(query)

        def _fill_categories() -> None:
            with open('src/categories.json', 'r', encoding='utf-8') as file:
                categories = map(lambda x: f"{x['title']}", json.load(file))
            separator = ', \n\t\t\t\t'
            values = [f'("{category}")' for category in categories]
            query = f"""
                   INSERT INTO category (title) VALUES
                   {separator.join(values)};
               """
            # print(query)
            self.cursObj.execute(query)

        def _fill_subcategories() -> None:
            categories = {category[1]: category[0] for category in self.cursObj.execute("SELECT * FROM category;")}
            with open('src/categories.json', 'r', encoding='utf-8') as file:
                items = [
                    [{'category_id': categories[item['title']], 'title': i['title'], 'endpoint': i['endpoint']} for i in item["subcategories"]] for
                    item in json.load(file)]
                a = []
                for i in items:
                    a.extend(i)
                items = a
                del a

            separator = ', \n\t\t\t\t'
            values = ['(' + str(item['category_id']) + ', "' + item['title'] + '", "' + item['endpoint'] + '")' for item in items]
            query = f"""
                   INSERT INTO subcategory (category_id, title, endpoint) VALUES
                       {separator.join(values)};
               """
            self.cursObj.execute(query)

        def _fill_items_stores(n: int) -> None:
            items = tuple(map(lambda x: x[0], self.cursObj.execute("SELECT id FROM item;").fetchall()))
            stores = tuple(map(lambda x: x[0], self.cursObj.execute("SELECT id FROM store;").fetchall()))
            items_stores = [(choice(items), choice(stores), randint(0, 150)) for _ in range(n)]
            separator = ', \n\t\t\t\t'
            values = [f'{item}' for item in items_stores]
            query = f"""
                   INSERT INTO item_store (item_id, store_id, amount) VALUES
                       {separator.join(values)};
               """
            self.cursObj.execute(query)

        def _fill_orderings(n: int) -> None:
            def generate_timestamp() -> str:
                current_time = datetime.now()
                current_time -= timedelta(days=randint(0, 80), hours=randint(0, 24), minutes=randint(0, 60),
                                          seconds=randint(0, 60))
                return str(current_time)[:19]

            users = tuple(map(lambda x: x[0], self.cursObj.execute("SELECT id FROM user;").fetchall()))
            items = tuple(map(lambda x: x[0], self.cursObj.execute("SELECT id FROM item;").fetchall()))
            stores = tuple(map(lambda x: x[0], self.cursObj.execute("SELECT id FROM store;").fetchall()))
            statuses = tuple(map(lambda x: x[0], self.cursObj.execute("SELECT id FROM status;").fetchall()))
            orderings = set()
            while len(orderings) != n:
                orderings.add((choice(users), choice(items), choice(stores), generate_timestamp()))
            orderings = list(orderings)
            for i in range(len(orderings)):
                orderings[i] = (*orderings[i], choice(statuses), randint(1, 5))
            separator = ', \n\t\t\t\t'
            values = [f"{i}" for i in orderings]
            query = f"""
                           INSERT INTO ordering (user_id, item_id, store_id, timestamp, status_id, amount) VALUES
                           {separator.join(values)};
                       """
            with open('src/orderings.txt', 'w+', encoding='utf-8') as file:
                file.write(query)
            self.cursObj.execute(query)

        def _fill_all_tables_with_filters() -> None:

            subcategories = self.cursObj.execute("SELECT id, title FROM subcategory;").fetchall()
            subcategories = {i[1]: i[0] for i in subcategories}

            with open("src/filters.json", "r", encoding="utf-8") as file:
                file_list = json.load(file)
            strainers = set(map(lambda item: item["title"], file_list))

            separator = ', \n\t\t\t\t'
            values = [f'("{item}")' for item in strainers]
            query = f"""
                INSERT INTO strainer (title) VALUES
                {separator.join(values)};
            """
            self.cursObj.execute(query)

            strainers = self.cursObj.execute("SELECT id, title FROM strainer;").fetchall()
            strainers = {i[1]: i[0] for i in strainers}

            values = []
            for item in file_list:
                for subcategory in item["subcategories"]:
                    strainer_id, subcategory_id = strainers[item["title"]], subcategories[subcategory]
                    values.append(f'({strainer_id}, {subcategory_id})')
            query = f"""
                INSERT INTO strainer_subcategory (strainer_id, subcategory_id) VALUES
                    {separator.join(values)};
            """
            self.cursObj.execute(query)

            values = set()
            for item in file_list:
                for parameter in item["values"]:
                    strainer_id, value = strainers[item["title"]], parameter
                    values.add(f'({strainer_id}, "{value}")')
            query = f"""
                INSERT INTO parameter (strainer_id, title) VALUES
                    {separator.join(values)};
            """
            self.cursObj.execute(query)

            items = self.cursObj.execute(
                "SELECT item.id, subcategory.title FROM item INNER JOIN subcategory ON item.subcategory_id = subcategory.id;").fetchall()
            parameters = self.cursObj.execute(
                "SELECT parameter.id, strainer.title, parameter.title FROM parameter INNER JOIN strainer ON strainer.id = parameter.strainer_id;").fetchall()
            p = {i[1]: dict() for i in parameters}
            for i in parameters:
                p[i[1]][i[2]] = i[0]
            parameters = p
            del p
            items_parameters = []
            for item in items:
                for element in file_list:
                    if item[1] in element['subcategories']:
                        items_parameters.append((item[0], parameters[element['title']][choice(element['values'])]))

            values = [f'{i}' for i in items_parameters]
            query = f"""
                INSERT INTO item_parameter (item_id, parameter_id) VALUES
                    {separator.join(values)};
            """
            self.cursObj.execute(query)


        TABLES = ['region', 'role', 'user', 'store', 'category', 'subcategory', 'strainer_subcategory', 'strainer',
                  'parameter', 'item', 'status', 'ordering', 'item_store', 'item_parameter', 'basket']
        for table in TABLES:
            self._drop_table(table_name=table)
        self.connection.commit()

        self._create_table(table_name='region', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'title': 'TEXT NOT NULL UNIQUE'
        })
        self._create_table(table_name='role', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'title': 'TEXT NOT NULL UNIQUE'
        })
        self._create_table(table_name='user', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'firstname': 'TEXT NOT NULL',
            'email': 'TEXT NOT NULL UNIQUE',
            'region_id': 'INTEGER',
            'hashed_password': 'TEXT NOT NULL',
            'role_id': 'INTEGER',
            'is_active': 'BOOLEAN NOT NULL DEFAULT TRUE',
            'is_superuser': 'BOOLEAN NOT NULL DEFAULT FALSE',
            'is_verified': 'BOOLEAN NOT NULL DEFAULT FALSE'
        }, foreign={
            'region': 'region_id',
            'role': 'role_id'
        })
        self._create_table(table_name='store', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'address': 'TEXT NOT NULL UNIQUE',
            'phone': 'TEXT NOT NULL UNIQUE',
            'region_id': 'INTEGER NOT NULL',
            'work_hours': 'TEXT NOT NULL'
        }, foreign={
            'region': 'region_id'
        })
        self._create_table(table_name='category', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'title': 'TEXT NOT NULL UNIQUE'
        })
        self._create_table(table_name='subcategory', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'category_id': 'INTEGER NOT NULL',
            'title': 'TEXT NOT NULL UNIQUE',
            'endpoint': 'TEXT NOT NULL UNIQUE'
        }, foreign={
            'category': 'category_id'
        })
        self._create_table(table_name='strainer', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'title': 'TEXT NOT NULL UNIQUE'
        })
        self._create_table(table_name='strainer_subcategory', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'subcategory_id': 'INTEGER NOT NULL',
            'strainer_id': 'INTEGER NOT NULL'
        }, foreign={
            'strainer': 'strainer_id'
        })
        self._create_table(table_name='parameter', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'title': 'TEXT NOT NULL',
            'strainer_id': 'INTEGER NOT NULL'
        }, foreign={
            'strainer': 'strainer_id'
        })
        self._create_table(table_name='item', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'title': 'TEXT NOT NULL',
            'price': 'INTEGER NOT NULL',
            'subcategory_id': 'INTEGER NOT NULL',
            'rate': 'REAL',
            'article': 'TEXT NOT NULL'
        }, foreign={
            'subcategory': 'subcategory_id'
        })
        self._create_table(table_name='status', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'title': 'TEXT NOT NULL UNIQUE',
        })
        self._create_table(table_name='ordering', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'store_id': 'INTEGER NOT NULL',
            'item_id': 'INTEGER NOT NULL',
            'user_id': 'INTEGER NOT NULL',
            'timestamp': 'TEXT NOT NULL',
            'amount': 'INTEGER NOT NULL',
            'status_id': 'INTEGER NOT NULL'
        }, foreign={
            'status': 'status_id',
            'store': 'store_id',
            'item': 'item_id',
            'user': 'user_id'
        })
        self._create_table(table_name='item_store', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'store_id': 'INTEGER NOT NULL',
            'item_id': 'INTEGER NOT NULL',
            'amount': 'INTEGER NOT NULL'
        }, foreign={
            'store': 'store_id',
            'item': 'item_id'
        })
        self._create_table(table_name='item_parameter', params={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'parameter_id': 'INTEGER NOT NULL',
            'item_id': 'INTEGER NOT NULL'
        }, foreign={
            'parameter': 'parameter_id',
            'item': 'item_id'
        })
        # self._create_table(table_name='basket', params={
        #     'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        #     'user_id': 'INTEGER NOT NULL',
        #     'item_id': 'INTEGER NOT NULL'
        # }, foreign={
        #     'user': 'user_id',
        #     'item': 'item_id'
        # })
        print('База создана')

        _fill_regions()
        print('Таблица region заполнена')
        self.cursObj.execute("""
            INSERT INTO role (title) VALUES 
            ("Клиент"), ("Администратор"), ("Продавец"), ("Курьер");
        """)
        print('Таблица role заполнена')
        self.cursObj.execute("""
            INSERT INTO status (title) VALUES 
            ("Принят"), ("В сборке"), ("В доставке"), ("Доставлен");
        """)
        print('Таблица status заполнена')
        _fill_categories()
        print('Таблица category заполнена')
        _fill_subcategories()
        print('Таблица subcategory заполнена')
        _fill_users(n=40_000)
        print('Таблица user заполнена')
        _fill_stores(n=20_000)
        print('Таблица store заполнена')
        _fill_items()
        print('Таблица item заполнена')
        _fill_items_stores(n=50_000)
        print('Таблица item_store заполнена')
        _fill_orderings(n=100_000)
        print('Таблица ordering заполнена')

        _fill_all_tables_with_filters()
        print('Таблицы связанные с фильтрами заполнены')

        self.connection.commit()


if __name__ == '__main__':
    contr = DatabaseController()
    contr._fast_create_database()
    contr.connection.close()

