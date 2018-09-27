from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os


class SQLs(object):
    def __init__(self):
        self.users_sql = """
           CREATE TABLE if not exists users(
           id serial primary key , 
           username varchar(25) not null , 
           fullnames varchar(75) not null,
           password varchar(140) not null ,
           unique(username))
        """
        self.address_sql = """
           CREATE TABLE if not exists addresses(
           id serial primary key,
           user_id integer not null,
           town varchar(60) not null,
           phone varchar(14) not null,
           foreign key(user_id) references users(id) on delete cascade on update cascade
           )
        """
        self.meal_sql = """
                        CREATE TABLE if not exists meals(
                        id SERIAL PRIMARY KEY, 
                        name varchar(26) NOT NULL, 
                        description varchar(100) not null,
                        price decimal not null,
                        date_added timestamp default now(),
                        unique(name)
                        );"""
        self.order_sql = """
                         CREATE TABLE if not exists orders(
                         id SERIAL PRIMARY KEY, 
                         user_id integer not null ,
                         date_ordered timestamp not null ,
                         address_id integer not null,
                         status varchar(20) not null,
                         cancelled boolean default false,
                         FOREIGN KEY(user_id) REFERENCES users(id) on update cascade,
                         FOREIGN KEY(address_id) REFERENCES addresses(id) on update cascade)
                         """
        self.order_meals_sql = """
                          CREATE TABLE if not exists order_meals(
                          id serial primary key, 
                          meal_id integer not null,
                          order_id integer not null,
                          foreign key(order_id) REFERENCES orders(id) ON DELETE CASCADE on update cascade,
                          foreign key(meal_id) REFERENCES meals(id))
                           """


class Database(SQLs):

    def __init__(self):
        super(Database, self).__init__()
        self.username = os.getenv("DB_USER", None)
        self.db = os.getenv("DB_FAST_FOOD_TEST", None)
        self.host = os.getenv("DB_HOST", None)
        self.password = os.getenv("DB_PASSWORD", None)
        self.connection = connect(host=self.host,
                                  port=5432,
                                  database=self.db,
                                  user=self.username,
                                  password=self.password)
        self.cursor = self.connection.cursor()

    def create_meals_table(self):
        try:
            self.cursor.execute(self.meal_sql)
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()

    def create_orders_table(self):
        try:
            self.cursor.execute(self.order_sql)
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()

    def create_order_products_table(self):
        try:
            self.cursor.execute(self.order_meals_sql)
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()

    def create_users_table(self):
        try:
            self.cursor.execute(self.users_sql)
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()

    def create_addresses_table(self):
        if self.connection is None:
            return False
        try:
            self.cursor.execute(self.address_sql)
            self.connection.commit()
            return True
        except Exception as ex:
            return False

    def create_tables(self):
        self.create_users_table()
        self.create_addresses_table()
        self.create_meals_table()
        self.create_orders_table()
        self.create_order_products_table()

    def drop_tables(self):
        try:
            drop_order_sql = "DROP TABLE if exists orders CASCADE"
            drop_users_sql = "DROP TABLE if exists users cascade "
            drop_meals_sql = "DROP TABLE if exists meals cascade "
            drop_order_meals_sql = "DROP TABLE if exists order_meals cascade "
            if self.connection is None:
                return
            self.cursor.execute(drop_meals_sql)
            self.cursor.execute(drop_order_meals_sql)
            self.cursor.execute(drop_order_sql)
            self.cursor.execute(drop_users_sql)
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()


database = Database()
