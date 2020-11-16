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
        assert response.json['name'] == "Pepperwood"
        assert response.json['phone'] == 555123427
        assert response.json[
                   'covid_measures'] == "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
        assert response.json['lat'] == 33.720586
        assert response.json['lon'] == 11.408347
        assert response.json['owner_email'] == "nick.miller@email.com"

    def test_get_restaurant_ko_404(self, client, db):
        """
        Test get restaurant by id not found (404)
        """
        response = client.get("/restaurants/" + str(123), follow_redirects=True)
        assert response.status_code == 404

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
Mariagiovanna: Dishes, Tables, Menu, Opening Hours 

Renato: Restaurants, Photos, Reviews
'''