from flask import Blueprint, request, jsonify
from repository.planets_repository import PlanetRepository
from bson import ObjectId

planet_bp = Blueprint('planet_bp', __name__)
repo = PlanetRepository()

@planet_bp.route('/planets', methods=['GET'])
def get_planets():
    todos = repo.find_all()
    return jsonify([todo for todo in todos])

@planet_bp.route('/planet/<id>', methods=['GET'])
def get_planet(id):
    todo = repo.find_by_id(ObjectId(id))
    return jsonify(todo)

@planet_bp.route('/planet', methods=['POST'])
def add_planet():
    data = request.json
    todo_id = repo.create(data)
    return jsonify({"_id": str(todo_id)}), 201

@planet_bp.route('/planet/<id>', methods=['PUT'])
def update_planet(id):
    repo.update(ObjectId(id), request.json)
    return jsonify({"message": "Todo updated"}), 200

@planet_bp.route('/planet/<id>', methods=['DELETE'])
def delete_planet(id):
    deleted_count = repo.delete(ObjectId(id))
    if deleted_count:
        return jsonify({"message": "Planet deleted"}), 200
    return jsonify({"message": "Planet not found"}), 404