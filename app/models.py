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
        self.cursor = database.cursor

    @classmethod
    def all(cls, table, user_id=None, user_type="0"):
        try:
            sql = "SELECT * FROM %s order by id" % (table)
            if cls.conn is None:
                return []
            cls.cursor.execute(sql)
            records = cls.cursor.fetchall()
            return records
        except psycopg2.Error:
            # print(ex)
            cls.conn.rollback()
            return []

    @classmethod
    def find_by_id(cls, table_name, ids, user_id=""):
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
        except Exception:
            # print(ex)
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
        except Exception:
            # print(ex)
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
            found.id = str(record[0])
            found.password = str(record[5])
            found.user_type = str(record[4])
            return found
        except Exception:
            # print("Some stupid error occurs here")
            # print(ex)
            return None

    def get_orders(self):
        try:
            sql = "SELECT * FROM orders WHERE user_id = '%s' order by id" % (
                self.id
            )
        except Exception:
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
        self.quantity = 1

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
        except Exception:
            # print(ex)
            self.conn.rollback()
            return False

    @classmethod
    def format(cls, menu):
        menus = Menu(menu[1], menu[2], menu[3])
        menus.id = menu[0]
        return menus.json, menus

    @classmethod
    def all(cls, user_id=None, user_type='0', **kwargs):
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
    def find_by_id(cls, table_name="", meal_id="", user_id=None):
        """Find a meal by a meal_id"""
        menu_item = super(Menu, cls).find_by_id("meals", meal_id, user_id)
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
            self.conn.commit()
            return True
        except psycopg2.Error:
            # print(ex)
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
        self.total = 0.00

    def save(self):
        try:
            sql1 = "SELECT MAX(id) FROM orders"
            sql = "INSERT INTO orders(reference, user_id, date_ordered, address_id, status)VALUES" \
                  " ('%s', '%s', now(), '%s' ,'%s')" % (
                      self.reference,
                      self.customer_id,
                      self.address,
                      self.status
                  )
            if self.conn is None:
                return False
            self.cursor.execute(sql1)
            nexter = self.cursor.fetchone()
            num = 1
            if not nexter:
                num = 1
            else:
                num = nexter[0]
            self.cursor.execute(sql)
            if num is None:
                self.conn.commit()
                self.cursor.execute(sql1)
                nexter = self.cursor.fetchone()
                num = nexter[0]
            print(num, "Something here")
            num = (int(num) + 1) if (num != 1 or num is None) else num
            for item in self.items:
                sql_individual = "INSERT INTO order_meals(meal_id, order_id, quantity, cost) VALUES ('%s', '%s', '%s', '%s')" % (
                    item.id,
                    num,
                    item.quantity,
                    item.price
                )
                self.cursor.execute(sql_individual)
            self.conn.commit()
            return True
        except psycopg2.Error as ex:
            print(ex)
            self.conn.rollback()
            return False

    @classmethod
    def format(cls, order):
        """Format an order"""
        try:
            order_gotten = Order(order[2], order[3], order[4])
            order_gotten.date_ordered = order[3]
            order_gotten.id = order[0]
            order_gotten.total = cls.get_total(order_gotten.id)
            print(order_gotten.id)
            return order_gotten
        except IndexError:
            return None

    @classmethod
    def all(cls, table="orders", user_id="", user_type='0'):
        """Get all orders"""
        records = super(Order, cls).all(table, user_id=user_id, user_type=user_type)
        res = []
        if int(user_type) == 0:
            records = [cls.format(record) for record in records]
            return records
        for record in records:
            if int(record[2]) == int(user_id):
                res.append(cls.format(record))
        if not res:
            return []
        return res

    @classmethod
    def get_total(cls, order_id):
        """Get the total value of an order given the id"""
        try:
            sql = "SELECT sum(cost * quantity) FROM order_meals WHERE order_id='%s'" % (
                order_id
            )
            if cls.conn is None:
                return 0.00
            cls.cursor.execute(sql)
            record = cls.cursor.fetchone()
            if not record:
                return 0.00
            return record[0]
        except Exception:
            return 0.00

    @classmethod
    def find_by_id(cls, table_name="orders", ids="", user_id=""):
        """Get an order given the id"""
        order = super(Order, cls).find_by_id(table_name, ids, user_id)
        if not order:
            return None
        order = cls.format(order)
        # print(order.customer_id)
        if not str(user_id).isnumeric():
            return []
        if user_id == '1' or user_id == 1:
            user_id = 1
        user = User.find_by_id("users", ids=1)
        if not user:
            return []
        if user[4] == '0' or user[4] == 0:
            return order
        if int(user_id) != int(order.customer_id):
            return []
        return order
    @property
    def json(self):
        """Return a json serializable version of the order"""
        return {
            "id": str(self.id),
            "reference": str(self.reference),
            "date_ordered": str(self.date_ordered),
            "value": str(self.total),
            "status": str(self.status)
        }

    @property
    def json1(self):
        """Return a json serializable version of the order"""
        return {
            "reference": str(self.reference),
            "status": str(self.status),
            "date_ordered": str(self.date_ordered),
            "items": Order.get_items(order_id=self.id),
            "total": self.get_total(self.id)
        }

    @classmethod
    def get_items(cls, order_id):
        """Get the total value of an order given the id"""
        try:
            sql = "SELECT * FROM order_meals WHERE order_id='%s'" % (
                order_id
            )
            if cls.conn is None:
                return 0.00
            cls.cursor.execute(sql)
            record = cls.cursor.fetchall()
            if not record:
                return 0.00
            record = list(record)
            res = []
            for item in record:
                res.append(cls.format_menu_order(item))
            return res
        except Exception as ex:
            print(ex)
            return []

    @classmethod
    def format_menu_order(cls, menu_order):
        return {
            "menu_item": Menu.find_by_id(meal_id=menu_order[1]).name,
            "quantity": menu_order[3],
            "unit_price": menu_order[4]
        }


class Address(Base):
    def __init__(self, town, street, phone):
        """The constructor for the addresses class"""
        super(Address, self).__init__()
        self.id = None
        self.town = town
        self.street = street
        self.phone = phone
        self.user_id = None

    @classmethod
    def find_by_id(cls, table_name="addresses", address_id="", user_id=""):
        """Find an address by a given if"""
        address = super(Address, cls).find_by_id(
            table_name="addresses", ids=address_id)
        if not address:
            return []
        new_add = cls.format(address)
        if new_add is None:
            return []
        print(new_add)
        if int(new_add.user_id) != int(user_id):
            return []
        return address

    def save(self, user_id=""):
        """Save the address to the database"""
        try:
            sql = "INSERT INTO addresses(user_id, town, phone, street)values('%s', '%s', '%s', '%s')" % (
                user_id,
                self.town,
                self.phone,
                self.street
            )
            if self.conn is None:
                return False
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception:
            # print(ex)
            return False

    @classmethod
    def format(cls, fields):
        """Format the address to an object"""
        address = Address(fields[2], fields[3], fields[4])
        address.id = fields[0]
        address.user_id = fields[1]
        return address

    @property
    def json(self):
        """Return json serializable properties without id"""
        return {"town": self.town, "street": self.street, "phone": self.phone}

    @property
    def json1(self):
        """Return JSON serializable properties without id"""
        return {"id": self.id, "town": self.town, "street": self.street, "phone": self.phone}

    @classmethod
    def all(cls, table_name="addresses", user_id="0", user_type='0'):
        """Return all the addresses for a specific user"""
        records = super(Address, cls).all("addresses", user_id=user_id)
        if not records:
            return []
        res = []
        for record in records:
            if int(record[1]) == int(user_id):
                res.append(cls.format(fields=record))
        return res
