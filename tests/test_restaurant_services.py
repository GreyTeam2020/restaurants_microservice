from services import RestaurantService
from utils import Utils
import unittest

_max_seats = 6
_stars = 2


class TestRestaurantsServices:
    def test_all_restaurant(self):
        """
        test about the services restaurant to test the result of all restaurants
        :return:
        """
        all_restaurants = RestaurantService.get_all_restaurants()
        assert len(all_restaurants) == 2

    def test_get_restaurant_ok(self):
        """
        test about the services restaurant to test the result of get a restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        restaurant = RestaurantService.get_restaurant(new_restaurant.id)
        assert restaurant is not None
        assert restaurant.name == "Test restaurant"
        assert restaurant.owner_email == "john@email.com"
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_not_exists(self):
        """
        test about the services restaurant to test the result of get a restaurant
        in the case restaurant doesn't exist
        :return:
        """
        restaurant = RestaurantService.get_restaurant(10)
        assert restaurant is None

    def test_get_restaurant_with_info_exist(self):
        """
        test about the services restaurant to test the result of get restaurant
        using its info
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        restaurant = RestaurantService.get_restaurant_with_info(
            new_restaurant.name,
            new_restaurant.phone,
            new_restaurant.lat,
            new_restaurant.lon,
        )
        assert restaurant is not None
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_with_info_not_exists(self):
        """
        test about the services restaurant to test the result of get restaurant
        that doesn't exist using info
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        restaurant = RestaurantService.get_restaurant_with_info(
            new_restaurant.name,
            new_restaurant.phone,
            new_restaurant.lat + 2,
            new_restaurant.lon,
        )
        assert restaurant is None
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_by_email_exist(self):
        """
        test about the services restaurant to test the result of get restaurant
        using owner email
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        restaurant = RestaurantService.get_restaurants_by_owner_email("john@email.com")
        assert restaurant == new_restaurant
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_by_email_not_exists(self):
        """
        test about the services restaurant to test the result of get restaurant
        that doesn't exist using owner email
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        restaurant = RestaurantService.get_restaurants_by_owner_email("test@email.com")
        assert restaurant is None
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_keyword_one_result(self):
        """
        test about the services restaurant to test the result of get restaurant
        using a keyword
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        restaurants = RestaurantService.get_restaurants_by_keyword_name("wood")
        assert len(restaurants) == 1
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_keyword_complete_name(self):
        """
        test about the services restaurant to test the result of get restaurant
        using as keyword the name of the restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        restaurants = RestaurantService.get_restaurants_by_keyword_name("Pepperwood")
        assert len(restaurants) == 1
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_keyword_more_results(self):
        """
        test about the services restaurant to test the result of get restaurant
        using a keyword, obteining more results
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        restaurants = RestaurantService.get_restaurants_by_keyword_name("rest")
        assert len(restaurants) == 2
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_keyword_no_results(self):
        """
        test about the services restaurant to test the result of get restaurant
        using a keyword obteining no results
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        restaurants = RestaurantService.get_restaurants_by_keyword_name("Bobby's")
        assert len(restaurants) == 0
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menus_ok(self):
        """
        test about the services restaurant to test the result of get menus of
        a restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_menu1 = Utils.create_menu(new_restaurant.id, "Italian food")
        new_menu2 = Utils.create_menu(new_restaurant.id, "Chinese food")

        menus = RestaurantService.get_menus(new_restaurant.id)
        assert len(menus) == 2

        Utils.delete_menu(new_menu1.id)
        Utils.delete_menu(new_menu2.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menus_no_results(self):
        """
        test about the services restaurant to test the result of get menus of
        a restaurant that doesn't have menus
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        menus = RestaurantService.get_menus(new_restaurant.id)
        assert len(menus) == 0
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menu_ok(self):
        """
        test about the services restaurant to test the result of get a menu
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_menu = Utils.create_menu(new_restaurant.id, "Italian food")

        menu = RestaurantService.get_menu(new_menu.id)
        assert menu is not None
        assert menu.cusine == "Italian food"

        Utils.delete_menu(new_menu.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menu_not_exists(self):
        """
        test about the services restaurant to test the result of get a menu
        that doesn't exist
        :return:
        """

        new_restaurant = Utils.create_restaurant()
        new_menu = Utils.create_menu(new_restaurant.id, "Italian food")

        menu = RestaurantService.get_menu(new_menu.id + 2)
        assert menu is None

        Utils.delete_menu(new_menu.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menu_photos_ok(self):
        """
        test about the services restaurant to test the result of get photos of
        a menu
        :return:
        """
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
        """
        test about the services restaurant to test the result of get photos of a 
        menu without photos
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_menu = Utils.create_menu(new_restaurant.id, "Italian food")

        photos = RestaurantService.get_menu_photos(new_menu.id)
        assert len(photos) == 0

        Utils.delete_menu(new_menu.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_menu_photos_with_url_ok(self):
        """
        test about the services restaurant to test the result of get a photo
        of a menu searching using its URL
        :return:
        """
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
        """
        test about the services restaurant to test the result of get a photo
        of a menu searching using a not existing URL
        :return:
        """
        photo = RestaurantService.get_menu_photo_with_url("http://phototest1.com")
        assert photo is None

    def test_get_dishes_ok(self):
        """
        test about the services restaurant to test the result of get dishes of
        a restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_dish1 = Utils.create_dish(new_restaurant.id, "Pizza")
        new_dish2 = Utils.create_dish(new_restaurant.id, "Pasta")

        dishes = RestaurantService.get_dishes(new_restaurant.id)
        assert len(dishes) == 2

        Utils.delete_dish(new_dish1.id)
        Utils.delete_dish(new_dish2.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_dishes_not_exists(self):
        """
        test about the services restaurant to test the result of get dishes of 
        a restaurant with no dishes
        :return:
        """
        new_restaurant = Utils.create_restaurant()

        dishes = RestaurantService.get_dishes(new_restaurant.id)
        assert len(dishes) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_openings_ok(self):
        """
        test about the services restaurant to test the result of get opening
        hours of a restaurant
        :return:
        """
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
        """
        test about the services restaurant to test the result of get opening
        hours of a restaurant without opening hours
        :return:
        """
        new_restaurant = Utils.create_restaurant()

        openings = RestaurantService.get_openings(new_restaurant.id)
        assert len(openings) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_tables_ok(self):
        """
        test about the services restaurant to test the result of get tables of a 
        restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_table1 = Utils.create_table(new_restaurant.id)
        new_table2 = Utils.create_table(new_restaurant.id)

        tables = RestaurantService.get_tables(new_restaurant.id)
        assert len(tables) == 2

        Utils.delete_table(new_table1.id)
        Utils.delete_table(new_table2.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_tables_not_exists(self):
        """
        test about the services restaurant to test the result of get tables of a 
        restaurant with no tables
        :return:
        """
        new_restaurant = Utils.create_restaurant()

        tables = RestaurantService.get_tables(new_restaurant.id)
        assert len(tables) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_photos_ok(self):
        """
        test about the services restaurant to test the result of get photos of a 
        restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_photo1 = Utils.create_photo(new_restaurant.id, "http://phototest1.com")
        new_photo2 = Utils.create_photo(new_restaurant.id, "http://phototest2.com")

        photos = RestaurantService.get_photos(new_restaurant.id)
        assert len(photos) == 2

        Utils.delete_photo(new_photo1.id)
        Utils.delete_photo(new_photo2.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_photos_not_exists(self):
        """
        test about the services restaurant to test the result of get photos of a 
        restaurant with no photos
        :return:
        """
        new_restaurant = Utils.create_restaurant()

        photos = RestaurantService.get_photos(new_restaurant.id)
        assert len(photos) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_photo_with_url_ok(self):
        """
        test about the services restaurant to test the result of get photo of a 
        restaurant uring its URL
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_photo = Utils.create_photo(new_restaurant.id, "http://phototest1.com")

        photos = RestaurantService.get_photo_with_url("http://phototest1.com")
        assert len(photos) == 1
        assert photos[0].restaurant_id == new_restaurant.id
        assert photos[0].url == "http://phototest1.com"

        Utils.delete_photo(new_photo.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_photo_with_url_not_exists(self):
        """
        test about the services restaurant to test the result of get photo of a 
        restaurant uring a not existing URL
        :return:
        """
        photos = RestaurantService.get_photo_with_url("http://phototest1.com")
        assert len(photos) == 0

    def test_get_reviews_ok(self):
        """
        test about the services restaurant to test the result of get reviews of a 
        restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_review = Utils.create_review(new_restaurant.id, _stars)

        reviews = RestaurantService.get_reviews(new_restaurant.id)
        assert len(reviews) == 1

        Utils.delete_review(new_review.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_not_exists(self):
        """
        test about the services restaurant to test the result of get reviews of a 
        restaurant with no reviews
        :return:
        """
        new_restaurant = Utils.create_restaurant()

        reviews = RestaurantService.get_reviews(new_restaurant.id)
        assert len(reviews) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_random_bigger_num_ok(self):
        """
        test about the services restaurant to test the result of get a number 
        of random reviews bigger of the number of reviews of the restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_review = Utils.create_review(new_restaurant.id, _stars)

        reviews = RestaurantService.get_reviews_random(new_restaurant.id, 3)
        assert len(reviews) == 1

        Utils.delete_review(new_review.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_random_smaller_num_ok(self):
        """
        test about the services restaurant to test the result of get a number 
        of random reviews smaller of the number of reviews of the restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_review1 = Utils.create_review(new_restaurant.id, _stars)
        new_review2 = Utils.create_review(new_restaurant.id, _stars)
        new_review3 = Utils.create_review(new_restaurant.id, _stars)

        reviews = RestaurantService.get_reviews_random(new_restaurant.id, 2)
        assert len(reviews) == 2

        Utils.delete_review(new_review1.id)
        Utils.delete_review(new_review2.id)
        Utils.delete_review(new_review3.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_random_not_exists(self):
        """
        test about the services restaurant to test the result of get a number 
        of random reviews of a restaurant with no reviews
        :return:
        """
        new_restaurant = Utils.create_restaurant()

        reviews = RestaurantService.get_reviews_random(new_restaurant.id, 5)
        assert len(reviews) == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_random_0(self):
        """
        test about the services restaurant to test the result of get a number 
        of random reviews of a restaurant testing a limit case (number=0)
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_review = Utils.create_review(new_restaurant.id, _stars)

        reviews = RestaurantService.get_reviews_random(new_restaurant.id, 0)
        assert len(reviews) == 0

        Utils.delete_review(new_review.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_reviews_random_negative(self):
        """
        test about the services restaurant to test the result of get a number 
        of random reviews of a restaurant usingg an invalid number
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_review1 = Utils.create_review(new_restaurant.id, _stars)
        new_review2 = Utils.create_review(new_restaurant.id, _stars)
        new_review3 = Utils.create_review(new_restaurant.id, _stars)

        reviews = RestaurantService.get_reviews_random(new_restaurant.id, -10)
        assert len(reviews) == 3

        Utils.delete_review(new_review1.id)
        Utils.delete_review(new_review2.id)
        Utils.delete_review(new_review3.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_delete_dish_ok(self):
        """
        test about the services restaurant to test the result of deleting a dish
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_dish = Utils.create_dish(new_restaurant.id, "Pizza")

        dish = Utils.get_dish(new_dish.id)
        assert dish is not None

        response = RestaurantService.delete_dish(new_dish.id)
        assert response is True

        dish = Utils.get_dish(new_dish.id)
        assert dish is None

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_dish_not_exists_not_fail(self):
        """
        test about the services restaurant to test the result of deleting a 
        dish that doesn't exist
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_dish = Utils.create_dish(new_restaurant.id, "Pizza")

        response = RestaurantService.delete_dish(new_dish.id + 1)
        assert response is True

        dish = Utils.get_dish(new_dish.id)
        assert dish is not None

        Utils.delete_dish(new_dish.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_delete_table_ok(self):
        """
        test about the services restaurant to test the result of deleting a table
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_table = Utils.create_table(new_restaurant.id)

        table = Utils.get_table(new_table.id)
        assert table is not None

        response = RestaurantService.delete_table(new_table.id)
        assert response is True

        table = Utils.get_table(new_table.id)
        assert table is None

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_table_not_exists_not_fail(self):
        """
        test about the services restaurant to test the result of deleting a table
        that doesn't exist
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_table = Utils.create_table(new_restaurant.id)

        response = RestaurantService.delete_table(new_table.id + 1)
        assert response is True

        table = Utils.get_table(new_table.id)
        assert table is not None

        Utils.delete_table(new_table.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_create_restaurant_ok(self):
        """
        test about the services restaurant to test the result of creating a restaurant
        :return:
        """
        body = Utils.json_create_restaurant()

        restaurants = RestaurantService.create_restaurant(body, _max_seats)
        assert restaurants is not None
        assert body["restaurant"]["name"] == restaurants.name
        assert restaurants.id > 0

        Utils.delete_creation_restaurant(body)

    def test_create_table_ok(self):
        """
        test about the services restaurant to test the result of creating a table
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        body = Utils.json_table()

        response = RestaurantService.create_table(
            body["name"], body["max_seats"], new_restaurant.id
        )
        assert response is True

        Utils.delete_table_restaurant(new_restaurant.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_create_dish_ok(self):
        """
        test about the services restaurant to test the result of creating a dish
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        body = Utils.json_dish()

        response = RestaurantService.create_dish(
            body["name"], body["price"], new_restaurant.id
        )
        assert response is True

        Utils.delete_dish_restaurant(new_restaurant.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_create_restaurant_photo_ok(self):
        """
        test about the services restaurant to test the result of creating a 
        restaurant photo
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        body = Utils.json_photo()

        response = RestaurantService.create_restaurant_photo(
            body["url"], body["caption"], new_restaurant.id
        )
        assert response is True

        Utils.delete_restaurant_photo(new_restaurant.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_create_review_ok(self):
        """
        test about the services restaurant to test the result of creating a review
        for a restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        body = Utils.json_review()

        response = RestaurantService.create_review(
            body["review"], body["stars"], body["reviewer_email"], new_restaurant.id
        )
        assert response is True

        Utils.delete_review_restaurant(new_restaurant.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_create_menu_photo_ok(self):
        """
        test about the services restaurant to test the result of creating a menu photo
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_menu = Utils.create_menu(new_restaurant.id, "Italian food")
        body = Utils.json_photo()

        response = RestaurantService.create_menu_photo(
            body["url"], body["caption"], new_restaurant.id
        )
        assert response is True

        Utils.delete_menu_photo_by_menu(new_restaurant.id)
        Utils.delete_menu(new_menu.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_rating_ok_not_0(self):
        """
        test about the services restaurant to test the result of getting rating
        for a restaurant whose rating is different from 0
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_review1 = Utils.create_review(new_restaurant.id, 3)
        new_review2 = Utils.create_review(new_restaurant.id, 5)
        new_review3 = Utils.create_review(new_restaurant.id, 2.5)

        rating = RestaurantService.get_avg_rating_restaurant(new_restaurant.id)
        assert rating == 3.5

        Utils.delete_review(new_review1.id)
        Utils.delete_review(new_review2.id)
        Utils.delete_review(new_review3.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_rating_ok_0(self):
        """
        test about the services restaurant to test the result of getting rating
        for a restaurant whose rating is 0
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_review1 = Utils.create_review(new_restaurant.id, 0)
        new_review2 = Utils.create_review(new_restaurant.id, 0)

        rating = RestaurantService.get_avg_rating_restaurant(new_restaurant.id)
        assert rating == 0

        Utils.delete_review(new_review1.id)
        Utils.delete_review(new_review2.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_rating_ok_empty(self):
        """
        test about the services restaurant to test the result of getting rating
        for a restaurant with no reviews
        :return:
        """
        new_restaurant = Utils.create_restaurant()

        rating = RestaurantService.get_avg_rating_restaurant(new_restaurant.id)
        assert rating == 0

        Utils.delete_restaurant(new_restaurant.id)

    def test_get_restaurant_rating_restaurant_not_exists(self):
        """
        test about the services restaurant to test the result of getting rating
        for a restaurant that doesn't exist
        :return:
        """
        exception_raised = True
        try:
            RestaurantService.get_avg_rating_restaurant(20)
            assert exception_raised is False
        except:
            assert exception_raised is True

    def test_get_all_restaurant_rating_not_fail(self):
        """
        test about the services restaurant to test the result of calculate rating
        for all restaurants
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_review1 = Utils.create_review(new_restaurant.id, 3)
        new_review2 = Utils.create_review(new_restaurant.id, 5)
        new_review3 = Utils.create_review(new_restaurant.id, 2.5)

        response = RestaurantService.calculate_rating_for_all_restaurant()
        assert response is True

        Utils.delete_review(new_review1.id)
        Utils.delete_review(new_review2.id)
        Utils.delete_review(new_review3.id)
        Utils.delete_restaurant(new_restaurant.id)

    def test_get_update_restaurant_info_ok(self):
        """
        test about the services restaurant to test the result of updating information
        about a restaurant
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        assert new_restaurant.name == "Test restaurant"

        body = Utils.json_restaurant(new_restaurant.id)

        response = RestaurantService.update_restaurant_info(body)
        assert response is True
        assert new_restaurant.name == "Bobby's"

        Utils.delete_restaurant(new_restaurant.id)

    def test_delete_restaurant_all_info_ok(self):
        """
        test about the services restaurant to test the result of deleting a restaurant
        and all its information (reivews, opening hours, ...)
        :return:
        """
        new_restaurant = Utils.create_restaurant()
        new_table = Utils.create_table(new_restaurant.id)
        new_menu = Utils.create_menu(new_restaurant.id, "Italian food")
        new_menu_photo = Utils.create_menu_photo(
            new_menu.id, "http://testphotomenu.com"
        )
        new_opening1 = Utils.create_openings(new_restaurant.id, 2)
        new_opening2 = Utils.create_openings(new_restaurant.id, 3)
        new_review = Utils.create_review(new_restaurant.id, 3)
        new_photo = Utils.create_photo(new_restaurant.id, "http://testphoto.com")
        new_dish = Utils.create_dish(new_restaurant.id, "Pizza")

        response = RestaurantService.delete_restaurant(new_restaurant.id)
        assert response is True

        assert Utils.get_restaurant(new_restaurant.id) is None
        assert Utils.get_table(new_table.id) is None
        assert Utils.get_menu(new_menu.id) is None
        assert Utils.get_menu(new_menu_photo.id) is None
        assert len(Utils.get_opening_by_restaurant(new_restaurant.id)) == 0
        assert Utils.get_review(new_review.id) is None
        assert Utils.get_photo(new_photo.id) is None
        assert Utils.get_dish(new_dish.id) is None

    def test_delete_restaurant_all_info_not_found(self):
        """
        test about the services restaurant to test the result of deleting a restaurant
        and all its information for a restaurant that doesn't exist
        :return:
        """
        response = RestaurantService.delete_restaurant(100)
        assert response is True
        assert Utils.get_restaurant(100) is None
