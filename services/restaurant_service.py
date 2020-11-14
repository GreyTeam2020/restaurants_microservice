from flask import current_app
from database import (
    Restaurant,
    Menu
)



class RestaurantService:
    """
    This services give the possibility to isolate all the operations
    about the restaurants with the database
    """


    @staticmethod
    def get_all_restaurants(db_session):
        """
        Method to return a list of all restaurants inside the database
        """
        all_restaurants = db_session.query(Restaurant).all()
        return all_restaurants


    @staticmethod
    def get_restaurant(db_session, restaurant_id):
        """
        Method to return the restaurant inside the database with the specified id
        """
        restaurant = db_session.query(Restaurant).filter(
            Restaurant.id == restaurant_id
        ).first()
        return restaurant


    @staticmethod
    def get_menus(db_session, restaurant_id):
        """
        Method to return the restaurant inside the database with the specified id
        """
        menus = db_session.query(Menu).filter(
            restaurant_id == Menu.restaurant_id
        ).all()

        return menus

