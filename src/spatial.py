import math

from shapely.geometry import Point as ShapelyPoint

class SpatialObject:
    """Base abstraction for domain objects that have geometry."""

    def __init__(self, geometry):
        self.geometry = geometry

    def bbox(self):
        return self.geometry.bounds

    def intersects(self, other):
        return self.geometry.intersects(other.geometry)

class Point(SpatialObject):
    def __init__(self, id, lon, lat, name=None, tag=None):
        # Coordinate validation
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        self.id = id
        geometry = ShapelyPoint(lon, lat)
        super().__init__(geometry)
        self.name = name
        self.tag = tag

    # Preserve lon/lat access through properties
    @property
    def lon(self):
        return self.geometry.x

    @property
    def lat(self):
        return self.geometry.y

    def to_tuple(self):
        return (self.lon, self.lat)

    # Preserve Lab 2 Haversine distance
    def distance_to(self, other):
        return Point.haversine_m(
            self.lon,
            self.lat,
            other.lon,
            other.lat
        )

    @staticmethod
    def haversine_m(
        lon1: float,
        lat1: float,
        lon2: float,
        lat2: float
    ) -> float:
        R = 6_371_000.0

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)

        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = (
            math.sin(dphi / 2) ** 2
            + math.cos(phi1)
            * math.cos(phi2)
            * math.sin(dlambda / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return R * c

    @classmethod
    def from_dict(cls, d: dict):
        # Read/convert the external representation here.
        # Then call cls(...) so __init__ remains the validation boundary.
        return cls(
            id=d["id"],
            lon=float(d["lon"]),
            lat=float(d["lat"]),
            name=d.get("name"),
            tag=d.get("tag")
        )

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "tag": self.tag,
            "geometry": [self.lon, self.lat],
            "bbox": list(self.geometry.bounds)
        }

class Parcel(SpatialObject):
    def __init__(self, parcel_id, geometry, attributes: dict):
        super().__init__(geometry)
        self.parcel_id = parcel_id
        self.attributes = attributes

    def as_dict(self):
        return {
            "parcel_id": self.parcel_id,
            "bbox": list(self.geometry.bounds),
            "attributes": self.attributes,
        }