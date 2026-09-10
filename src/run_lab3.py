import csv
import json

import matplotlib.pyplot as plt

from spatial import Point, Parcel
from shapely.geometry import Polygon


def main():

    # Load points from CSV
    points = []

    with open("data/points.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            points.append(Point.from_dict(row))

    # Use the first point from the CSV as the report point
    point = points[0]

    # Construct a synthetic parcel
    attributes = {
        "area": 50.0,
        "zone": "Residential",
        "is_active": True
    }

    geom = Polygon([
        (0, 0),
        (10, 0),
        (10, 5),
        (0, 5)
    ])

    parcel = Parcel(101, geom, attributes)

    # Construct points for spatial relationship
    inside = Point("IN", 2, 2)
    outside = Point("OUT", 12, 2)

    # Evaluate spatial relationships
    inside_intersects = inside.intersects(parcel)
    outside_intersects = outside.intersects(parcel)

    # Build report dictionary
    report = {
        "point": point.as_dict(),
        "parcel": parcel.as_dict(),
        "relationships": {
            "inside_intersects_parcel": inside_intersects,
            "outside_intersects_parcel": outside_intersects
        }
    }

    # Write JSON report
    with open("output/lab3_report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    # Create preview figure
    x, y = geom.exterior.xy

    plt.figure()

    plt.plot(x, y)

    plt.plot(inside.lon, inside.lat, "o")
    plt.text(inside.lon, inside.lat, "IN")

    plt.plot(outside.lon, outside.lat, "o")
    plt.text(outside.lon, outside.lat, "OUT")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Lab 3 Spatial Object Preview")

    plt.savefig("output/lab3_preview.png")

    plt.close()


if __name__ == "__main__":
    main()