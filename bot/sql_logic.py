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

        cursor.execute("""CREATE TABLE IF NOT EXISTS categories(
                                            id INTEGER PRIMARY KEY,
                                            name TEXT NOT NULL);
                                            """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS services_category(
                                            id INTEGER PRIMARY KEY,
                                            id_category TEXT NOT NULL,
                                            id_service TEXT NOT NULL);
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

        cursor.execute("""CREATE TABLE IF NOT EXISTS schedule(
                                                            id INTEGER PRIMARY KEY,
                                                            id_master TEXT,
                                                            id_client TEXT,
                                                            id_service TEXT,
                                                            date TEXT);
                                                            """)
        conn.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
        return False


def sql_add_master(master_name, description):
    """ добавить мастера """
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO masters(name, description) VALUES('{master_name}','{description}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new master: {error}"
        print(error_text)


def sql_add_category(name_category):
    """ добавить категорию """
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO categories(name) VALUES('{name_category}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new service: {error}"
        print(error_text)


def sql_add_service(service_name, price, time):
    """ добавить услугу """
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
    """ добавить дату работы мастера """
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO job_calendar(id_master, date, time_start, time_end) VALUES('{id_master}','{date}', '{time_start}', '{time_end}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new service: {error}"
        print(error_text)


def sql_add_client(id_telegram, fio, phone):
    """ добавить клиента """
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
    """ добавить навыки для мастера """
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


def sql_add_relation_services(category_id, service_id):
    """ связать услуги и категории в бд """
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO services_category(id_category, id_service) VALUES('{category_id}', '{service_id}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new services schedule: {error}"
        print(error_text)


def sql_add_relation_master(master_id, service_id):
    """ связать услуги и мастера в бд """
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO master_skills(id_master, id_service) VALUES('{master_id}', '{service_id}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new services schedule: {error}"
        print(error_text)


def sql_get_id_client(id_telegram):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    id_client = cursor.execute(f"SELECT id FROM clients WHERE id_telegram='{id_telegram}'").fetchall()[0]
    return id_client


def sql_get_all_reg_client(id_client):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    all_reg = cursor.execute(f"SELECT id, date from schedule WHERE id_client='{id_client}'").fetchall()
    return all_reg


def sql_get_all_info_reg(id_reg):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    # date, master, service, price
    my_reg = cursor.execute(f"SELECT date, id_master, id_service FROM schedule WHERE id='{id_reg}'").fetchall()[0]
    date = my_reg[0]
    master = my_reg[1]
    service = my_reg[2]
    return date, master,service


def sql_get_all_category():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    all_cat = cursor.execute("SELECT id, name from categories").fetchall()
    return all_cat


def sql_get_name_cat(id_cat):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    all_cat = cursor.execute(f"SELECT name FROM categories WHERE id='{id_cat}'").fetchall()[0]
    # print(all_cat)[0]
    return all_cat[0]


def sql_get_all_services(id_category):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    all_services = cursor.execute(
        f"SELECT services.id, services.name FROM services, services_category WHERE "
        f"services.id=services_category.id_service and services_category.id_category={id_category}").fetchall()
    return all_services


def sql_get_name_service(id_service):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    name_service = cursor.execute(f"SELECT name FROM services WHERE id='{id_service}'").fetchall()[0]
    return name_service[0]


def sql_get_service_master(id_service):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    all_masters = cursor.execute(f"SELECT masters.id, masters.name FROM masters, master_skills "
                                 f"WHERE masters.id=master_skills.id_master AND master_skills.id_service={id_service}").fetchall()
    return all_masters


def sql_get_name_master(id_master):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    name_master = cursor.execute(f"SELECT name FROM masters WHERE id='{id_master}'").fetchall()[0]
    return name_master


def sql_get_all_alone_service():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    all_alone_service = cursor.execute(f"SELECT id, name FROM services WHERE NOT EXISTS ("
                                       f"SELECT 1 FROM services_category WHERE services_category.id_service=services.id"
                                       f")").fetchall()
    print(all_alone_service)
    return all_alone_service


def sql_get_all_masters():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    all_masters = cursor.execute("SELECT id, name FROM masters").fetchall()
    return all_masters


def sql_get_price(id_service):
    """ получение стоимости услуги """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    price = cursor.execute(f"SELECT price FROM services WHERE id='{id_service}'").fetchall()[0]
    return price

def sql_check_telegram(telegram_id):
    """ проверка клиента в бд """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    all_masters = cursor.execute(f"SELECT id FROM clients WHERE id_telegram='{telegram_id}'").fetchall()[0]
    return all_masters


def sql_create_client(id_telegram, fio, phone):
    """ добавить клиента в бд """
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

# id_master, id_client, id_service, date
def sql_add_sale(id_master, id_client, id_service, date):
    """ добавить запись в бд """
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO schedule(id_master, id_client, id_service, date) VALUES('{id_master}', '{id_client}', '{id_service}', '{date}')")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = f"Error add new services schedule: {error}"
        print(error_text)

