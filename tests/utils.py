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


class Utils:
    @staticmethod
    def create_restaurant():
        """
        This method creates a new restaurant
        """
        new_restaurant = Restaurant()
        new_restaurant.name = "Test restaurant"
        new_restaurant.lat = "46.234"
        new_restaurant.lon = "21.563"
        new_restaurant.phone = 12345678
        new_restaurant.covid_measures = "Distance between tables"
        new_restaurant.avg_time = 50
        new_restaurant.owner_email = "john@email.com"

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_restaurant)
        db_session.commit()

        return new_restaurant

    @staticmethod
    def delete_restaurant(restaurant_id):
        """
        This method deletes a restaurant
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(Restaurant).filter(Restaurant.id == restaurant_id).delete()
        db_session.commit()

    @staticmethod
    def create_menu(restaurant_id, cuisine):
        """
        This method creates a new menu
        """
        db_session = current_app.config["DB_SESSION"]
        new_menu = Menu()
        new_menu.restaurant_id = restaurant_id
        new_menu.cusine = cuisine
        new_menu.description = ""

        db_session.add(new_menu)
        db_session.commit()
        return new_menu

    @staticmethod
    def delete_menu(menu_id):
        """
        This method deletes a menu
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(Menu).filter(Menu.id == menu_id).delete()
        db_session.commit()

    @staticmethod
    def create_menu_photo(menu_id, url):
        """
        This method creates a new photo of a menu
        """
        new_photo = MenuPhotoGallery()
        new_photo.menu_id = menu_id
        new_photo.url = url
        new_photo.caption = ""

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_photo)
        db_session.commit()
        return new_photo

    @staticmethod
    def delete_menu_photo(photo_id):
        """
        This method deltes a photo of the specified menu
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(MenuPhotoGallery).filter(
            MenuPhotoGallery.id == photo_id
        ).delete()
        db_session.commit()

    @staticmethod
    def create_dish(restaurant_id, name):
        """
        This method creates a new dish
        """
        new_dish = MenuDish()
        new_dish.restaurant_id = restaurant_id
        new_dish.name = name
        new_dish.price = 10.50

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_dish)
        db_session.commit()
        return new_dish

    @staticmethod
    def delete_dish(dish_id):
        """
        This method deletes a dish
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(MenuDish).filter(MenuDish.id == dish_id).delete()
        db_session.commit()

    @staticmethod
    def create_openings(restaurant_id, week_day):
        """
        This method creates a new opening hour
        """
        new_opening = OpeningHours()
        new_opening.restaurant_id = restaurant_id
        new_opening.week_day = week_day
        new_opening.open_lunch = datetime.time(12, 00)
        new_opening.close_lunch = datetime.time(15, 00)
        new_opening.open_dinner = datetime.time(19, 00)
        new_opening.close_dinner = datetime.time(22, 00)

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_opening)
        db_session.commit()
        return new_opening

    @staticmethod
    def delete_openings(opening):
        """
        This method deletes an opening hour
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(OpeningHours).filter(
            OpeningHours.restaurant_id == opening.restaurant_id,
            OpeningHours.week_day == opening.week_day,
        ).delete()
        db_session.commit()

    @staticmethod
    def create_table(restaurant_id):
        """
        This method creates a new table
        """
        new_table = RestaurantTable()
        new_table.restaurant_id = restaurant_id
        new_table.name = ""
        new_table.max_seats = 6
        new_table.available = True

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_table)
        db_session.commit()
        return new_table

    @staticmethod
    def delete_table(table_id):
        """
        This method deletes a table
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(RestaurantTable).filter(
            RestaurantTable.id == table_id
        ).delete()
        db_session.commit()

    @staticmethod
    def create_photo(restaurant_id, url):
        """
        This method creates a new photo of the restaurant
        """
        new_photo = PhotoGallery()
        new_photo.restaurant_id = restaurant_id
        new_photo.url = url
        new_photo.caption = ""

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_photo)
        db_session.commit()
        return new_photo

    @staticmethod
    def delete_photo(photo_id):
        """
        This method deletes a photo of the restaurant
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(PhotoGallery).filter(PhotoGallery.id == photo_id).delete()
        db_session.commit()

    @staticmethod
    def create_review(restaurant_id, stars):
        """
        This method creates a new review for a restaurant
        """
        new_review = Review()
        new_review.restaurant_id = restaurant_id
        new_review.review = "nice!"
        new_review.stars = stars
        new_review.reviewer_email = "john@email.com"

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_review)
        db_session.commit()
        return new_review

    @staticmethod
    def delete_review(review_id):
        """
        This method deletes a review
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(Review).filter(Review.id == review_id).delete()
        db_session.commit()

    def get_dish(dish_id):
        """
        This method gets a dish
        """
        db_session = current_app.config["DB_SESSION"]
        dish = db_session.query(MenuDish).filter(dish_id == MenuDish.id).first()
        return dish

    def get_table(table_id):
        """
        This method gets a table
        """
        db_session = current_app.config["DB_SESSION"]
        table = (
            db_session.query(RestaurantTable)
            .filter(table_id == RestaurantTable.id)
            .first()
        )
        return table

    def delete_creation_restaurant(data):
        """
        This method deletes all data inserted in the database to create a
        new restaurant
        """
        name = data["restaurant"]["name"]
        phone = data["restaurant"]["phone"]
        lat = data["restaurant"]["lat"]
        lon = data["restaurant"]["lon"]

        db_session = current_app.config["DB_SESSION"]
        restaurant = (
            db_session.query(Restaurant)
            .filter(
                Restaurant.name == name,
                Restaurant.phone == phone,
                Restaurant.lat == lat,
                Restaurant.lon == lon,
            )
            .first()
        )

        # delete menu , tables, restaurant
        db_session.query(OpeningHours).filter(
            OpeningHours.restaurant_id == restaurant.id
        ).delete()

        Utils.delete_table_restaurant(restaurant.id)

        db_session.query(Menu).filter(Menu.restaurant_id == restaurant.id).delete()
        db_session.query(Restaurant).filter(Restaurant.id == restaurant.id).delete()
        db_session.commit()

    def delete_table_restaurant(restaurant_id):
        """
        This method deletes tables of a restaurant
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(RestaurantTable).filter(
            RestaurantTable.restaurant_id == restaurant_id
        ).delete()
        db_session.commit()

    def delete_dish_restaurant(restaurant_id):
        """
        This method deletes dishes of a restaurantt
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(MenuDish).filter(
            MenuDish.restaurant_id == restaurant_id
        ).delete()
        db_session.commit()

    def delete_restaurant_photo(restaurant_id):
        """
        This method deletes restaurant photos
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(PhotoGallery).filter(
            PhotoGallery.restaurant_id == restaurant_id
        ).delete()
        db_session.commit()

    def delete_review_restaurant(restaurant_id):
        """
        This method deletes restaurant reviews
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(Review).filter(Review.restaurant_id == restaurant_id).delete()
        db_session.commit()

    def delete_menu_photo_by_menu(menu_id):
        """
        This method deletes menu photos
        """
        db_session = current_app.config["DB_SESSION"]
        db_session.query(MenuPhotoGallery).filter(
            MenuPhotoGallery.menu_id == menu_id
        ).delete()
        db_session.commit()

    @staticmethod
    def json_create_restaurant():
        """
        This method creates a JSON object to create a restaurant
        """
        return {
            "menu": ["Italian food", "Chinese food"],
            "opening": [
                {
                    "close_dinner": "22:00",
                    "close_lunch": "15:30",
                    "open_dinner": "19:00",
                    "open_lunch": "11:30",
                    "week_day": 3,
                },
                {
                    "close_dinner": "22:00",
                    "close_lunch": "15:30",
                    "open_dinner": "19:00",
                    "open_lunch": "11:30",
                    "week_day": 1,
                },
            ],
            "restaurant": {
                "avg_time": 50,
                "covid_measures": "Distance between tables",
                "lat": 43.7118,
                "lon": 10.4147,
                "name": "Bobby's",
                "owner_email": "bobby.sing@email.it",
                "phone": 10528958,
                "rating": 0,
            },
            "restaurant_tables": 5,
        }

    @staticmethod
    def json_table():
        """
        This method creates a JSON object to create a table
        """
        return {"max_seats": 3, "name": "Red table"}

    @staticmethod
    def json_dish():
        """
        This method creates a JSON object to create a dish
        """
        return {"name": "Pizza", "price": 6.5}

    @staticmethod
    def json_photo():
        """
        This method creates a JSON object to create a photo
        """
        return {"caption": "Photo 1", "url": "http://test_photo.safe"}

    @staticmethod
    def json_review():
        """
        This method creates a JSON object to create a review
        """
        return {
            "review": "Nice place!",
            "reviewer_email": "nick.miller@email.com",
            "stars": 3.5,
        }

    @staticmethod
    def json_restaurant(restaurant_id):
        """
        This method creates a JSON object to update a restaurant
        """
        return {
            "id": restaurant_id,
            "avg_time": 50,
            "covid_measures": "Distance between tables",
            "lat": 43.7118,
            "lon": 10.4147,
            "name": "Bobby's",
            "owner_email": "bobby.sing@email.it",
            "phone": 10528958,
            "rating": 0,
            
        }
