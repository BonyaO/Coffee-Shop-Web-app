import os
from urllib import response
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST, PATCH,DELETE, OPTIONS"
    )
    return response


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES


@app.route("/drinks")
def get_drinks():
    try:
        drinks = Drink.query.all()
        return jsonify({
            "success": True,
            "drinks": [drink.short() for drink in drinks]
        })
    except:
        abort(401)


@app.route("/drinks-detail")
@requires_auth(permission="get:drinks-detail")
def get_drinks_details(jwt):
    try:
        drinks = Drink.query.all()
        return jsonify({
            "success": True,
            "drinks": [drink.long() for drink in drinks]
        })
    except:
        abort(403)


@app.route("/drinks", methods=["POST"])
@requires_auth(permission="post:drinks")
def post_drink(jwt):
    request_body = request.get_json()

    if request_body is None:
        abort(422)
    title = request_body.get("title", None)
    recipe = request_body.get("recipe", None)

    try:
        new_drink = Drink(title=title, recipe=json.dumps(recipe))
        print(type(new_drink))
        new_drink.insert()

        return jsonify({
            "success": True,
            "drinks": [new_drink.long()]
        })

    except:
        abort(500)


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth(permission="patch:drinks")
def update_drink(jwt, id):
    request_body = request.get_json()

    try:
        drink = Drink.query.get(id)
        if request_body.get("title") is not None:
            drink.title = request_body.get("title")
        if request_body.get("recipe") is not None:
            drink.recipe = request_body.get("recipe")

        drink.update()
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    except:
        abort(422)


@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth(permission="delete:drinks")
def delete_drink(jwt, id):
    try:
        drink = Drink.query.get(id)
        print(drink)
        drink.delete()
        return jsonify({
            "success": True,
            "deleted": id
        })
    except:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.errorhandler(405)
def handle_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "The method is not allowed for the requested URL."
    }), 405


@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404


@app.errorhandler(403)
def handle_not_found(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Permission Not Found"
    }), 403


@app.errorhandler(500)
def handle_not_found(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server Error"
    }), 500
