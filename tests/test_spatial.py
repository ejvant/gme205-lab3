import sys
from pathlib import Path

import pytest
from shapely.geometry import Polygon

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from spatial import Point, Parcel


# 1. Valid Point can be constructed
def test_valid_point_can_be_constructed():
    point = Point("A", 121.0, 14.6)
    assert point.id == "A"
    assert point.lon == 121.0
    assert point.lat == 14.6


# 2. Invalid longitude raises ValueError
def test_invalid_longitude_raises_value_error():
    with pytest.raises(ValueError):
        Point("A", 999, 14.6)


# 3. from_dict(valid_record) creates Point
def test_from_dict_valid_record_creates_point():
    record = {
        "id": "C",
        "lon": 121.2,
        "lat": 14.7,
        "name": "Gate 2",
        "tag": "POI"
    }
    point = Point.from_dict(record)
    assert isinstance(point, Point)


# 4. from_dict(invalid_record) fails through constructor validation
def test_from_dict_invalid_record_fails_through_constructor_validation():
    record = {
        "id": "D",
        "lon": 999,
        "lat": 14.7
    }
    with pytest.raises(ValueError):
        Point.from_dict(record)


# 5. Point bbox is correct
def test_point_bbox_is_correct():
    point = Point("A", 121.0, 14.6)
    assert point.bbox() == (121.0, 14.6, 121.0, 14.6)


# 6. Parcel bbox is correct
def test_parcel_bbox_is_correct():
    geometry = Polygon([
        (0, 0),
        (10, 0),
        (10, 5),
        (0, 5)
    ])

    parcel = Parcel(
        101,
        geometry,
        {
            "area": 50.0,
            "zone": "Residential",
            "is_active": True
        }
    )

    assert parcel.bbox() == (0.0, 0.0, 10.0, 5.0)


# 7. inside.intersects(parcel) is True
def test_inside_intersects_parcel():
    parcel = Parcel(
        101,
        Polygon([
            (0, 0),
            (10, 0),
            (10, 5),
            (0, 5)
        ]),
        {}
    )

    inside = Point("IN", 2, 2)

    assert inside.intersects(parcel) is True


# 8. outside.intersects(parcel) is False
def test_outside_does_not_intersect_parcel():
    parcel = Parcel(
        101,
        Polygon([
            (0, 0),
            (10, 0),
            (10, 5),
            (0, 5)
        ]),
        {}
    )

    outside = Point("OUT", 12, 2)

    assert outside.intersects(parcel) is False


# 9. as_dict() contains no live Shapely objects
def test_as_dict_contains_no_live_shapely_objects():
    point = Point("A", 121.0, 14.6, name="Gate", tag="POI")

    result = point.as_dict()

    assert result["geometry"] == [121.0, 14.6]
    assert result["bbox"] == [121.0, 14.6, 121.0, 14.6]

    for value in result.values():
        assert not hasattr(value, "geom_type")
