from flask import current_app
from database import (
    Restaurant,
    Menu,
    MenuDish,
    OpeningHours,
    RestaurantTable,
    PhotoGallery,
    Review,
    MenuPhotoGallery,
)

from flask import current_app

import datetime
from sqlalchemy.sql.expression import func

from decimal import Decimal


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
    def get_restaurant_with_info(db_session, r_name, r_phone, r_lat, r_lon):
        """
        Method to return if a restaurant with name, phone, latitude and longitude
        specified already exists
        """
        restaurant = (
            db_session.query(Restaurant)
            .filter(
                Restaurant.name == r_name,
                Restaurant.phone == r_phone,
                Restaurant.lat == r_lat,
                Restaurant.lon == r_lon,
            )
            .first()
        )
        if restaurant is None:
            # the restaurant doesn't exist
            return False
        else:
            # the restaurant already exists
            return True

    @staticmethod
    def get_restaurants_by_keyword_name(db_session, name):
        """
        Method to return the restaurant inside the database using name as keyword
        """
        restaurant = (
            db_session.query(Restaurant)
            .filter(Restaurant.name.ilike("%{}%".format(name)))
            .all()
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
    def get_menu(db_session, menu_id):
        """
        Method to return the restaurant inside the database with the specified id
        """
        menu = db_session.query(Menu).filter(Menu.id == menu_id).first()
        return menu

    @staticmethod
    def get_menu_photos(db_session, menu_id):
        """
        Method to return photos of the specified restaurant
        """
        photos = (
            db_session.query(MenuPhotoGallery)
            .filter(menu_id == MenuPhotoGallery.menu_id)
            .all()
        )
        return photos

    @staticmethod
    def get_menu_photo_with_url(db_session, url):
        """
        Method to return photos with a specified URL
        """
        photo = (
            db_session.query(MenuPhotoGallery)
            .filter(url == MenuPhotoGallery.url)
            .first()
        )
        return photo

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
        photos = (
            db_session.query(PhotoGallery)
            .filter(restaurant_id == PhotoGallery.restaurant_id)
            .all()
        )
        return photos

    @staticmethod
    def get_photo_with_url(db_session, url):
        """
        Method to return photos of the specified restaurant using url
        """
        photo = db_session.query(PhotoGallery).filter(url == PhotoGallery.url).all()
        return photo

    @staticmethod
    def get_reviews(db_session, restaurant_id):
        """
        Method to return photos of the specified restaurant
        """
        review = (
            db_session.query(Review).filter(restaurant_id == Review.restaurant_id).all()
        )
        return review

    @staticmethod
    def get_reviews_random(db_session, restaurant_id, number):
        """
        Method to return random reviews of the specified restaurant 
        """
        reviews = (
            db_session.query(Review)
            .filter(restaurant_id == Review.restaurant_id)
            .order_by(func.random())
            .limit(number)
            .all()
        )

        return reviews

    @staticmethod
    def delete_dish(dish_id):
        db_session = current_app.config["DB_SESSION"]
        db_session.query(MenuDish).filter_by(id=dish_id).delete()
        db_session.commit()
        return True

    @staticmethod
    def delete_table(db_session, table_id):
        db_session.query(RestaurantTable).filter_by(id=table_id).delete()
        db_session.commit()
        return True

    @staticmethod
    def create_restaurant(db_session, data, max_seats):
        """
        Method to create a restaurant
        """

        # add in restaurant table
        new_restaurant = Restaurant()
        new_restaurant.name = data["restaurant"]["name"]
        new_restaurant.lat = data["restaurant"]["lat"]
        new_restaurant.lon = data["restaurant"]["lon"]
        new_restaurant.phone = data["restaurant"]["phone"]
        new_restaurant.covid_measures = data["restaurant"]["covid_measures"]
        new_restaurant.avg_time = data["restaurant"]["avg_time"]
        new_restaurant.rating = data["restaurant"]["rating"]
        new_restaurant.owner_email = data["restaurant"]["owner_email"]

        db_session.add(new_restaurant)
        db_session.commit()

        # add tables in RestaurantTable table
        number_tables = data["restaurant_tables"]
        for i in range(number_tables):
            RestaurantService.create_table(db_session, "", max_seats, new_restaurant.id)

        # insert opening hours
        list_openings = data["opening"]
        for opening in list_openings:
            new_opening = OpeningHours()
            new_opening.restaurant_id = new_restaurant.id
            new_opening.week_day = opening["week_day"]

            time_info = opening["open_lunch"].split(":")
            new_opening.open_lunch = datetime.time(int(time_info[0]), int(time_info[1]))
            time_info = str(opening["close_lunch"]).split(":")
            new_opening.close_lunch = datetime.time(
                int(time_info[0]), int(time_info[1])
            )
            time_info = str(opening["open_dinner"]).split(":")
            new_opening.open_dinner = datetime.time(
                int(time_info[0]), int(time_info[1])
            )
            time_info = str(opening["close_dinner"]).split(":")
            new_opening.close_dinner = datetime.time(
                int(time_info[0]), int(time_info[1])
            )

            db_session.add(new_opening)
            db_session.commit()

        # insert menus
        for menu in data["menu"]:
            new_menu = Menu()
            new_menu.restaurant_id = new_restaurant.id
            new_menu.cusine = menu
            new_menu.description = ""

            db_session.add(new_menu)
            db_session.commit()

    @staticmethod
    def create_table(db_session, name, max_seats, restaurant_id):
        new_table = RestaurantTable()
        new_table.restaurant_id = restaurant_id
        new_table.name = name
        new_table.max_seats = max_seats
        new_table.available = True

        db_session.add(new_table)
        db_session.commit()

    @staticmethod
    def get_rating_restaurant(restaurant_id: int) -> float:
        """
        get avg of rating for a restaurant
        This method perform the request to calculate the rating of the restaurants
        with the review.
        :param restaurant_id: the restaurant id
        :return: the rating value, as 0.0 or 5.0
        """
        db_session = current_app.config["DB_SESSION"]
        rating_value = 0.0
        restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).first()
        if restaurant is None:
            raise Exception(
                "Restaurant with id {} don't exist on database".format(restaurant_id)
            )
        reviews_list = (
            db_session.query(Review).filter_by(restaurant_id=restaurant_id).all()
        )
        if (reviews_list is None) or (len(reviews_list) == 0):
            return rating_value

        for review in reviews_list:
            rating_value = rating_value + float(review.stars)

        rating_value = rating_value / float(len(reviews_list))
        current_app.logger.debug(
            "Rating calculate for restaurant with name {} is {}".format(
                restaurant.name, rating_value
            )
        )
        restaurant.rating = Decimal(rating_value)
        db_session.commit()
        return rating_value

    @staticmethod
    def calculate_rating_for_all_restaurant():
        """
        This method is used inside celery background task to calculate the rating for each restaurants
        """
        db_session = current_app.config["DB_SESSION"]
        restaurants_list = db_session.query(Restaurant).all()
        for restaurant in restaurants_list:
            RestaurantService.get_rating_restaurant(restaurant.id)
        return True

    @staticmethod
    def update_restaurant_info():
        """
        update the restaurant infos
        """
        pass

    @staticmethod
    def create_dish(db_session, name, price, restaurant_id):
        new_dish = MenuDish()
        new_dish.restaurant_id = restaurant_id
        new_dish.name = name
        new_dish.price = price

        db_session.add(new_dish)
        db_session.commit()

    @staticmethod
    def create_restaurant_photo(db_session, url, caption, restaurant_id):
        new_photo = PhotoGallery()
        new_photo.restaurant_id = restaurant_id
        new_photo.url = url
        new_photo.caption = caption

        db_session.add(new_photo)
        db_session.commit()

    @staticmethod
    def create_review(db_session, review, stars, reviewer_email, restaurant_id):
        new_review = Review()
        new_review.restaurant_id = restaurant_id
        new_review.review = review
        new_review.stars = stars
        new_review.reviewer_email = reviewer_email

        db_session.add(new_review)
        db_session.commit()

    @staticmethod
    def create_menu_photo(db_session, url, caption, menu_id):
        new_photo = MenuPhotoGallery()
        new_photo.menu_id = menu_id
        new_photo.url = url
        new_photo.caption = caption

        db_session.add(new_photo)
        db_session.commit()
