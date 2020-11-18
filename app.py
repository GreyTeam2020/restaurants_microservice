import connexion, logging, database
import os
from database import init_db
from flask import current_app, request
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
def JSON_serialization(obj_dict):
    for key, value in obj_dict.items():
        if str(type(value)) == "<class 'datetime.time'>":
            obj_dict.update({key: value.strftime("%H:%M")})
        elif str(type(value)) == "<class 'datetime.datetime'>":
            obj_dict.update({key: value.strftime("%m/%d/%Y, %H:%M:%S")})
        elif str(type(value)) == "<class 'decimal.Decimal'>":
            obj_dict.update({key: float(value)})
    return obj_dict


def list_obj_json(name_list, list_objs):
    objects = []
    for obj in list_objs:
        objects.append(JSON_serialization(serialize(obj)))
    if len(name_list) == 0:
        return objects
    else:
        list_json = json.dumps({name_list: objects})
        return json.loads(list_json)


def error_message(code, message):
    return json.loads(json.dumps({"code": code, "message": message}))


def get_restaurants():
    restaurants = RestaurantService.get_all_restaurants()
    return list_obj_json("restaurants", restaurants)


def get_restaurant(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404
    else:
        return serialize(restaurant)


def get_restaurant_name(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404
    else:
        return _get_response(restaurant.name, 200)

def get_restaurant_id_by_owner_email(owner_email):

    restaurant_id = RestaurantService.get_restaurants_by_owner_email(owner_email)
    if restaurant_id == -1:
        return error_message("404", "Owner not found"), 404
    else:
        return json.loads(json.dumps({"result": restaurant_id}))

def get_restaurants_by_keyword(name):
    restaurants = RestaurantService.get_restaurants_by_keyword_name(name)
    return list_obj_json("restaurants", restaurants)


def get_menus(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    menus = RestaurantService.get_menus(restaurant_id)

    all_menus = []
    # get menu photos for each menu
    for menu in menus:
        photos = RestaurantService.get_menu_photos(menu.id)
        json_menu = serialize(menu)
        photos_list = []
        for photo in photos:
            photos_list.append(serialize(photo))
        json_menu["photos"] = photos_list
        all_menus.append(json_menu)

    return json.loads(json.dumps({"menus": all_menus}))


def get_dishes(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    dishes = RestaurantService.get_dishes(restaurant_id)
    return list_obj_json("dishes", dishes)


def get_openings(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    openings = RestaurantService.get_openings(restaurant_id)
    return list_obj_json("openings", openings)


def get_tables(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    tables = RestaurantService.get_tables(restaurant_id)
    return list_obj_json("tables", tables)


def get_photos(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    photos = RestaurantService.get_photos(restaurant_id)
    return list_obj_json("photos", photos)


def get_reviews(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    reviews = RestaurantService.get_reviews(restaurant_id)
    return list_obj_json("Reviews", reviews)


def get_random_reviews(restaurant_id, number):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    reviews = RestaurantService.get_reviews_random(restaurant_id, number)
    return list_obj_json("Reviews", reviews)


def get_restaurant_more_info(restaurant_id):
    # get restaurant and check if restaurant exists
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    info = dict()
    info["Restaurant"] = serialize(restaurant)

    # get menus
    menus = RestaurantService.get_menus(restaurant_id)
    all_menus = []
    # get menu photos for each menu
    for menu in menus:
        photos = RestaurantService.get_menu_photos(menu.id)
        json_menu = serialize(menu)
        photos_list = []
        for photo in photos:
            photos_list.append(serialize(photo))
        json_menu["photos"] = photos_list
        all_menus.append(json_menu)
    info["Menus"] = all_menus

    # get photos about restaurant
    photos = RestaurantService.get_photos(restaurant_id)
    info["Photos"] = list_obj_json("", photos)

    # get dishes
    dishes = RestaurantService.get_dishes(restaurant_id)
    info["Dishes"] = list_obj_json("", dishes)

    # get openings
    openings = RestaurantService.get_openings(restaurant_id)
    info["Openings"] = list_obj_json("", openings)

    return json.loads(json.dumps({"Restaurant_info": info}))


def create_restaurant():
    body = request.get_json()

    # check if the restaurant already exists (phone number, lat, lon, name)
    name = body["restaurant"]["name"]
    phone = body["restaurant"]["phone"]
    lat = body["restaurant"]["lat"]
    lon = body["restaurant"]["lon"]

    # if the restaurant already exists: error

    if RestaurantService.get_restaurant_with_info(name, phone, lat, lon) is not None:
        return error_message("409", "Restaurant already exists"), 409

    rest = RestaurantService.create_restaurant(body, _max_seats)
    json_resp = serialize(rest)
    if rest is None:
        return _get_response("An error occur during the restaurants creation", 500)
    current_app.logger.debug("Result is: {}".format(json_resp))
    return _get_response(json_resp, 200, True)


def create_table(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    body = request.get_json()
    RestaurantService.create_table(body["name"], body["max_seats"], restaurant_id)
    return _get_response("Table added to restaurant", 200)


def create_dish(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    body = request.get_json()
    RestaurantService.create_dish(body["name"], body["price"], restaurant_id)
    return _get_response("Dish added", 200)


def create_photo(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    body = request.get_json()

    photo = RestaurantService.get_photo_with_url(body["url"])
    if len(photo) is not 0:
        return error_message("409", "URL already present"), 409

    RestaurantService.create_restaurant_photo(
        body["url"], body["caption"], restaurant_id
    )
    return _get_response("Photo added", 200)


def create_review(restaurant_id):
    restaurant = RestaurantService.get_restaurant(restaurant_id)
    if restaurant is None:
        return error_message("404", "Restaurant not found"), 404

    body = request.get_json()

    RestaurantService.create_review(
        body["review"], body["stars"], body["reviewer_email"], restaurant_id
    )

    return _get_response("Review added", 200)


def create_menu_photo(menu_id):
    menu = RestaurantService.get_menu(menu_id)
    if menu is None:
        return error_message("404", "Menu not found"), 404

    body = request.get_json()

    photo = RestaurantService.get_menu_photo_with_url(body["url"])
    if photo is not None:
        return error_message("409", "URL already present"), 409

    RestaurantService.create_menu_photo(body["url"], body["caption"], menu_id)

    return _get_response("Photo of the menu added", 200)


def get_avg_rating_restaurant(restaurant_id):
    """
    get avg of rating for a restaurant
    """
    if restaurant_id is None:
        return error_message("400", "dish_id not specified"), 400
    rating = RestaurantService.get_avg_rating_restaurant(restaurant_id)
    if rating == -1:
        return _get_response(rating, 404)
    else:
        return _get_response(rating, 200)


def calculate_rating_for_all_restaurant():
    """
    calculate rating for all restaurant(celery)
    """
    done = RestaurantService.calculate_rating_for_all_restaurant()
    return _get_response(done, 200)


def update_restaurant_info():
    """
    update the restaurant infos
    """
    data = request.get_json()
    result = RestaurantService.update_restaurant_info(data)

    if result is False:
        return error_message("500", "Restaurant data has not been modified."), 500
    else:
        return _get_response("Restaurant data has been modified.", 200)


def delete_dish(dish_id):
    if dish_id is None:
        return error_message("400", "dish_id not specified"), 400
    RestaurantService.delete_dish(dish_id)
    return _get_response("OK", 200)


def delete_table(table_id):
    if table_id is None:
        return error_message("400", "table_id not specified"), 400
    RestaurantService.delete_table(table_id)
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
    flask_app.config["DB_SESSION"] = db_session


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    _init_flask_app(application)
    app.run(port=5003)
