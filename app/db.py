import os
import psycopg2

from psycopg2 import connect


class SQLs(object):
    """A class to hold sql statements"""

    def __init__(self):
        """Constructor for the SQL class"""
        self.users_sql = """
           CREATE TABLE if not exists users(
           id serial primary key , 
           username varchar(25) not null , 
           fullnames varchar(75) not null,
           email varchar(100) not null,
           user_type integer not null default 1,
           password varchar(140) not null ,
           unique(username),
           unique(email))
        """
        self.address_sql = """
           CREATE TABLE if not exists addresses(
           id serial primary key,
           user_id integer not null,
           town varchar(60) not null,
           phone varchar(14) not null,
           street varchar(60) not null,
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
                         reference varchar(100) not null,
                         user_id integer not null ,
                         date_ordered timestamp not null ,
                         address_id integer not null,
                         status varchar(20) not null,
                         cancelled boolean default false,
                         unique(reference),
                         FOREIGN KEY(user_id) REFERENCES users(id) on update cascade,
                         FOREIGN KEY(address_id) REFERENCES addresses(id) on update cascade)
                         """
        self.order_meals_sql = """
                          CREATE TABLE if not exists order_meals(
                          id serial primary key, 
                          meal_id integer not null,
                          order_id integer not null,
                          quantity integer not null,
                          cost integer not null,
                          foreign key(order_id) REFERENCES orders(id) ON DELETE CASCADE on update cascade,
                          foreign key(meal_id) REFERENCES meals(id))
                           """


class Database(SQLs):
    """The database class where everything creating schemas happen"""

    def __init__(self):
        super(Database, self).__init__()
        self.username = os.getenv("DB_USER", None)
        self.database = os.getenv("DB_NAME", "fast_food")
        self.host = os.getenv("DB_HOST", None)
        self.port = os.getenv("DB_PORT", 5432)
        self.password = os.getenv("DB_PASSWORD", None)
        try:
            self.connection = connect(host=self.host,
                                  port=self.DB_PORT,
                                  database=self.database,
                                  user=self.username,
                                  password=self.password)
        except Exception as ex:
            self.connection = None
            print(ex)
        if self.connection:
            self.cursor = self.connection.cursor()
        else:
            self.connection = None
            self.cursor = None

    def create_meals_table(self):
        """A method to create the meals table"""
        try:
            if not self.cursor:
                return
            self.cursor.execute(self.meal_sql)
            self.connection.commit()
        except (psycopg2.Error, Exception):
            # print(ex)
            self.connection.rollback()

    def create_orders_table(self):
        """A method to create the orders table"""
        try:
            if not self.cursor:
                return
            self.cursor.execute(self.order_sql)
            self.connection.commit()
        except psycopg2.Error:
            # print(ex)
            self.connection.rollback()

    def create_order_products_table(self):
        """A method to create the order_products table"""
        try:
            if not self.cursor:
                return
            self.cursor.execute(self.order_meals_sql)
            self.connection.commit()
        except (psycopg2.Error, Exception):
            # print(ex)
            self.connection.rollback()

    def create_users_table(self):
        """A method to create the users table"""
        try:
            if not self.cursor:
                return
            self.cursor.execute(self.users_sql)
            self.connection.commit()
        except (Exception, psycopg2.Error):
            # print(ex)
            self.connection.rollback()

    def create_addresses_table(self):
        """A method to create the addresses table"""
        if self.connection is None:
            return False
        try:
            self.cursor.execute(self.address_sql)
            self.connection.commit()
            return True
        except (psycopg2.Error, Exception):
            # print(ex)
            return False

    def create_tables(self):
        """A method to call all methods creating tables"""
        self.create_users_table()
        self.create_addresses_table()
        self.create_meals_table()
        self.create_orders_table()
        self.create_order_products_table()

    def drop_tables(self):
        """A method to drop all tables"""
        try:
            drop_order_sql = "DROP TABLE if exists orders CASCADE"
            drop_users_sql = "DROP TABLE if exists users cascade "
            drop_meals_sql = "DROP TABLE if exists meals cascade "
            drop_order_meals_sql = "DROP TABLE if exists order_meals cascade "
            drop_address_sql = "DROP TABLE if exists addresses cascade "
            if self.connection is None:
                return
            self.cursor.execute(drop_meals_sql)
            self.cursor.execute(drop_order_meals_sql)
            self.cursor.execute(drop_order_sql)
            self.cursor.execute(drop_users_sql)
            self.cursor.execute(drop_address_sql)
            self.connection.commit()
        except (psycopg2.Error, Exception):
            # print(ex)
            self.connection.rollback()

    def create_default_admin(self, fullnames="Silas Kenneth", username="silaskenny", email="silaskenny@gmail.com",
                             password="SilasK@2019"):
        """Create the default user"""
        from app.models import User
        user = User(fullnames, username, password, email)
        user.user_type = 0
        user.save()


database = Database()
