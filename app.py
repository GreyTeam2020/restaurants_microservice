import connexion, logging, database
import os
from database import init_db
from flask import jsonify, request
from services.restaurant_service import RestaurantService
import json

db_session = None

_max_seats = 6


def _get_response(message: str, code: int, is_custom_obj: bool = False):
    """
    This method contains the code to make a new response for flask view
    :param message: Message response
    :param code: Code result
    :return: a json object that look like {"result": "OK"}
    """
    if is_custom_obj is False:
        return {"result": message}, code
    return message, code


def serialize(obj):
    return dict([(k, v) for k, v in obj.__dict__.items() if k[0] != "_"])


# time objects are not serializeble in JSON so they are changed in strings
def times_to_strings(obj_dict):
    for key, value in obj_dict.items():
        if str(type(value)) == "<class 'datetime.time'>":
            obj_dict.update({key: value.strftime("%H:%M")})
    return obj_dict


def list_obj_json(name_list, list_objs):
    objects = []
    for obj in list_objs:
        objects.append(times_to_strings(serialize(obj)))
    list_json = json.dumps({name_list: objects})
    return json.loads(list_json)


def error_message(code, message):
    return json.loads(json.dumps({"code": code, "message": message}))


def get_restaurants():

    restaurants = RestaurantService.get_all_restaurants(db_session)
    if restaurants is None:
        return error_message("404", "Restaurants not found"), 404
    else:
        return list_obj_json("restaurants", restaurants)


def get_restaurant(restaurant_id):

    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404
    else:
        return serialize(restaurant)


def get_menus(restaurant_id):

    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    menus = RestaurantService.get_menus(db_session, restaurant_id)
    if len(menus) == 0:
        return error_message("404", "Menus not found"), 404
    else:

        all_menus = []
        # get menu photos for each menu
        for menu in menus:
            photos = RestaurantService.get_menu_photos(db_session, menu.id)
            json_menu = serialize(menu)
            photos_list = []
            for photo in photos:
                photos_list.append(serialize(photo))
            json_menu["photos"] = photos_list
            all_menus.append(json_menu)

        return json.loads(json.dumps({"menus": all_menus}))


def get_dishes(restaurant_id):

    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    dishes = RestaurantService.get_dishes(db_session, restaurant_id)
    if len(dishes) == 0:
        return error_message("404", "Dishes not found"), 404
    else:
        return list_obj_json("dishes", dishes)


def get_openings(restaurant_id):

    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    openings = RestaurantService.get_openings(db_session, restaurant_id)
    if len(openings) == 0:
        return error_message("404", "Opening hours not found"), 404
    else:
        return list_obj_json("opening hours", openings)


def get_tables(restaurant_id):

    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    tables = RestaurantService.get_tables(db_session, restaurant_id)
    if len(tables) == 0:
        return error_message("404", "Tables not found"), 404
    else:
        return list_obj_json("Tables", tables)


def get_photos(restaurant_id):

    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    photos = RestaurantService.get_photos(db_session, restaurant_id)
    if len(photos) == 0:
        return error_message("404", "Photos not found"), 404
    else:
        return list_obj_json("Photos", photos)


def get_reviews(restaurant_id):

    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    reviews = RestaurantService.get_reviews(db_session, restaurant_id)

    if len(reviews) == 0:
        return error_message("404", "Reviews not found"), 404
    else:
        return list_obj_json("Reviews", reviews)


def get_random_reviews(restaurant_id, number):

    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    reviews = RestaurantService.get_reviews_random(db_session, restaurant_id, number)
    if len(reviews) == 0:
        return error_message("404", "Reviews not found"), 404
    else:
        return list_obj_json("Reviews", reviews)


def create_restaurant():

    body = request.get_json()

    # check if the restaurant already exists (phone number, lat, lon, name)
    name = body["restaurant"]["name"]
    phone = body["restaurant"]["phone"]
    lat = body["restaurant"]["lat"]
    lon = body["restaurant"]["lon"]

    # if the restaurant already exists: error
    if (
        RestaurantService.get_restaurant_with_info(db_session, name, phone, lat, lon)
        is True
    ):
        return error_message("409", "Restaurant already exists"), 409

    # add restaurant
    RestaurantService.create_restaurant(db_session, body, _max_seats)
    # return response
    return _get_response("Restaurant is been created", 200, False)


def create_table(restaurant_id):

    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    body = request.get_json()
    RestaurantService.create_table(
        db_session, body["name"], body["max_seats"], restaurant_id
    )
    return _get_response("Table added to restaurant", 200, False)


def create_dish(restaurant_id):
    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    body = request.get_json()
    RestaurantService.create_dish(
        db_session, body["name"], body["price"], restaurant_id
    )
    return _get_response("Dish added", 200, False)


def create_photo(restaurant_id):
    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    body = request.get_json()

    RestaurantService.create_restaurant_photo(
        db_session, body["url"], body["caption"], restaurant_id
    )
    return _get_response("Photo added", 200, False)


def create_review(restaurant_id):
    restaurant = RestaurantService.get_restaurant(db_session, restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    body = request.get_json()

    photo = RestaurantService.get_photo_with_url(db_session, body["url"])
    if photo is not None:
        return error_message("409", "URL already present"), 409

    RestaurantService.create_review(
        db_session, body["review"], body["stars"], body["reviewer_email"], restaurant_id
    )

    return _get_response("Review added", 200, False)


def create_menu_photo(menu_id):
    menu = RestaurantService.get_menu(db_session, menu_id)
    if menu is None:
        return error_message("404", "Menu not found"), 404

    body = request.get_json()

    photo = RestaurantService.get_menu_photo_with_url(db_session, body["url"])
    if photo is not None:
        return error_message("409", "URL already present"), 409

    RestaurantService.create_menu_photo(
        db_session, body["url"], body["caption"], menu_id
    )

    return _get_response("Photo of the menu added", 200, False)


def delete_dish(dish_id):
    if dish_id is None:
        return error_message("400", "dish_id not specified"), 400
    RestaurantService.delete_dish(db_session, dish_id)
    return _get_response("OK", 200)


def delete_table(table_id):
    if table_id is None:
        return error_message("400", "table_id not specified"), 400
    RestaurantService.delete_table(db_session, table_id)
    return _get_response("OK", 200)


# --------- END API definition --------------------------
logging.basicConfig(level=logging.INFO)

app = connexion.App(__name__)

application = app.app
if "GOUOUTSAFE_TEST" in os.environ and os.environ["GOUOUTSAFE_TEST"] == "1":
    db_session = init_db("sqlite:///tests/restaurant.db")
else:
    db_session = init_db("sqlite:///restaurant.db")
app.add_api("swagger.yml")
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app


def _init_flask_app(flask_app, conf_type: str = "config.DebugConfiguration"):
    """
    This method init the flask app
    :param flask_app:
    """
    flask_app.config.from_object(conf_type)


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    _init_flask_app(application)
    app.run(port=5003)
