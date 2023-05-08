#!/usr/bin/python3
""" a new view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all():
    """retrieve all"""
    list_all = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(list_all)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_method_state(state_id):
    """retrieve state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_method(state_id):
    """Delete state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_obj():
    """create new state instance"""
    if not request.get_json():
        return make_request(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    data_js = request.get_json()
    state_obj = State(**data_js)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def post_method(state_id):
    """Post"""
    if not request.get_json():
        return make_reponse(jsonify({"error": "Not a JSON"}), 400)
    obj_data = storage.get(State, state_id)
    if obj_data is None:
        abort(400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj_data, key, value)
    storage.save()
    return jsonify(obj_data.to_dict())
