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