from config.db import get_database
from bson import ObjectId

class PlanetRepository:
    def __init__(self):
        self.db = get_database()
        self.planets = self.db.planets  # 'planets' is the collection name

    def find_all(self):
        planets = list(self.planets.find({}))
        return [self.convert_to_json(planet) for planet in planets]

    def find_by_id(self, id):
        planet = self.planets.find_one({"_id": ObjectId(id)})
        return self.convert_to_json(planet) if planet else None

    def create(self, planet):
        return self.planets.insert_one(planet).inserted_id

    def update(self, id, planet):
        self.planets.update_one({"_id": ObjectId(id)}, {"$set": planet})

    def delete(self, id):
        return self.planets.delete_one({"_id": ObjectId(id)}).deleted_count
    
    def convert_to_json(self, planet):
        if planet and '_id' in planet:
            planet['_id'] = str(planet['_id'])
        return planet






















