import sqlite3


def open_database():
    connection = sqlite3.connect("database.bd")
    return connection, connection.cursor()


def close_database(connection):
    connection.commit()
    connection.close()


def insert_item_to_companies_table(cur, name, budget, is_stopped):
    cur.execute(
        f"""INSERT INTO Companies_table ('name', 'budget', 'is_stopped')
                 values('{name}', '{budget}', '{is_stopped})'"""
    )


def get_id_from_data(cur, name, budget):
    return cur.execute(f"SELECT id FROM Companies_table WHERE name = '{name}' AND budget = '{budget}'").fetchall()[0]


def get_data_from_table_with_id(cur, id):
    return cur.execute(f"SELECT name, budget, is_stopped FROM Companies_table WHERE id = '{id}'").fetchall()[0]


def calculate_spent_budget(cur, id):
    return cur.execute(f"SELECT SUM(cashback) FROM History_table WHERE id_company = '{id}'")


def insert_item_to_history_table(cur, id_company, date, cashback, is_stopped):
    cur.execute(
        f"""INSERT INTO History_table ('id_company', 'date', 'cashback', 'is_stopped')
                 values('{id_company}', '{date}', '{cashback}', '{is_stopped}')"""
    )


def get_history_dict(cur, id):
    qu = f"SELECT date, cashback FROM History_table WHERE id_company = '{id}'"
    data = cur.execute(qu).fetchall()
    history = dict()
    for date, cashback in data:
        history[date] = cashback
    return history


con, cur = open_database()

cur.execute("""
CREATE TABLE IF NOT EXISTS Companies_table (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
budget FLOAT,
is_stopped BOOLEAN
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS History_table (
id INTEGER PRIMARY KEY,
id_company INTEGER,
date TEXT NOT NULL,
cashback FLOAT,
is_stopped BOOLEAN
)
""")

close_database(con)
