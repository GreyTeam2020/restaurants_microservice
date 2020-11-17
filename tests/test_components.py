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
        assert json_data['name'] == "Pepperwood"
        assert json_data['phone'] == 555123427
        assert json_data['covid_measures'] == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        assert json_data['lat'] == 33.720586
        assert json_data['lon'] == 11.408347
        assert json_data['owner_email'] == "nick.miller@email.com"

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
        assert json_data['result'] == "Pepperwood"

    def test_get_restaurant_name_by_id_ko_404(self, client, db):
        """
        Test get name restaurant not found by id ko (404)
        """
        response = client.get("/restaurants/" + str(123) + "/name", follow_redirects=True)
        assert response.status_code == 404

    def test_get_restaurant_info_ok(self, client, db):
        """
        Test get restaurant info by id
        """
        response = client.get("/restaurants/" + str(2) + "/info", follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert json_data['Restaurant_info']['Restaurant']['name'] == "Pepperwood"
        assert json_data['Restaurant_info']['Restaurant']['phone'] == 555123427
        assert json_data['Restaurant_info']['Restaurant']['covid_measures'] == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        assert json_data['Restaurant_info']['Restaurant']['lat'] == 33.720586
        assert json_data['Restaurant_info']['Restaurant']['lon'] == 11.408347
        assert json_data['Restaurant_info']['Restaurant']['owner_email'] == "nick.miller@email.com"

        assert json_data['Restaurant_info']['Menus'][0]['cusine'] == "Italian food"
        assert json_data['Restaurant_info']['Menus'][0]['description'] == "local food"
        assert json_data['Restaurant_info']['Menus'][0]['id'] == 1

        assert json_data['Restaurant_info']['Menus'][0]['photos'][0]['caption'] == "Photo 1"
        assert json_data['Restaurant_info']['Menus'][0]['photos'][0]['id'] == 1
        assert json_data['Restaurant_info']['Menus'][0]['photos'][0]['url'] == "http://photo1.com"

    def test_get_restaurant_info_ko_404(self, client, db):
        """
        Test get name restaurant not found by id ko (404)
        """
        response = client.get("/restaurants/" + str(123) + "/info", follow_redirects=True)
        assert response.status_code == 404

    def test_get_restaurants_by_keyword_ok(self, client, db):
        """
        Test search restaurant by keywords
        """
        keyword = "pep"
        response = client.get("/restaurants/search/" + keyword, follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert json_data['restaurants'][0]['name'] == "Pepperwood"
        assert json_data['restaurants'][0]['phone'] == 555123427
        assert json_data['restaurants'][0]['covid_measures'] == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        assert json_data['restaurants'][0]['lat'] == 33.720586
        assert json_data['restaurants'][0]['lon'] == 11.408347
        assert json_data['restaurants'][0]['owner_email'] == "nick.miller@email.com"

    def test_get_restaurants_by_keyword_ok_noresults(self, client, db):
        """
        Test search restaurant by keywords, no results
        """
        keyword = "notexists"
        response = client.get("/restaurants/search/" + keyword, follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data['restaurants']) == 0

    def test_post_restaurant_create_ok(self, client, db):
        """
        Test get create restaurant ok (200)
        """
        json_data = Utils.json_create_restaurant()
        response = client.post("/restaurants/create", json=json_data, follow_redirects=True)
        assert response.status_code == 200
        Utils.delete_creation_restaurant(json_data)

    def test_post_restaurant_create_ko_409(self, client, db):
        """
        Test get create restaurant ok (200)
        """
        json_data = Utils.json_create_restaurant()
        response = client.post("/restaurants/create", json=json_data, follow_redirects=True)
        assert response.status_code == 200

        """
        Test get create restaurant ko (409) because is duplicate 
        """
        response = client.post("/restaurants/create", json=json_data, follow_redirects=True)
        assert response.status_code == 409
        Utils.delete_creation_restaurant(json_data)

    def test_post_restaurant_create_ko_400(self, client, db):
        """
        Test get create restaurant ko (400), phone missing
        """
        json_data = Utils.json_create_restaurant()
        json_data['restaurant']['phone'] = None
        response = client.post("/restaurants/create", json=json_data, follow_redirects=True)
        assert response.status_code == 400

    '''
    def test_put_restaurant_update_ok_200(self, client, db):
        """
        Test put update restaurant ok (200)
        """
        # get a restaurant for update
        response = client.get("/restaurants/" + str(2), follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        # test data before update
        assert json_data['name'] == "Pepperwood"
        assert json_data['phone'] == 555123427
        assert json_data['covid_measures'] == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        assert json_data['lat'] == 33.720586
        assert json_data['lon'] == 11.408347
        assert json_data['owner_email'] == "nick.miller@email.com"

        # add 'changed' keyword to string and change sign to number
        changed = 'changed'
        json_data['name'] = "Pepperwood" + changed
        json_data['phone']= (555123427 * -1)
        json_data['covid_measures'] = "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment" + changed
        json_data['lat'] = (33.720586 * -1)
        json_data['lon'] = (11.408347 * -1)
        json_data['owner_email'] = "nick.miller@email.com" + changed
        response = client.put("/restaurants/update", json=json_data, follow_redirects=True)
        assert response.status_code == 200

        # check updated data
        response = client.get("/restaurants/" + str(2), follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert json_data['name'] == "Pepperwood" + changed
        assert json_data['phone'] == (555123427 * -1)
        assert json_data['covid_measures'] == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment" + changed
        assert json_data['lat'] == (33.720586 * -1)
        assert json_data['lon'] == (11.408347 * -1)
        assert json_data['owner_email'] == "nick.miller@email.com" + changed
        '''

    '''
    Mariagiovanna: Dishes, Tables, Menu, Opening Hours 

    Renato: Restaurants, Photos, Reviews
    '''


    def test_get_dishes_ok_noresults(self, client, db):
        """
        Test search dishes of a restaurant, no results
        """
        restaurant = Utils.create_restaurant()
        
        response = client.get("/restaurants/"+ str(restaurant.id)+"/dishes", follow_redirects=True)
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

        response = client.get("/restaurants/"+ str(restaurant.id)+"/dishes", follow_redirects=True)
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

        response = client.get("/restaurants/"+ str(restaurant_id)+"/dishes", follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"


    def test_post_dishes_ok(self, client, db):
        """
        Test create a new dish
        """
        restaurant = Utils.create_restaurant()

        body = Utils.json_dish()
        response = client.post("/restaurants/"+ str(restaurant.id)+ "/dishes", json=body, follow_redirects=True)
        assert response.status_code == 200
        assert response.json["result"] == "Dish added"

        Utils.delete_dish_restaurant(restaurant.id)
        Utils.delete_restaurant(restaurant.id)

    def test_post_dishes_restaurant_not_found(self, client, db):
        """
        Test create a new dish of a not existing restaurant
        """
        restaurant_id = 100

        body = Utils.json_dish()
        response = client.post("/restaurants/"+ str(restaurant_id)+ "/dishes", json=body, follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"


    def test_delete_dishes_ok(self, client, db):
        """
        Test delete a dish
        """
        restaurant = Utils.create_restaurant()
        dish = Utils.create_dish(restaurant.id, "Pizza")
        
        response = client.delete("/restaurant/menu/"+str(dish.id), follow_redirects=True)
        
        assert response.status_code == 200
        assert response.json["result"] == "OK"
        assert Utils.get_dish(dish.id) is None

        Utils.delete_restaurant(restaurant.id)


    def test_get_tables_ok_noresults(self, client, db):
        """
        Test search table of a restaurant, no results
        """
        restaurant = Utils.create_restaurant()
        
        response = client.get("/restaurants/"+ str(restaurant.id)+"/tables", follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["Tables"]) == 0

        Utils.delete_restaurant(restaurant.id)

    def test_get_tables_ok(self, client, db):
        """
        Test search tables of a restaurant
        """
        restaurant = Utils.create_restaurant()
        table = Utils.create_table(restaurant.id)

        response = client.get("/restaurants/"+ str(restaurant.id)+"/tables", follow_redirects=True)
        assert response.status_code == 200
        json_data = response.json
        assert len(json_data["Tables"]) == 1

        Utils.delete_table(table.id)
        Utils.delete_restaurant(restaurant.id)

    def test_get_tables_restaurant_not_found(self, client, db):
        """
        Test search tables of a restaurant that doesn't exist
        """
        restaurant_id = 100

        response = client.get("/restaurants/"+ str(restaurant_id)+"/tables", follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"


    def test_post_tables_ok(self, client, db):
        """
        Test create a new table
        """
        restaurant = Utils.create_restaurant()

        body = Utils.json_table()
        response = client.post("/restaurants/"+ str(restaurant.id)+ "/tables", json=body, follow_redirects=True)
        assert response.status_code == 200
        assert response.json["result"] == "Table added to restaurant"

        Utils.delete_table_restaurant(restaurant.id)
        Utils.delete_restaurant(restaurant.id)

    def test_post_table_restaurant_not_found(self, client, db):
        """
        Test create a new table of a not existing restaurant
        """
        restaurant_id = 100

        body = Utils.json_table()
        response = client.post("/restaurants/"+ str(restaurant_id)+ "/tables", json=body, follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"


    def test_delete_tables_ok(self, client, db):
        """
        Test delete a table
        """
        restaurant = Utils.create_restaurant()
        table = Utils.create_table(restaurant.id)
        
        response = client.delete("/restaurant/table/"+str(table.id), follow_redirects=True)
        
        assert response.status_code == 200
        assert response.json["result"] == "OK"
        assert Utils.get_table(table.id) is None

        Utils.delete_restaurant(restaurant.id)


    def test_get_openings_ok_noresults(self, client, db):
        """
        Test search opening hours of a restaurant, no results
        """
        restaurant = Utils.create_restaurant()
        
        response = client.get("/restaurants/"+ str(restaurant.id)+"/openings", follow_redirects=True)
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

        response = client.get("/restaurants/"+ str(restaurant.id)+"/openings", follow_redirects=True)
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

        response = client.get("/restaurants/"+ str(restaurant_id)+"/openings", follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"







    
    def test_get_menu_ok_noresults(self, client, db):
        """
        Test search menus of a restaurant, no results
        """
        restaurant = Utils.create_restaurant()
        
        response = client.get("/restaurants/"+ str(restaurant.id)+"/menu", follow_redirects=True)
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

        response = client.get("/restaurants/"+ str(restaurant.id)+"/menu", follow_redirects=True)
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

        response = client.get("/restaurants/"+ str(restaurant_id)+"/menu", follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"


    def test_post_menu_photo_ok(self, client, db):
        """
        Test create a new menu
        """
        restaurant = Utils.create_restaurant()
        menu = Utils.create_menu(restaurant.id, "Italian food")

        body = Utils.json_photo()
        response = client.post("/restaurants/menu/"+ str(menu.id), json=body, follow_redirects=True)
        assert response.status_code == 200
        assert response.json["result"] == "Photo of the menu added"

        Utils.delete_menu_photo_by_menu(menu.id)
        Utils.delete_menu(menu.id)
        Utils.delete_restaurant(restaurant.id)

    def test_post_table_restaurant_not_found(self, client, db):
        """
        Test create a new table of a not existing restaurant
        """
        restaurant_id = 100

        body = Utils.json_table()
        response = client.post("/restaurants/"+ str(restaurant_id)+ "/tables", json=body, follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["message"] == "Restaurant not found"