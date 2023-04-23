import sqlite3
from datetime import datetime


def check_sql():
    """проверяем бд, если не создана, то создаем"""
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS masters(
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            description TEXT NOT NULL);
                            """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS services(
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    price INTEGER NOT NULL,
                                    time TEXT);
                                    """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS master_skills(
                                            id INTEGER PRIMARY KEY,
                                            id_master INTEGER,
                                            id_service INTEGER);
                                            """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS job_calendar(
                                            id INTEGER PRIMARY KEY,
                                            id_master INTEGER,
                                            date TEXT,
                                            time_start TEXT,
                                            time_end TEXT);
                                            """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS clients(
                                                    id INTEGER PRIMARY KEY,
                                                    id_telegram INTEGER,
                                                    fio TEXT,
                                                    phone TEXT);
                                                    """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS services_schedule(
                                                    id INTEGER PRIMARY KEY,
                                                    id_master INTEGER,
                                                    id_client INTEGER,
                                                    date TEXT,
                                                    time_start TEXT,
                                                    time_end TEXT,
                                                    payment TEXT);
                                                    """)

        conn.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
        return False


def sql_add_master():
    pass


def sql_all_service():
    pass


def sql_add_job_calendar():
    pass


def sql_services_schedule():
    pass


def sql_add_client():
    pass

