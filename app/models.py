import uuid
import datetime
from werkzeug.security import generate_password_hash
from app.db import database
from app.utils import decode_token as claims
import psycopg2


class Base(object):
    conn = database.connection
    cursor = database.cursor

    def __init__(self):
        self.conn = database.connection
        print(self.conn)
        self.cursor = database.cursor

    @classmethod
    def all(cls, table, token=None):
        try:
            sql = "SELECT * FROM %s order by id" % (table)
            if cls.conn is None:
                return []
            cls.cursor.execute(sql)
            records = cls.cursor.fetchall()
            return records
        except psycopg2.Error as ex:
            print(ex)
            cls.conn.rollback()
            return []

    @classmethod
    def find_by_id(cls, table_name, ids, token=None):
        try:
            if not str(ids).isnumeric():
                return []
            ids = int(ids)
            sql = "SELECT * FROM %s WHERE id = %d" % (table_name, ids)
            if cls.conn is None:
                return []
            cls.cursor.execute(sql)
            record = cls.cursor.fetchone()
            return record
        except Exception as ex:
            print(ex)
            return []


class User(Base):

    def __init__(self, fullnames, username, password, email):
        super(User, self).__init__()
        self.id = None
        self.fullnames = fullnames
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.addresses = []
        self.orders = []
        self.user_type = 1

    def save(self):
        try:
            fullnames = self.fullnames
            username = self.username
            password = self.password
            email = self.email
            user_type = self.user_type
            sql = "INSERT INTO users(fullnames, username, email, password, user_type)values('%s', '%s', '%s', '%s', '%s')" % \
                  (
                      fullnames,
                      username,
                      email,
                      password,
                      user_type
                  )
            if self.conn is None:
                return False
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as ex:
            print(ex)
            self.conn.rollback()
            return False

    @property
    def json(self):
        """Make the user object JSON serializable"""
        return {
            "id": self.id,
            "fullnames": self.fullnames,
            "username": self.username,
            "email": self.email,
            "user_type": "admin" if self.user_type == '0' else "normal"
        }
    @property
    def json1(self):
        """Remove the id field from the serializable version"""
        return {
            "fullnames": self.fullnames,
            "username": self.username,
            "email": self.email,
            "user_type": "admin" if self.user_type == 0 else "normal"
        }

    @classmethod
    def get_by_username_or_email(cls, username):
        """Get a user by email or username"""
        try:
            sql = "SELECT * FROM users WHERE username = '%s' or email = '%s'" % (
                username,
                username
            )
            if cls.conn is None:
                return None
            cls.cursor.execute(sql)
            record = cls.cursor.fetchone()
            if not record:
                return None
            found = User(
                username=str(record[1]),
                password=str(record[5]),
                email=str(record[3]),
                fullnames=str(record[2])
            )
            # print(found)
            found.id = str(record[0])
            found.password = str(record[5])
            found.user_type = str(record[4])
            return found
        except Exception as ex:
            # print("Some stupid error occurs here")
            print(ex)
            return None

    def get_orders(self):
        try:
            sql = "SELECT * FROM orders WHERE user_id = '%s' order by id" % (
                self.id
            )
        except Exception as ex:
            return {}


class Menu(Base):
    def __init__(self, name, description, price):
        """
        The class constructor for the menu model
        :param name:
        :param description:
        :param price:
        """
        super(Menu, self).__init__()
        self.id = None
        self.name = name
        self.description = description
        self.price = price
        self.date_added = datetime.datetime.utcnow()

    def save(self):
        """Save a menu item to the database
        :rtype: Boolean
        """
        try:
            sql = "INSERT INTO meals(name, description, price)values('%s', '%s', '%s')" \
                  % (
                      self.name,
                      self.description,
                      self.price
                  )
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as ex:
            # print(ex)
            self.conn.rollback()
            return False

    @classmethod
    def format(cls, menu):
        menus = Menu(menu[1], menu[2], menu[3])
        menus.id = menu[0]
        return menus.json, menus

    @classmethod
    def all(cls, token=None, **kwargs):
        items = super(Menu, cls).all("meals")
        res = []
        for item in items:
            res.append(cls.format(item)[0])
        return res

    @property
    def json(self):
        return {
            "menu_id": str(self.id),
            "name": self.name,
            "description": self.description,
            "price": str(self.price)
        }

    @property
    def json1(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": str(self.price)
        }

    @classmethod
    def find_by_id(cls, table_name="", meal_id="", token=None):
        """Find a meal by a meal_id"""
        menu_item = super(Menu, cls).find_by_id("meals", meal_id, token)
        if not menu_item:
            return None
        return cls.format(menu_item)[-1]

    def update(self):
        try:
            sql = "UPDATE meals SET name= '%s', description='%s', price='%s' WHERE id = '%s'" % (
                self.name,
                self.description,
                self.price,
                self.id
            )
            if self.conn is None:
                return False
            self.cursor.execute(sql)
            return True
        except psycopg2.Error as ex:
            print(ex)
            self.conn.rollback()
            return False


class Order(Base):
    """The order class which represents an order"""
    def __init__(self, customer_id, address_id, items):
        """Constructor for the Order class"""
        super(Order, self).__init__()
        self.id = None
        self.reference = uuid.uuid4()
        self.customer_id = customer_id
        self.items = items
        self.address = address_id
        self.date_ordered = datetime.datetime.utcnow()
        self.status = "pending"

    def save(self):
        try:
            sql = "INSERT INTO orders(reference, customer_id, date_ordered, status)VALUES" \
                  " ('%s', '%s', '%s', '%s')" % (
                      self.reference,
                      self.customer_id,
                      self.date_ordered,
                      self.status
                  )
            if self.conn is None:
                return False
            self.cursor.execute(sql)
            nexter = self.next_id()
            for item in self.items:
                sql_indivi = "INSERT INTO order_meals(meal_id, order_id) VALUES ('%s', '%s')" % (
                    item.id,
                    nexter
                )
                self.cursor.execute(sql_indivi)
            self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            return False

    @classmethod
    def all(cls, table="orders", token=""):
        records = super(Order, cls).all(table)
        who = claims(token)
        if not who:
            return []
        res = []
        if who.get("user_type", "") == "admin":
            return records
        for record in records:
            if record[1] == who.get("id", 0):
                res.append(record)
        if not res:
            return []
        print(res)
        return res

    @classmethod
    def find_by_id(cls, table_name="orders", ids="", token=""):
        order = super(Order, cls).find_by_id(table_name, ids, token)
        if not order:
            return {}
        return {}

    @classmethod
    def next_id(cls):
        try:
            sql = "SELECT nextval(id) FROM users"
            if cls.conn is None:
                return 1
            cls.cursor.execute(sql)
            res = cls.cursor.fetchone()
            if not res:
                return 1
            return res[0]
        except Exception as ex:
            return 1


class Address(Base):
    def __init__(self, town, street, phone):
        super(Address, self).__init__()
        self.id = None
        self.town = town
        self.street = street
        self.phone = phone
        self.user_id = None

    @classmethod
    def find_by_id(cls, table_name="addresses", address_id="", token=None):
        address = super(Address, cls).find_by_id(
            table_name="addresses", ids=address_id, token=token)
        who_this_is = claims(token)
        return address
    def save(self, token=""):
        """Save the address to the database"""
        try:
            sql = "INSERT INTO addresses(user_id, town, phone, street)values('%s', '%s', '%s')"%(
                self.user_id,
                self.town,
                self.phone,
                self.street
            )
            if self.conn is None:
                return False
            self.cursor.execute(sql)

        except Exception as ex:
            return False
