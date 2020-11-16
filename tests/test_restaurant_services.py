from services import RestaurantService
from utils import Utils


class TestRestaurantsServices:
    def test_all_restaurant(self):
        """
        test about the services restaurant to test the result of all restaurants
        :return:
        """
        all_restaurants = RestaurantService.get_all_restaurants()
        assert len(all_restaurants) == 2

    def test_get_restaurant_ok(self):
        new_restaurant = Utils.create_restaurant()
        restaurant = RestaurantService.get_restaurant(new_restaurant.id)
        assert restaurant is not None
        assert restaurant.name == "Test restaurant"
        assert restaurant.owner_email == "john@email.com"
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_not_exists(self):
        restaurant = RestaurantService.get_restaurant(10)
        assert restaurant is None

    def test_get_restaurant_with_info_exist(self):
        new_restaurant = Utils.create_restaurant()
        restaurant = RestaurantService.get_restaurant_with_info(
            new_restaurant.name,
            new_restaurant.phone,
            new_restaurant.lat,
            new_restaurant.lon,
        )
        assert restaurant is True
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_with_info_not_exists(self):
        new_restaurant = Utils.create_restaurant()
        restaurant = RestaurantService.get_restaurant_with_info(
            new_restaurant.name,
            new_restaurant.phone,
            new_restaurant.lat + 2,
            new_restaurant.lon,
        )
        assert restaurant is False
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_keyword_one_result(self):
        new_restaurant = Utils.create_restaurant()
        restaurants = RestaurantService.get_restaurants_by_keyword_name("wood")
        assert len(restaurants) == 1
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_keyword_complete_name(self):
        new_restaurant = Utils.create_restaurant()
        restaurants = RestaurantService.get_restaurants_by_keyword_name("Pepperwood")
        assert len(restaurants) == 1
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_keyword_more_results(self):
        new_restaurant = Utils.create_restaurant()
        restaurants = RestaurantService.get_restaurants_by_keyword_name("rest")
        assert len(restaurants) == 2
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_keyword_no_results(self):
        new_restaurant = Utils.create_restaurant()
        restaurants = RestaurantService.get_restaurants_by_keyword_name("Bobby's")
        assert len(restaurants) == 0
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menus_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_menu1 = Utils.create_menu(new_restaurant.id, "Italian food")
        new_menu2 = Utils.create_menu(new_restaurant.id, "Chinese food")

        menus = RestaurantService.get_menus(new_restaurant.id)
        assert len(menus) == 2

        Utils.delete_menu(new_menu1.id)
        Utils.delete_menu(new_menu2.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menus_no_results(self):
        new_restaurant = Utils.create_restaurant()
        menus = RestaurantService.get_menus(new_restaurant.id)
        assert len(menus) == 0
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menu_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_menu = Utils.create_menu(new_restaurant.id, "Italian food")

        menu = RestaurantService.get_menu(new_menu.id)
        assert menu is not None
        assert menu.cusine == "Italian food"

        Utils.delete_menu(new_menu.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menu_not_exists(self):

        new_restaurant = Utils.create_restaurant()
        new_menu = Utils.create_menu(new_restaurant.id, "Italian food")

        menu = RestaurantService.get_menu(new_menu.id + 2)
        assert menu is None

        Utils.delete_menu(new_menu.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menu_photos_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_menu = Utils.create_menu(new_restaurant.id, "Italian food")
        new_photo1 = Utils.create_menu_photo(new_menu.id, "http://phototest1.com")
        new_photo2 = Utils.create_menu_photo(new_menu.id, "http://phototest2.com")

        photos = RestaurantService.get_menu_photos(new_menu.id)
        assert len(photos) == 2

        Utils.delete_menu_photo(new_photo1.id)
        Utils.delete_menu_photo(new_photo2.id)
        Utils.delete_menu(new_menu.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menu_photos_not_exist(self):
        new_restaurant = Utils.create_restaurant()
        new_menu = Utils.create_menu(new_restaurant.id, "Italian food")

        photos = RestaurantService.get_menu_photos(new_menu.id)
        assert len(photos) == 0

        Utils.delete_menu(new_menu.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menu_photos_with_url_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_menu = Utils.create_menu(new_restaurant.id, "Italian food")
        new_photo = Utils.create_menu_photo(new_menu.id, "http://phototest1.com")

        photo = RestaurantService.get_menu_photo_with_url(new_photo.url)
        assert photo is not None
        assert photo.url == "http://phototest1.com"

        Utils.delete_menu_photo(new_photo.id)
        Utils.delete_menu(new_menu.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menu_photos_with_url_not_exist(self):
        photo = RestaurantService.get_menu_photo_with_url("http://phototest1.com")
        assert photo is None

    def test_get_dishes_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_dish1 = Utils.create_dish(new_restaurant.id, "Pizza")
        new_dish2 = Utils.create_dish(new_restaurant.id, "Pasta")

        dishes = RestaurantService.get_dishes(new_restaurant.id)
        assert len(dishes) == 2

        Utils.delete_dish(new_dish1.id)
        Utils.delete_dish(new_dish2.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_dishes_not_exists(self):
        new_restaurant = Utils.create_restaurant()

        dishes = RestaurantService.get_dishes(new_restaurant.id)
        assert len(dishes) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_openings_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_opening1 = Utils.create_openings(new_restaurant.id, 2)
        new_opening2 = Utils.create_openings(new_restaurant.id, 3)
        new_opening3 = Utils.create_openings(new_restaurant.id, 5)

        openings = RestaurantService.get_openings(new_restaurant.id)
        assert len(openings) == 3

        Utils.delete_openings(new_opening1)
        Utils.delete_openings(new_opening2)
        Utils.delete_openings(new_opening3)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_openings_not_exists(self):
        new_restaurant = Utils.create_restaurant()

        openings = RestaurantService.get_openings(new_restaurant.id)
        assert len(openings) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_tables_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_table1 = Utils.create_table(new_restaurant.id)
        new_table2 = Utils.create_table(new_restaurant.id)

        tables = RestaurantService.get_tables(new_restaurant.id)
        assert len(tables) == 2

        Utils.delete_table(new_table1.id)
        Utils.delete_table(new_table2.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_tables_not_exists(self):
        new_restaurant = Utils.create_restaurant()

        tables = RestaurantService.get_tables(new_restaurant.id)
        assert len(tables) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_photos_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_photo1 = Utils.create_photo(new_restaurant.id, "http://phototest1.com")
        new_photo2 = Utils.create_photo(new_restaurant.id, "http://phototest2.com")

        photos = RestaurantService.get_photos(new_restaurant.id)
        assert len(photos) == 2

        Utils.delete_photo(new_photo1.id)
        Utils.delete_photo(new_photo2.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_photos_not_exists(self):
        new_restaurant = Utils.create_restaurant()

        photos = RestaurantService.get_photos(new_restaurant.id)
        assert len(photos) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_photo_with_url_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_photo = Utils.create_photo(new_restaurant.id, "http://phototest1.com")

        photos = RestaurantService.get_photo_with_url("http://phototest1.com")
        assert len(photos) == 1
        assert photos[0].restaurant_id == new_restaurant.id
        assert photos[0].url == "http://phototest1.com"

        Utils.delete_photo(new_photo.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_photo_with_url_not_exists(self):
        photos = RestaurantService.get_photo_with_url("http://phototest1.com")
        assert len(photos) == 0

    def test_get_reviews_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_review = Utils.create_review(new_restaurant.id)

        reviews = RestaurantService.get_reviews(new_restaurant.id)
        assert len(reviews) == 1

        Utils.delete_review(new_review.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_not_exists(self):
        new_restaurant = Utils.create_restaurant()

        reviews = RestaurantService.get_reviews(new_restaurant.id)
        assert len(reviews) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_random_bigger_num_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_review = Utils.create_review(new_restaurant.id)

        reviews = RestaurantService.get_reviews_random(new_restaurant.id, 3)
        assert len(reviews) == 1

        Utils.delete_review(new_review.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_random_smaller_num_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_review1 = Utils.create_review(new_restaurant.id)
        new_review2 = Utils.create_review(new_restaurant.id)
        new_review3 = Utils.create_review(new_restaurant.id)

        reviews = RestaurantService.get_reviews_random(new_restaurant.id, 2)
        assert len(reviews) == 2

        Utils.delete_review(new_review1.id)
        Utils.delete_review(new_review2.id)
        Utils.delete_review(new_review3.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_random_not_exists(self):
        new_restaurant = Utils.create_restaurant()

        reviews = RestaurantService.get_reviews_random(new_restaurant.id, 5)
        assert len(reviews) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_random_0(self):
        new_restaurant = Utils.create_restaurant()
        new_review = Utils.create_review(new_restaurant.id)

        reviews = RestaurantService.get_reviews_random(new_restaurant.id, 0)
        assert len(reviews) == 0

        Utils.delete_review(new_review.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_random_negative(self):
        new_restaurant = Utils.create_restaurant()
        new_review1 = Utils.create_review(new_restaurant.id)
        new_review2 = Utils.create_review(new_restaurant.id)
        new_review3 = Utils.create_review(new_restaurant.id)

        reviews = RestaurantService.get_reviews_random(new_restaurant.id, -10)
        assert len(reviews) == 3

        Utils.delete_review(new_review1.id)
        Utils.delete_review(new_review2.id)
        Utils.delete_review(new_review3.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_delete_dishes_ok(self):
        new_restaurant = Utils.create_restaurant()
        new_dish = Utils.create_dish(new_restaurant.id, "Pizza")

        response = RestaurantService.delete_dish(new_dish.id)
        assert response is True

        dish = Utils.get_dish(new_dish.id)
        assert dish is None

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_dishes_not_exists_not_fail(self):
        new_restaurant = Utils.create_restaurant()
        new_dish = Utils.create_dish(new_restaurant.id, "Pizza")

        response = RestaurantService.delete_dish(new_dish.id + 1)
        assert response is True

        dish = Utils.get_dish(new_dish.id)
        assert dish is not None

        Utils.delete_dish(new_dish.id)
        Utils.delete_restaurant(new_restaurant.id)

    '''


    @staticmethod
    def delete_table(table_id):

        db_session = current_app.config["DB_SESSION"]
        db_session.query(RestaurantTable).filter_by(id=table_id).delete()
        db_session.commit()
        return True

    @staticmethod
    def create_restaurant(data, max_seats):
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

    @staticmethod
    def create_table(name, max_seats, restaurant_id):
        new_table = RestaurantTable()
        new_table.restaurant_id = restaurant_id
        new_table.name = name
        new_table.max_seats = max_seats
        new_table.available = True

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_table)
        db_session.commit()

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
    def update_restaurant_info(data):
        """
        update the restaurant infos
        """

        # put in model from json for better validation, debug, test
        update_restaurant = Restaurant()
        update_restaurant.name = data["restaurant"]["name"]
        update_restaurant.lat = data["restaurant"]["lat"]
        update_restaurant.lon = data["restaurant"]["lon"]
        update_restaurant.phone = data["restaurant"]["phone"]
        update_restaurant.covid_measures = data["restaurant"]["covid_measures"]
        update_restaurant.avg_time = data["restaurant"]["avg_time"]
        update_restaurant.rating = data["restaurant"]["rating"]
        update_restaurant.owner_email = data["restaurant"]["owner_email"]
        update_restaurant.id = data["restaurant"]["id"]

        db_session = current_app.config["DB_SESSION"]
        q = db_session.query(Restaurant).filter_by(id=update_restaurant.id).update(
            {
                "name": update_restaurant.name,
                "lat": update_restaurant.lat,
                "lon": update_restaurant.lon,
                "phone": update_restaurant.phone,
                "covid_measures": update_restaurant.covid_measures,
                "avg_time": update_restaurant.avg_time,
                "rating": update_restaurant.rating,
                "owner_email": update_restaurant.owner_email
            }
        )
        db_session.commit()
        db_session.flush()

        # return True if a restaurant was modified
        return q != 0

    @staticmethod
    def create_dish(name, price, restaurant_id):
        new_dish = MenuDish()
        new_dish.restaurant_id = restaurant_id
        new_dish.name = name
        new_dish.price = price

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_dish)
        db_session.commit()

    @staticmethod
    def create_restaurant_photo(url, caption, restaurant_id):
        new_photo = PhotoGallery()
        new_photo.restaurant_id = restaurant_id
        new_photo.url = url
        new_photo.caption = caption

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_photo)
        db_session.commit()

    @staticmethod
    def create_review(review, stars, reviewer_email, restaurant_id):
        new_review = Review()
        new_review.restaurant_id = restaurant_id
        new_review.review = review
        new_review.stars = stars
        new_review.reviewer_email = reviewer_email

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_review)
        db_session.commit()

    @staticmethod
    def create_menu_photo(url, caption, menu_id):
        new_photo = MenuPhotoGallery()
        new_photo.menu_id = menu_id
        new_photo.url = url
        new_photo.caption = caption

        db_session = current_app.config["DB_SESSION"]
        db_session.add(new_photo)
        db_session.commit()

        '''
