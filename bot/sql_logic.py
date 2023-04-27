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

        cursor.execute("""CREATE TABLE IF NOT EXISTS services_schedule(
                                                    id INTEGER PRIMARY KEY,
                                                    id_master INTEGER,
                                                    id_client INTEGER,
                                                    date TEXT,
                                                    time_start TEXT,
                                                    time_end TEXT,
                                                    payment TEXT);
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

        cursor.execute("""CREATE TABLE IF NOT EXISTS services_for_masters(
                                                            id INTEGER PRIMARY KEY,
                                                            name_service TEXT);
                                                            """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS links_service_master(
                                                            id INTEGER PRIMARY KEY,
                                                            id_master INTEGER,
                                                            id_service INTEGER);
                                                            """)

        conn.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
        return False


def sql_add_master(master_name, description):
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO masters(name, description) VALUES('{master_name}',{description}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new master: {error}"
        print(error_text)


def sql_add_service(service_name, price, time):
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO services(name, price, time) VALUES('{service_name}','{price}', '{time}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new service: {error}"
        print(error_text)


def sql_add_job_calendar(id_master, date, time_start, time_end):
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO job_calendar(id_master, date, time_start, time_end) VALUES('{id_master}','{date}', '{time_start}', '{time_end}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new service: {error}"
        print(error_text)


def sql_add_services_schedule(id_master, id_client, date, time_start, time_end, payment):
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO services_schedule(id_master, id_client,  date, time_start, time_end, payment) VALUES('{id_master}', '{id_client}', '{date}', '{time_start}', '{time_end}', '{payment}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new services schedule: {error}"
        print(error_text)


def sql_add_client(id_telegram, fio, phone):
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO clients(id_telegram, fio, phone) VALUES('{id_telegram}', '{fio}', '{phone}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new services schedule: {error}"
        print(error_text)


def sql_add_master_skills(id_master, id_service):
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO master_skills(id_master, id_service) VALUES('{id_master}', '{id_service}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new services schedule: {error}"
        print(error_text)


