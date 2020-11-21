import logging

from services import RestaurantService
from utils import Utils
import json


class TestComponents:
    """
    This test include the component testing that
    help us to test the answer from the client
    """

    def test_get_restaurants_ok(self, client, db):
        """
        Test get restaurants
        """
        response = client.get("/restaurants", follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["restaurants"]) == 2

    def test_get_restaurant_ok(self, client, db):
        """
        Test get restaurant by id
        """
        response = client.get("/restaurants/" + str(2), follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert json_data["name"] == "Pepperwood"
        assert json_data["phone"] == 555123427
        assert (
            json_data["covid_measures"]
            == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        )
        assert json_data["lat"] == 33.720586
        assert json_data["lon"] == 11.408347
        assert json_data["owner_email"] == "nick.miller@email.com"

    def test_get_restaurant_ko_404(self, client, db):
        """
        Test get restaurant by id not found (404)
        """
        response = client.get("/restaurants/" + str(123), follow_redirects=True)
        assert response.status_code == 404

    def test_get_restaurant_name_by_id_ok(self, client, db):
        """
        Test get name restaurant by id ok (200)
        """
        response = client.get("/restaurants/" + str(2) + "/name", follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert json_data["result"] == "Pepperwood"

    def test_get_restaurant_name_by_id_ko_404(self, client, db):
        """
        Test get name restaurant not found by id ko (404)
        """
        response = client.get(
            "/restaurants/" + str(123) + "/name", follow_redirects=True
        )
        assert response.status_code == 404

    def test_get_restaurant_info_ok(self, client, db):
        """
        Test get restaurant info by id
        """
        response = client.get("/restaurants/" + str(2) + "/info", follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert json_data["Restaurant_info"]["Restaurant"]["name"] == "Pepperwood"
        assert json_data["Restaurant_info"]["Restaurant"]["phone"] == 555123427
        assert (
            json_data["Restaurant_info"]["Restaurant"]["covid_measures"]
            == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        )
        assert json_data["Restaurant_info"]["Restaurant"]["lat"] == 33.720586
        assert json_data["Restaurant_info"]["Restaurant"]["lon"] == 11.408347
        assert (
            json_data["Restaurant_info"]["Restaurant"]["owner_email"]
            == "nick.miller@email.com"
        )

        assert json_data["Restaurant_info"]["Menus"][0]["cusine"] == "Italian food"
        assert json_data["Restaurant_info"]["Menus"][0]["description"] == "local food"
        assert json_data["Restaurant_info"]["Menus"][0]["id"] == 1

        assert (
            json_data["Restaurant_info"]["Menus"][0]["photos"][0]["caption"]
            == "Photo 1"
        )
        assert json_data["Restaurant_info"]["Menus"][0]["photos"][0]["id"] == 1
        assert (
            json_data["Restaurant_info"]["Menus"][0]["photos"][0]["url"]
            == "http://photo1.com"
        )

    def test_get_restaurant_info_ko_404(self, client, db):
        """
        Test get name restaurant not found by id ko (404)
        """
        response = client.get(
            "/restaurants/" + str(123) + "/info", follow_redirects=True
        )
        assert response.status_code == 404

    def test_get_restaurants_by_keyword_ok(self, client, db):
        """
        Test search restaurant by keywords
        """
        keyword = "pep"
        response = client.get("/restaurants/search/" + keyword, follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert json_data["restaurants"][0]["name"] == "Pepperwood"
        assert json_data["restaurants"][0]["phone"] == 555123427
        assert (
            json_data["restaurants"][0]["covid_measures"]
            == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        )
        assert json_data["restaurants"][0]["lat"] == 33.720586
        assert json_data["restaurants"][0]["lon"] == 11.408347
        assert json_data["restaurants"][0]["owner_email"] == "nick.miller@email.com"

    def test_get_restaurants_by_keyword_ok_noresults(self, client, db):
        """
        Test search restaurant by keywords, no results
        """
        keyword = "notexists"
        response = client.get("/restaurants/search/" + keyword, follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["restaurants"]) == 0

    def test_post_restaurant_create_ok(self, client, db):
        """
        Test get create restaurant ok (201)
        """
        json_data = Utils.json_create_restaurant()
        response = client.post(
            "/restaurants/create", json=json_data, follow_redirects=True
        )
        assert response.status_code == 201
        Utils.delete_creation_restaurant(json_data)

    def test_post_restaurant_create_ko_409(self, client, db):
        """
        Test get create restaurant ok (201)
        """
        json_data = Utils.json_create_restaurant()
        response = client.post(
            "/restaurants/create", json=json_data, follow_redirects=True
        )
        assert response.status_code == 201

        """
        Test get create restaurant ko (409) because is duplicate 
        """
        response = client.post(
            "/restaurants/create", json=json_data, follow_redirects=True
        )
        assert response.status_code == 409
        Utils.delete_creation_restaurant(json_data)

    def test_post_restaurant_create_ko_400(self, client, db):
        """
        Test get create restaurant ko (400), phone missing
        """
        json_data = Utils.json_create_restaurant()
        json_data["restaurant"]["phone"] = None
        response = client.post(
            "/restaurants/create", json=json_data, follow_redirects=True
        )
        assert response.status_code == 400

    def test_get_restaurant_id_by_owner_email_ok(self, client, db):
        """
        Test get restaurant info by id
        """
        email = "ham.burger@email.com"
        response = client.get("/restaurants/id/" + email, follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert json_data["id"] == 1

    def test_get_restaurant_id_by_owner_email_ko_404(self, client, db):
        """
        Test get name restaurant not found by id ko (404)
        """
        email = "notexists@noemail.com"
        response = client.get("/restaurants/id/" + email, follow_redirects=True)
        assert response.status_code == 404

    def test_put_restaurant_update_ok_200(self, client, db):
        """
        Test put update restaurant ok (200)
        """
        # get a restaurant for update
        response = client.get("/restaurants/" + str(2), follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        # test data before update
        assert json_data["name"] == "Pepperwood"
        assert json_data["phone"] == 555123427
        assert (
            json_data["covid_measures"]
            == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        )
        assert json_data["lat"] == 33.720586
        assert json_data["lon"] == 11.408347
        assert json_data["owner_email"] == "nick.miller@email.com"

        # add 'changed' keyword to string and change sign to number
        changed = "changed"
        json_data["name"] = "Pepperwood" + changed
        json_data["phone"] = 555123427 * -1
        json_data["covid_measures"] = (
            "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
            + changed
        )
        json_data["lat"] = 33.720586 * -1
        json_data["lon"] = 11.408347 * -1
        json_data["owner_email"] = "nick.miller@email.com" + changed
        response = client.put(
            "/restaurants/update", json=json_data, follow_redirects=True
        )
        assert response.status_code == 200

        # check updated data
        response = client.get("/restaurants/" + str(2), follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert json_data["name"] == "Pepperwood" + changed
        assert json_data["phone"] == (555123427 * -1)
        assert (
            json_data["covid_measures"]
            == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
            + changed
        )
        assert json_data["lat"] == (33.720586 * -1)
        assert json_data["lon"] == (11.408347 * -1)
        assert json_data["owner_email"] == "nick.miller@email.com" + changed

    def test_get_dishes_ok_noresults(self, client, db):
        """
        Test search dishes of a restaurant, no results
        """
        restaurant = Utils.create_restaurant()

        response = client.get(
            "/restaurants/" + str(restaurant.id) + "/dishes", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["dishes"]) == 0

        Utils.delete_restaurant(restaurant.id)

    def test_get_dishes_ok(self, client, db):
        """
        Test search dishes of a restaurant
        """
        restaurant = Utils.create_restaurant()
        dish = Utils.create_dish(restaurant.id, "Pizza")

        response = client.get(
            "/restaurants/" + str(restaurant.id) + "/dishes", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["dishes"]) == 1

        Utils.delete_dish(dish.id)
        Utils.delete_restaurant(restaurant.id)

    def test_get_dishes_restaurant_not_found(self, client, db):
        """
        Test search dishes of a restaurant that doesn't exist
        """
        restaurant_id = 100

        response = client.get(
            "/restaurants/" + str(restaurant_id) + "/dishes", follow_redirects=True
        )
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"

    def test_post_dishes_ok(self, client, db):
        """
        Test create a new dish
        """
        restaurant = Utils.create_restaurant()

        body = Utils.json_dish()
        response = client.post(
            "/restaurants/" + str(restaurant.id) + "/dishes",
            json=body,
            follow_redirects=True,
        )
        assert response.status_code == 201
        assert response.json["name"] == body["name"]

        Utils.delete_dish_restaurant(restaurant.id)
        Utils.delete_restaurant(restaurant.id)

    def test_post_dishes_restaurant_not_found(self, client, db):
        """
        Test create a new dish of a not existing restaurant
        """
        restaurant_id = 100

        body = Utils.json_dish()
        response = client.post(
            "/restaurants/" + str(restaurant_id) + "/dishes",
            json=body,
            follow_redirects=True,
        )
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"

    def test_delete_dishes_ok(self, client, db):
        """
        Test delete a dish
        """
        restaurant = Utils.create_restaurant()
        dish = Utils.create_dish(restaurant.id, "Pizza")

        response = client.delete(
            "/restaurant/menu/" + str(dish.id), follow_redirects=True
        )

        assert response.status_code == 200
        assert response.json["result"] == "OK"
        assert Utils.get_dish(dish.id) is None

        Utils.delete_restaurant(restaurant.id)

    def test_get_tables_ok_noresults(self, client, db):
        """
        Test search table of a restaurant, no results
        """
        restaurant = Utils.create_restaurant()

        response = client.get(
            "/restaurants/" + str(restaurant.id) + "/tables", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["tables"]) == 0

        Utils.delete_restaurant(restaurant.id)

    def test_get_tables_ok(self, client, db):
        """
        Test search tables of a restaurant
        """
        restaurant = Utils.create_restaurant()
        table = Utils.create_table(restaurant.id)

        response = client.get(
            "/restaurants/" + str(restaurant.id) + "/tables", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["tables"]) == 1

        Utils.delete_table(table.id)
        Utils.delete_restaurant(restaurant.id)

    def test_get_tables_restaurant_not_found(self, client, db):
        """
        Test search tables of a restaurant that doesn't exist
        """
        restaurant_id = 100

        response = client.get(
            "/restaurants/" + str(restaurant_id) + "/tables", follow_redirects=True
        )
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"

    def test_post_tables_ok(self, client, db):
        """
        Test create a new table
        """
        restaurant = Utils.create_restaurant()

        body = Utils.json_table()
        response = client.post(
            "/restaurants/" + str(restaurant.id) + "/tables",
            json=body,
            follow_redirects=True,
        )
        assert response.status_code == 201
        assert response.json["name"] == body["name"]

        Utils.delete_table_restaurant(restaurant.id)
        Utils.delete_restaurant(restaurant.id)

    def test_post_table_restaurant_not_found(self, client, db):
        """
        Test create a new table of a not existing restaurant
        """
        restaurant_id = 100

        body = Utils.json_table()
        response = client.post(
            "/restaurants/" + str(restaurant_id) + "/tables",
            json=body,
            follow_redirects=True,
        )
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"

    def test_delete_tables_ok(self, client, db):
        """
        Test delete a table
        """
        restaurant = Utils.create_restaurant()
        table = Utils.create_table(restaurant.id)

        response = client.delete(
            "/restaurant/table/" + str(table.id), follow_redirects=True
        )

        assert response.status_code == 200
        assert response.json["result"] == "OK"
        assert Utils.get_table(table.id) is None

        Utils.delete_restaurant(restaurant.id)

    def test_get_openings_ok_noresults(self, client, db):
        """
        Test search opening hours of a restaurant, no results
        """
        restaurant = Utils.create_restaurant()

        response = client.get(
            "/restaurants/" + str(restaurant.id) + "/openings", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["openings"]) == 0

        Utils.delete_restaurant(restaurant.id)

    def test_get_openings_ok(self, client, db):
        """
        Test search opening hours of a restaurant
        """
        restaurant = Utils.create_restaurant()
        opening1 = Utils.create_openings(restaurant.id, 2)
        opening2 = Utils.create_openings(restaurant.id, 4)

        response = client.get(
            "/restaurants/" + str(restaurant.id) + "/openings", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["openings"]) == 2

        Utils.delete_openings(opening1)
        Utils.delete_openings(opening2)
        Utils.delete_restaurant(restaurant.id)

    def test_get_openings_restaurant_not_found(self, client, db):
        """
        Test search openings of a restaurant that doesn't exist
        """
        restaurant_id = 100

        response = client.get(
            "/restaurants/" + str(restaurant_id) + "/openings", follow_redirects=True
        )
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"

    def test_get_menu_ok_noresults(self, client, db):
        """
        Test search menus of a restaurant, no results
        """
        restaurant = Utils.create_restaurant()

        response = client.get(
            "/restaurants/" + str(restaurant.id) + "/menu", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["menus"]) == 0

        Utils.delete_restaurant(restaurant.id)

    def test_get_menu_ok(self, client, db):
        """
        Test search menu of a restaurant
        """
        restaurant = Utils.create_restaurant()
        menu1 = Utils.create_menu(restaurant.id, "Italian food")
        menu2 = Utils.create_menu(restaurant.id, "Chinese food")

        response = client.get(
            "/restaurants/" + str(restaurant.id) + "/menu", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["menus"]) == 2

        Utils.delete_menu(menu1.id)
        Utils.delete_menu(menu2.id)
        Utils.delete_restaurant(restaurant.id)

    def test_get_menu_restaurant_not_found(self, client, db):
        """
        Test search menu of a restaurant that doesn't exist
        """
        restaurant_id = 100

        response = client.get(
            "/restaurants/" + str(restaurant_id) + "/menu", follow_redirects=True
        )
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"

    def test_post_menu_photo_ok(self, client, db):
        """
        Test create a new menu photo
        """
        restaurant = Utils.create_restaurant()
        menu = Utils.create_menu(restaurant.id, "Italian food")

        body = Utils.json_photo()
        response = client.post(
            "/restaurants/menu/" + str(menu.id), json=body, follow_redirects=True
        )
        assert response.status_code == 201
        assert response.json["url"] == body["url"]

        Utils.delete_menu_photo_by_menu(menu.id)
        Utils.delete_menu(menu.id)
        Utils.delete_restaurant(restaurant.id)

    def test_post_photo_to_menu_not_found(self, client, db):
        """
        Test create a new photo of a not existing menu
        """
        menu_id = 100

        body = Utils.json_photo()
        response = client.post(
            "/restaurants/menu/" + str(menu_id), json=body, follow_redirects=True
        )
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Menu not found"

    def test_post_photo_to_menu_url_already_used(self, client, db):
        """
        Test create a new photo of the menu but with an URL that already exists
        """
        restaurant = Utils.create_restaurant()
        menu = Utils.create_menu(restaurant.id, "Italian food")

        body = Utils.json_photo()
        response = client.post(
            "/restaurants/menu/" + str(menu.id), json=body, follow_redirects=True
        )
        assert response.status_code == 201
        assert response.json["url"] == body["url"]

        response = client.post(
            "/restaurants/menu/" + str(menu.id), json=body, follow_redirects=True
        )
        assert response.status_code == 409
        assert response.json["message"] == "URL already present"

        Utils.delete_menu_photo_by_menu(menu.id)
        Utils.delete_menu(menu.id)
        Utils.delete_restaurant(restaurant.id)

    def test_get_calculate_rating_for_all_restaurant_ok(self, client, db):
        """
        Test get calculate rating for all restaurant
        """
        response = client.get(
            "/restaurants/calculate_rating_for_all_restaurant", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert json_data["result"] is True

    def test_get_avg_rating_ok(self, client, db):
        """
        Test get calculate rating for all restaurant
        """
        response = client.get(
            "/restaurants/" + str(1) + "/avg_rating", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert round(json_data["result"], 1) == 2.7

    def test_get_avg_rating_ko_404(self, client, db):
        """
        Test get calculate rating for all restaurant
        """
        response = client.get(
            "/restaurants/" + str(123) + "/avg_rating", follow_redirects=True
        )
        assert response.status_code == 404

    def test_get_reviews_ok(self, client, db):
        """
        Test get calculate rating for all restaurant
        """
        response = client.get(
            "/restaurants/" + str(1) + "/reviews", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["Reviews"]) == 3
        assert json_data["Reviews"][0]["review"] == "Excellent"
        assert json_data["Reviews"][1]["review"] == "Bad"
        assert json_data["Reviews"][2]["review"] == "Beautiful"
        assert json_data["Reviews"][0]["stars"] == 4
        assert json_data["Reviews"][1]["stars"] == 1
        assert json_data["Reviews"][2]["stars"] == 3
        assert json_data["Reviews"][0]["stars"] == 4
        assert json_data["Reviews"][1]["stars"] == 1
        assert json_data["Reviews"][2]["stars"] == 3
        assert json_data["Reviews"][0]["reviewer_email"] == "user@email.com"
        assert json_data["Reviews"][1]["reviewer_email"] == "user2@email.com"
        assert json_data["Reviews"][2]["reviewer_email"] == "user3@email.com"

    def test_get_reviews_ko_404(self, client, db):
        """
        Test get reviews for restaurant not found
        """
        response = client.get(
            "/restaurants/" + str(123) + "/reviews", follow_redirects=True
        )
        assert response.status_code == 404

    def test_get_random_reviews_ok(self, client, db):
        """
        Test get random reviews for restaurant
        """
        n = 3
        response = client.get(
            "/restaurants/" + str(1) + "/reviews/" + str(n), follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["Reviews"]) == n

    def test_get_random_reviews_ko_404(self, client, db):
        """
        Test get random reviews for restaurant not found
        """
        response = client.get(
            "/restaurants/" + str(123) + "/reviews/" + str(10), follow_redirects=True
        )
        assert response.status_code == 404

    """
    POST
    /restaurants/{restaurant_id}/reviews
    Create a new review for the restaurant
    """

    def test_post_review_to_restaurants(self, client, db):
        """
        Test create a new reviews for restaurants
        """
        body = Utils.json_review()
        response = client.post(
            "/restaurants/" + str(1) + "/reviews", json=body, follow_redirects=True
        )
        assert response.status_code == 201
        assert response.json["stars"] == body["stars"]
        Utils.delete_review(4)

    def test_get_photos_restaurant_ok(self, client, db):
        """
        Test Get the photos of a single restaurant
        """
        response = client.get(
            "/restaurants/" + str(1) + "/photos", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["photos"]) == 3
        assert json_data["photos"][0]["caption"] == "Caption 1"
        assert json_data["photos"][1]["caption"] == "Caption 2"
        assert json_data["photos"][2]["caption"] == "Caption 3"
        assert json_data["photos"][0]["restaurant_id"] == 1
        assert json_data["photos"][1]["restaurant_id"] == 1
        assert json_data["photos"][2]["restaurant_id"] == 1
        assert json_data["photos"][0]["url"] == "http://myrestaurant.com/photo1.jpg"
        assert json_data["photos"][1]["url"] == "http://myrestaurant.com/photo2.jpg"
        assert json_data["photos"][2]["url"] == "http://myrestaurant.com/photo3.jpg"

    def test_get_photos_restaurant_ko_404(self, client, db):
        """
        Test get photos for restaurant not found
        """
        response = client.get(
            "/restaurants/" + str(123) + "/photos/" + str(10), follow_redirects=True
        )
        assert response.status_code == 404

    def test_post_photo_to_restaurants(self, client, db):
        """
        Test create a new photo for restaurants
        """
        body = Utils.json_photo()
        response = client.post(
            "/restaurants/" + str(1) + "/photos", json=body, follow_redirects=True
        )
        assert response.status_code == 201
        assert response.json["url"] == body["url"]

        Utils.delete_photo(4)

    def test_post_photo_to_restaurants_ko_404(self, client, db):
        """
        Test create a new photo for restaurants not found
        """
        body = Utils.json_photo()
        response = client.post(
            "/restaurants/" + str(123) + "/photos", json=body, follow_redirects=True
        )
        assert response.status_code == 404

    def test_post_photo_to_restaurants_ko_409(self, client, db):
        """
        Test create a new photo for restaurants url already exists
        """
        body = Utils.json_photo()
        print(body)
        response = client.post(
            "/restaurants/" + str(1) + "/photos", json=body, follow_redirects=True
        )
        assert response.status_code == 201
        response = client.post(
            "/restaurants/" + str(1) + "/photos", json=body, follow_redirects=True
        )
        assert response.status_code == 409

    def test_delete_restaurant_all_info_ok(self, client, db):
        """
        Test delete a restaurant with all its information
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

        response = client.delete(
            "/restaurants/" + str(new_restaurant.id), follow_redirects=True
        )

        assert response.status_code == 200
        assert response.json["result"] == "OK"

        assert Utils.get_restaurant(new_restaurant.id) is None
        assert Utils.get_table(new_table.id) is None
        assert Utils.get_menu(new_menu.id) is None
        assert Utils.get_menu(new_menu_photo.id) is None
        assert len(Utils.get_opening_by_restaurant(new_restaurant.id)) == 0
        assert Utils.get_review(new_review.id) is None
        assert Utils.get_photo(new_photo.id) is None
        assert Utils.get_dish(new_dish.id) is None

    def test_delete_restaurant_all_info_not_found(self, client, db):
        """
        Test delete a restaurant with all its information for a restaurant that
        doesn't exist
        """

        response = client.delete("/restaurants/" + str(100), follow_redirects=True)

        assert response.status_code == 404
        assert response.json["message"] == "Restaurant not found"

    def test_get_table_ok(self, client, db):
        """
        Test search tables of a restaurant
        """
        restaurant = Utils.create_restaurant()
        table = Utils.create_table(restaurant.id)

        response = client.get(
            "/restaurants/" + str(restaurant.id) + "/tables", follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["tables"]) == 1

        response = client.get(
            "/restaurants/table/" + str(table.id) , follow_redirects=True
        )
        assert response.status_code == 200
        json_data = response.json
        assert json_data["id"] == table.id
        assert json_data["restaurant"]["name"] == restaurant.name

        Utils.delete_table(table.id)
        Utils.delete_restaurant(restaurant.id)