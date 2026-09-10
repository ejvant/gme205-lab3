from spatial import Point


# B.4 — Important Technical Rule: Shapely Distance Is Planar

p = Point("A", 121.0, 14.6, name="Gate", tag="POI")
q = Point("B", 121.1, 14.6)

# This is Cartesian distance in the coordinate units.
# For lon/lat values, do NOT label the result as meters.
coordinate_distance = p.geometry.distance(q.geometry)

print("Shapely planar distance:", coordinate_distance)

# Preserve the geodesic meaning from Laboratory 2:
meters = p.distance_to(q)

# Haversine implementation from Lab 2
print("Haversine distance (meters):", meters)

# B.5 — Demo

p = Point("A", 121.0, 14.6, name="Gate", tag="POI")

print(p.id)
print(p.lon, p.lat)
print(p.to_tuple())
print(p.geometry.geom_type)

# C.1 — Create Point from a dictionary

data = {
    "id": "C",
    "lon": 121.0,
    "lat": 14.6,
    "name": "Gate",
    "tag": "POI"
}

p_from_dict = Point.from_dict(data)

print(p_from_dict.id)
print(p_from_dict.lon, p_from_dict.lat)
print(p_from_dict.name)
print(p_from_dict.tag)

# C.2 — Convert Point to a dictionary

print("As dict:")
print(p.as_dict())

# D.3 — Test inherited bbox()

p = Point("A", 121.0, 14.6)
print(p.bbox())