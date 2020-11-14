from flask import current_app
from database import (
    Restaurant,
    Menu,
    MenuDish,
    OpeningHours,
    RestaurantTable,
    PhotoGallery,
    Review,
    MenuPhotoGallery
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
        restaurant = (
            db_session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        )
        return restaurant

    @staticmethod
    def get_menus(db_session, restaurant_id):
        """
        Method to return menus of the specified restaurant 
        """
        menus = db_session.query(Menu).filter(restaurant_id == Menu.restaurant_id).all()
        return menus

    @staticmethod
    def get_menu_photos(db_session, menu_id):
        """
        Method to return photos of the specified restaurant 
        """
        tables = (
            db_session.query(MenuPhotoGallery).filter(menu_id == MenuPhotoGallery.menu_id).all()
        )
        return tables

    @staticmethod
    def get_dishes(db_session, restaurant_id):
        """
        Method to return dishes of the specified restaurant 
        """
        dishes = (
            db_session.query(MenuDish)
            .filter(restaurant_id == MenuDish.restaurant_id)
            .all()
        )
        return dishes

    @staticmethod
    def get_openings(db_session, restaurant_id):
        """
        Method to return opening hours of the specified restaurant 
        """
        openings = (
            db_session.query(OpeningHours)
            .filter(restaurant_id == OpeningHours.restaurant_id)
            .all()
        )
        return openings

    @staticmethod
    def get_tables(db_session, restaurant_id):
        """
        Method to return tables of the specified restaurant 
        """
        tables = (
            db_session.query(RestaurantTable)
            .filter(restaurant_id == RestaurantTable.restaurant_id)
            .all()
        )
        return tables

    @staticmethod
    def get_photos(db_session, restaurant_id):
        """
        Method to return photos of the specified restaurant 
        """
        tables = (
            db_session.query(PhotoGallery)
            .filter(restaurant_id == PhotoGallery.restaurant_id)
            .all()
        )
        return tables

    @staticmethod
    def get_reviews(db_session, restaurant_id):
        """
        Method to return photos of the specified restaurant 
        """
        tables = (
            db_session.query(Review).filter(restaurant_id == Review.restaurant_id).all()
        )
        return tables
