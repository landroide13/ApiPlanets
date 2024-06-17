class Planet:
    def __init__(self, planet_name, planet_type, home_start, mass, radius, distance ,_id=None):
        self.planet_id = _id
        self.planet_name = planet_name
        self.planet_type = planet_type
        self.home_start = home_start
        self.mass = mass
        self.radius = radius
        self.distance = distance

    def to_json(self):
        return {
            "_id": self.id,
            "planet_name": self.title,
            "planet_type": self.description,
            "home_start": self.home_start,
            "mass": self.mass,
            "radius": self.radius,
            "distance": self.distance
        }