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

import datetime
from sqlalchemy.sql.expression import func

from decimal import Decimal


class RestaurantService:
    """
    This services give the possibility to isolate all the operations
    about the restaurants with the database
    """

    @staticmethod
    def get_all_restaurants():
        """
        This method returns a list of all restaurants inside the database
        """
        db_session = current_app.config["DB_SESSION"]
        all_restaurants = db_session.query(Restaurant).all()
        return all_restaurants

    @staticmethod
    def get_restaurant(restaurant_id):
        """
        This method returns the restaurant inside the database with the specified id
        """
        db_session = current_app.config["DB_SESSION"]
        restaurant = (
            db_session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        )
        return restaurant

    @staticmethod
    def get_restaurant_with_info(r_name, r_phone, r_lat, r_lon):
        """
        This method returns if a restaurant with name, phone, latitude and longitude
        specified already exists
        """
        db_session = current_app.config["DB_SESSION"]
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
        return restaurant

    @staticmethod
    def get_restaurants_by_owner_email(owner_email):
        """
        This method returns if a restaurant with name, phone, latitude and longitude
        specified already exists
        """
        db_session = current_app.config["DB_SESSION"]
        restaurant = db_session.query(Restaurant).filter(
                Restaurant.owner_email == owner_email
            ).first()
        
        if restaurant is not None:
            return restaurant
        else:
            return None

    @staticmethod
    def get_restaurants_by_keyword_name(name):
        """
        This method returnsthe restaurant inside the database using name as keyword
        """
        db_session = current_app.config["DB_SESSION"]
        restaurant = (
            db_session.query(Restaurant)
            .filter(Restaurant.name.ilike("%{}%".format(name)))
            .all()
        )
        return restaurant

    @staticmethod
    def get_menus(restaurant_id):
        """
        This method returns menus of the specified restaurant
        """
        db_session = current_app.config["DB_SESSION"]
        menus = db_session.query(Menu).filter(restaurant_id == Menu.restaurant_id).all()
        return menus

    @staticmethod
    def get_menu(menu_id):
        """
        This method returns the menu with the id specified
        """
        db_session = current_app.config["DB_SESSION"]
        menu = db_session.query(Menu).filter(Menu.id == menu_id).first()
        return menu

    @staticmethod
    def get_menu_photos(menu_id):
        """
        This method returnsphotos of the specified menu
        """
        db_session = current_app.config["DB_SESSION"]
        photos = (
            db_session.query(MenuPhotoGallery)
            .filter(menu_id == MenuPhotoGallery.menu_id)
            .all()
        )
        return photos

    @staticmethod
    def get_menu_photo_with_url(url):
        """
        This method returns photos about menu with a specified URL
        """
        db_session = current_app.config["DB_SESSION"]
        photo = (
            db_session.query(MenuPhotoGallery)
            .filter(url == MenuPhotoGallery.url)
            .first()
        )
        return photo

    @staticmethod
    def get_dishes(restaurant_id):
        """
        This method returns dishes of the specified restaurant
        """
        db_session = current_app.config["DB_SESSION"]
        dishes = (
            db_session.query(MenuDish)
            .filter(restaurant_id == MenuDish.restaurant_id)
            .all()
        )
        return dishes

    @staticmethod
    def get_openings(restaurant_id):
        """
        This method returns opening hours of the specified restaurant
        """
        db_session = current_app.config["DB_SESSION"]
        openings = (
            db_session.query(OpeningHours)
            .filter(restaurant_id == OpeningHours.restaurant_id)
            .all()
        )
        return openings

    @staticmethod
    def get_tables(restaurant_id):
        """
        This method returns tables of the specified restaurant
        """
        db_session = current_app.config["DB_SESSION"]
        tables = (
            db_session.query(RestaurantTable)
            .filter(restaurant_id == RestaurantTable.restaurant_id)
            .all()
        )
        return tables

    @staticmethod
    def get_photos(restaurant_id):
        """
        This method returns photos of the specified restaurant
        """
        db_session = current_app.config["DB_SESSION"]
        photos = (
            db_session.query(PhotoGallery)
            .filter(restaurant_id == PhotoGallery.restaurant_id)
            .all()
        )
        return photos

    @staticmethod
    def get_photo_with_url(url):
        """
        This method returns photos of the specified restaurant using url
        """
        db_session = current_app.config["DB_SESSION"]
        photo = db_session.query(PhotoGallery).filter(url == PhotoGallery.url).all()
        return photo

    @staticmethod
    def get_reviews(restaurant_id):
        """
        This method returns review of the restaurant
        """
        db_session = current_app.config["DB_SESSION"]
        review = (
            db_session.query(Review).filter(restaurant_id == Review.restaurant_id).all()
        )
        return review

    @staticmethod
    def get_reviews_random(restaurant_id, number):
        """
        This method returns random reviews of the restaurant 
        Number of reviews is given by the argument "number"
        """
        db_session = current_app.config["DB_SESSION"]
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
        """
        This method deletes the specified dish
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(MenuDish).filter_by(id=dish_id).delete()
        db_session.commit()
        return True

    @staticmethod
    def delete_table(table_id):
        """
        This method deletes the specified table
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(RestaurantTable).filter_by(id=table_id).delete()
        db_session.commit()
        return True

    @staticmethod
    def delete_table(table_id):
        """
        This method deletes the specified table
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(RestaurantTable).filter_by(id=table_id).delete()
        db_session.commit()
        return True


    def delete_restaurant(restaurant_id):
        """
        This method deletes all data about a restaurant (also in other tables)
        """

        db_session = current_app.config["DB_SESSION"]
        restaurant = db_session.query(Restaurant).filter(
                Restaurant.id == restaurant_id
            ).first()

        if restaurant is None:
            return True

        db_session.query(OpeningHours).filter(
            OpeningHours.restaurant_id == restaurant.id
        ).delete()

        db_session.query(RestaurantTable).filter(
            RestaurantTable.restaurant_id == restaurant.id
        ).delete()

        db_session.query(PhotoGallery).filter(
            PhotoGallery.restaurant_id == restaurant.id
        ).delete()

        db_session.query(MenuDish).filter(
            MenuDish.restaurant_id == restaurant.id
        ).delete()

        db_session.query(Review).filter(
            Review.restaurant_id == restaurant.id
        ).delete()

        menus = db_session.query(Menu).filter(Menu.restaurant_id == restaurant.id).all()
        for menu in menus:
            db_session.query(MenuPhotoGallery).filter(
                MenuPhotoGallery.menu_id == menu.id
            ).delete()

        db_session.query(Menu).filter(Menu.restaurant_id == restaurant.id).delete()
        
        db_session.query(Restaurant).filter(Restaurant.id == restaurant.id).delete()
        db_session.commit()


    @staticmethod
    def create_restaurant(data, max_seats):
        """
        This method creates a new restaurant
        """
        rest = data["restaurant"]
        rest_name = rest["name"]
        lat = rest["lat"]
        lon = rest["lon"]
        rest_phone = rest["phone"]
        # add in restaurant table
        new_restaurant = Restaurant()
        new_restaurant.name = rest_name
        new_restaurant.lat = lat
        new_restaurant.lon = lon
        new_restaurant.phone = rest_phone
        new_restaurant.covid_measures = data["restaurant"]["covid_measures"]
        new_restaurant.avg_time = data["restaurant"]["avg_time"]
        new_restaurant.rating = data["restaurant"]["rating"]
        new_restaurant.owner_email = data["restaurant"]["owner_email"]

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_restaurant)
        db_session.commit()

        # add tables in RestaurantTable table
        number_tables = data["restaurant_tables"]
        for i in range(number_tables):
            RestaurantService.create_table("", max_seats, new_restaurant.id)

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
        return db_session.query(Restaurant).filter_by(name=rest_name, lat=lat, lon=lon, phone=rest_phone).first()

    @staticmethod
    def create_table(name, max_seats, restaurant_id):
        """
        This method creates a table for the  restaurant with id "restaurant_id".
        the table has a name and a maximum number of people
        """
        new_table = RestaurantTable()
        new_table.restaurant_id = restaurant_id
        new_table.name = name
        new_table.max_seats = max_seats
        new_table.available = True

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_table)
        db_session.commit()
        return True

    @staticmethod
    def get_avg_rating_restaurant(restaurant_id: int) -> float:
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
           return -1
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
            RestaurantService.get_avg_rating_restaurant(restaurant.id)
        return True

    @staticmethod
    def update_restaurant_info(data):
        """
        update the restaurant infos
        """

        # put in model from json for better validation, debug, test
        update_restaurant = Restaurant()
        update_restaurant.name = data["name"]
        update_restaurant.lat = data["lat"]
        update_restaurant.lon = data["lon"]
        update_restaurant.phone = data["phone"]
        update_restaurant.covid_measures = data["covid_measures"]
        update_restaurant.avg_time = data["avg_time"]
        update_restaurant.rating = data["rating"]
        update_restaurant.owner_email = data["owner_email"]
        update_restaurant.id = data["id"]

        db_session = current_app.config["DB_SESSION"]
        q = (
            db_session.query(Restaurant)
            .filter_by(id=update_restaurant.id)
            .update(
                {
                    "name": update_restaurant.name,
                    "lat": update_restaurant.lat,
                    "lon": update_restaurant.lon,
                    "phone": update_restaurant.phone,
                    "covid_measures": update_restaurant.covid_measures,
                    "avg_time": update_restaurant.avg_time,
                    "rating": update_restaurant.rating,
                    "owner_email": update_restaurant.owner_email,
                }
            )
        )
        db_session.commit()
        db_session.flush()

        # return True if a restaurant was modified
        return q != 0

    @staticmethod
    def create_dish(name, price, restaurant_id):
        """
        This method creates a new dish
        """
        new_dish = MenuDish()
        new_dish.restaurant_id = restaurant_id
        new_dish.name = name
        new_dish.price = price

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_dish)
        db_session.commit()
        return True

    @staticmethod
    def create_restaurant_photo(url, caption, restaurant_id):
        """
        This method creates a new restaurant photo
        """
        new_photo = PhotoGallery()
        new_photo.restaurant_id = restaurant_id
        new_photo.url = url
        new_photo.caption = caption

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_photo)
        db_session.commit()
        return True

    @staticmethod
    def create_review(review, stars, reviewer_email, restaurant_id):
        """
        This method creates a new review for the restaurant
        """
        new_review = Review()
        new_review.restaurant_id = restaurant_id
        new_review.review = review
        new_review.stars = stars
        new_review.reviewer_email = reviewer_email

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_review)
        db_session.commit()
        return True

    @staticmethod
    def create_menu_photo(url, caption, menu_id):
        """
        This method creates a new photo of the specified menu
        """
        new_photo = MenuPhotoGallery()
        new_photo.menu_id = menu_id
        new_photo.url = url
        new_photo.caption = caption

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_photo)
        db_session.commit()
        return True
