from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    Text,
    ForeignKey,
    Boolean,
    Time,
    DateTime,
    Unicode,
)
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal as D
import sqlalchemy.types as types


db = declarative_base()


class SqliteNumeric(types.TypeDecorator):
    """
    Pysql doesn't support the floating point and we need to support it
    to avoid the warning during the tests
    """

    impl = types.String

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.VARCHAR(100))

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return D(value)


class Restaurant(db):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text(100))

    lat = Column(Float)  # restaurant latitude
    lon = Column(Float)  # restaurant longitude

    phone = Column(Integer)
    covid_measures = Column(Text(500))

    # THERE IS NO INTERVAL DATA TYPE IN SQL LITE
    # avg_time = Column(db.Interval())
    # I store the avg time in integer THAT REPRESENTS MINUTES
    avg_time = Column(Integer, default=30)
    rating = Column(Float, default=0.0)

    # resturant owner.
    owner_email = Column(Unicode(128), nullable=False)

    def __init__(self, *args, **kw):
        super(Restaurant, self).__init__(*args, **kw)


class RestaurantTable(db):
    __tablename__ = "restaurant_table"
    id = Column(Integer, primary_key=True, autoincrement=True)

    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    restaurant = relationship(
        "Restaurant", foreign_keys="RestaurantTable.restaurant_id"
    )

    name = Column(Text(100))  # table name

    max_seats = Column(Integer)  # max seats of the table

    available = Column(
        Boolean, default=False
    )  # I don't understand the purpose of this field..


class PhotoGallery(db):
    __tablename__ = "photo_gallery"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text(255))
    caption = Column(Text(200))
    # restaurant
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    restaurant = relationship("Restaurant", foreign_keys="PhotoGallery.restaurant_id")


class OpeningHours(db):
    """
    opening hours
    """

    __tablename__ = "opening_hours"
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"), primary_key=True)
    restaurant = relationship("Restaurant", foreign_keys="OpeningHours.restaurant_id")
    week_day = Column(Integer, primary_key=True)
    open_lunch = Column(Time, default=datetime.utcnow)
    close_lunch = Column(Time, default=datetime.utcnow)
    open_dinner = Column(Time, default=datetime.utcnow)
    close_dinner = Column(Time, default=datetime.utcnow)


class Menu(db):
    # menu
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # restaurant
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    restaurant = relationship("Restaurant", foreign_keys="Menu.restaurant_id")
    #
    cusine = Column(Text(100))
    description = Column(Text(255))


class MenuDish(db):
    # menu dishes
    __tablename__ = "menu_dish"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # restaurant
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    restaurant = relationship("Restaurant", foreign_keys="MenuDish.restaurant_id")
    #
    name = Column(Text(100))
    price = Column(Float())


class MenuPhotoGallery(db):
    # menu photos
    __tablename__ = "menu_photo_gallery"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text(255))
    caption = Column(Text(200))
    # menu reference
    menu_id = Column(Integer, ForeignKey("menu.id"))
    menu = relationship("Menu", foreign_keys="MenuPhotoGallery.menu_id")


class Review(db):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # restaurant
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    restaurant = relationship("Restaurant", foreign_keys="Review.restaurant_id")

    stars = Column(SqliteNumeric())
    review = Column(Text())
    data = Column(DateTime(), default=datetime.now())

    # review, reletion with user table
    reviewer_email = Column(Unicode(128), nullable=False)


def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    db.query = db_session.query_property()
    db.metadata.create_all(bind=engine)

    q = db_session.query(Restaurant).filter(Restaurant.id == 1)
    restaurant = q.first()
    if restaurant is None:
        first_restaurant = Restaurant()
        first_restaurant.name = "Trial Restaurant"
        first_restaurant.phone = 555123456
        first_restaurant.covid_measures = "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        first_restaurant.lat = 43.720586
        first_restaurant.lon = 10.408347
        first_restaurant.owner_email = "ham.burger@email.com"
        db_session.add(first_restaurant)
        db_session.commit()

    q = db_session.query(Restaurant).filter(Restaurant.id == 2)
    restaurant = q.first()
    if restaurant is None:
        first_restaurant = Restaurant()
        first_restaurant.name = "Pepperwood"
        first_restaurant.phone = 555123427
        first_restaurant.covid_measures = "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        first_restaurant.lat = 33.720586
        first_restaurant.lon = 11.408347
        first_restaurant.owner_email = "nick.miller@email.com"
        db_session.add(first_restaurant)
        db_session.commit()

    q = db_session.query(Menu).filter(Menu.id == 1)
    menu = q.first()
    if menu is None:
        first_menu = Menu()
        first_menu.restaurant_id = 2
        first_menu.cusine = "Italian food"
        first_menu.description = "local food"
        db_session.add(first_menu)
        db_session.commit()

    q = db_session.query(Menu).filter(Menu.id == 2)
    menu = q.first()
    if menu is None:
        second_menu = Menu()
        second_menu.restaurant_id = 2
        second_menu.cusine = "Japanese food"
        second_menu.description = "oriental food"
        db_session.add(second_menu)
        db_session.commit()

    return db_session
