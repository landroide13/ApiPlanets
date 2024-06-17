from config.db import get_database

class PlanetRepository:
    def __init__(self):
        self.db = get_database()
        self.planets = self.db.planets  # 'planets' is the collection name

    def find_all(self):
        return list(self.planets.find({}))

    def find_by_id(self, id):
        return self.planets.find_one({"_id": id})

    def create(self, todo):
        return self.planets.insert_one(todo).inserted_id

    def update(self, id, todo):
        self.planets.update_one({"_id": id}, {"$set": todo})

    def delete(self, id):
        return self.planets.delete_one({"_id": id}).deleted_count






















