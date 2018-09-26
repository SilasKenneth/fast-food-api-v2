import uuid
import datetime
from werkzeug.security import generate_password_hash
from app.db import database


class Base(object):
    conn = database.connection
    cursor = database.cursor

    @classmethod
    def all(cls, table):
        try:
            sql = "SELECT * FROM %s" % (table)
            if cls.conn is None:
                return []
            cls.cursor.execute(sql)
            records = cls.cursor.fetchall()
            return records
        except Exception as ex:
            cls.conn.rollback()
            return []


class User(Base):

    def __init__(self, username, password, email):
        super(User, self).__init__()
        self.id = None
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        try:
            username = self.username
            password = self.password
            email = self.email
            sql = "INSERT INTO users(username, email, password)values('%s', '%s', '%s')" % (username, email, password)
            if self.conn is None:
                return False
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as ex:
            self.conn.rollback()
            return False


class Menu(Base):
    def __init__(self, name, description, price):
        super(Menu, self).__init__()
        self.id = None
        self.name = name
        self.description = description
        self.price = price
        self.date_added = datetime.datetime.utcnow()

    def save(self):
        try:
            sql = "INSERT INTO meals(name, description, price)values('%s', '%s', '%s')" % (
                self.name,
                self.description,
                self.price
            )
            self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as ex:
            print(ex)
            self.conn.rollback()
            return False

    @classmethod
    def get_by_id(cls, meal_id):
        try:
            pass
        except Exception as ex:
            pass

    @classmethod
    def all(cls):
        return super(Menu, cls).all("meals")
    @property
    def json(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price
        }


class Order(Base):
    def __init__(self, customer_id, items):
        super(Order, self).__init__()
        self.id = None
        self.reference = uuid.uuid4()
        self.customer_id = customer_id
        self.items = self.items
        self.date_ordered = datetime.datetime.utcnow()
        self.status = "pending"

    def save(self):
        try:
            sql = "INSERT INTO orders(reference, customer_id, date_ordered, status)VALUES ('%s', '%s', '%s', '%s')" % (
                self.reference,
                self.customer_id,
                self.date_ordered,
                self.status
            )
            if self.conn is None:
                return False
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            return False

    @classmethod
    def all(cls):
        return super(Order, cls).all("orders")
