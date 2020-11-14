import connexion, logging, database
from flask import jsonify, request
from services.restaurant_service import RestaurantService
import json

db_session = None


def serialize(obj):
    return dict([(k, v) for k, v in obj.__dict__.items() if k[0] != "_"])


def list_obj_json(name_list, list_objs):
    objects = []
    for obj in list_objs:
        objects.append(serialize(obj))
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
        #get menu photos for each menu
        for menu in menus:
            photos = RestaurantService.get_menu_photos(db_session, menu.id)
            json_menu = serialize(menu)
            photos_list=[]
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


def create_restaurant():
    
    json = request.get_json()
    email = json["email"]
    phone = json["phone"]
    user = UserService.user_is_present(db_session, email, phone)
    if user is not None:
        return _get_response(
            "User with email {} and/or phone already exist".format(email, phone),
            500,
        )
    user = UserService.create_user(db_session, json)
    if user is not None:
        return _get_response("OK", 200)
    else:
        return _get_response(
            "User not created because we have an error on server", 500
        )
    
    
    pass


def create_table():
    pass


def create_dish():
    pass


def create_photo():
    pass


def create_review():
    pass


logging.basicConfig(level=logging.INFO)
db_session = database.init_db("sqlite:///restaurant.db")
app = connexion.App(__name__)
app.add_api("swagger.yml")
application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(port=5003)
