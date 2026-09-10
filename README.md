# GmE 205: Laboratory Exercise 3
**Spatial Object Systems in Python**
## Overview
*This laboratory exercise builds on the spatial object design developed in Laboratory 2. It focuses on refactoring the existing implementation using Shapely, introducing a `SpatialObject` base class for shared spatial behavior, and implementing structured data input and output through `from_dict()` and `as_dict()`. The exercise also introduces a `Parcel` object, focused tests, and a runner that produces structured and visual outputs. It emphasizes maintaining clear responsibilities while correctly interpreting coordinate systems and units.*

## How to set up the virtual environment
The steps to set up a virtual environment:
1. Open Visual Studio Code.
2. Under the VS Code Terminal tab, select "New Terminal".
3. In the Terminal, run:

   `py -m venv .venv`

   `.\.venv\Scripts\activate`

4. When successful, your terminal prompt should show `(.venv)`.

## Refactor Point to Use Shapely

The `Point` class was updated to store its geometry as a Shapely `Point` object while preserving coordinate validation and access to `lon` and `lat`. The existing Haversine distance calculation was also retained to preserve the behavior established in the previous exercise.

## Explain the Distance Decision (Challenge 4)

The choice of distance method depends on how the coordinates are represented and interpreted. Shapely’s `geometry.distance()` is not used to calculate geographic distance as an alternative to the Haversine method because longitude and latitude describe geographic positions on the Earth surface and are not simple planar x and y measurements. Shapely’s distance operation calculates distance using planar geometry and does not automatically consider the Earth’s curvature. Applying this directly to longitude/latitude would not give a reliable distance in meters or kilometers. Therefore, the Haversine formula is used to calculate geographic distance because it accounts the Earth’s curvature. In this exercise, Shapely is used to represent and manage the point geometry, while the model is responsible for interpreting the coordinates as longitude and latitude, and determining the meaning, rules, and behavior of the spatial data.

## Reflection

1. *Refactoring:* The `Point` class was refactored to store its spatial geometry as a Shapely `Point` object. This consequently changed how the data is stored internally, but the way the object is used stayed the same. This allows the object to use Shapely for spatial operations while keeping the code organized. The way the `Point` object is used remains the same. Users can still access `lon` and `lat`, use `to_tuple()`, and calculate Haversine distance as in the previous exercise. In this way, the internal code was improved without changing how the `Point` object works.

2. *Responsibility:* The responsibilities are divided so that each component handles the part it is designed for. Shapely manages geometry representation and geometric operations, `SpatialObject` provides common spatial functions that can be shared by different object types, such as `bbox()` and `intersects()`. On the other hand, both `Point` and `Parcel` handle theor own specific data and behavior. Specifically, `Point` is responsible for coordinate validation, coordinate access, and Haversine Distance, whereas `Parcel` is responsible for its parcel ID and structured attributes.

3. *Data Boundary:* `from_dict()` should be responsible for reading and converting of external data into the format needed to create a `Point`. The constructor is responsible for checking whether those values are valid. This keeps the validation rules in one place, avoids duplicating the same checks, and ensures that every `Point` is created using the same validation process. To make it simple: `from_dict()` prepares the data, while `__init__()` validates it.

4. *Output Boundary:* `as_dict()` should convert the object’s information into simple and JSON-ready values that can be easily understood and processed outside the class. This allows the output to be easily converted to JSON, stored, or shared to other systems. It also keeps the internal Shapely representation separate from the data being exported. Shapely geometry stays inside the object for spatial operations, while `as_dict()` converts information into simple values for output and storage.

5. *Inheritance:* Since both `Point` and `Parcel` have geometries, they can perform the same intersection operation. Placing `intersects()` in `SpatialObject` provides one shared implementation that both classes can inherit. By defining it once in the parent class, both objects can inherit the same behavior without repeating the code. This keeps the individual classes focused on their own specific responsibilities. Defining it once allows both classes to inherit and use the same method, while keeping the spatial behavior in one place.

6. *Coordinate Meaning:* `geometry.distance()` does not directly gives a distance in meters when working with longitude and latitude because these coordinates describe locations using angles on the Earth’s surface (which can be referred to as angular coordinates). Shapely treats the values as coordinates on a flat plane, so the result does not account for the Earth’s curved surface and is based on the coordinate units rather than its actual distance. For this specific reason, the Haversine method from the previous exercise is kept for obtaining the actual geographic distance in meters.

7. *Scale:* The use of `SpatialObject` makes the system easier to maintain because shared spatial functions are defined only once and can be reused by different object types. It also makes the system easier to maintain because common methods such as `bbox()` and `intersects()` only need to manage in one place. However, the same object-based approach may become slower and use more memory when dealing with millions of spatial objects. Techniques such as spatial indexing and efficient data storage would be needed to make spatial queries and processing faster.

## Why does each responsibility live where it does?

Each part of the design handles a specific purpose. Shapely is used for storing geometry and performing geometric operations, while `SpatialObject` provides spatial functions shared by different objects. `Point` handles point-specific rules, including coordinate validation and Haversine distance, while `Parcel` manages parcel-specific information and attributes. The data conversion methods also have distinct roles: `from_dict()` prepares and handles incoming data, while `as_dict()` creates structured output. Separating these responsibilities keeps the classes organized, reduces duplicated logic, and makes the system easier to modify, expand, or maintain. 

The main principle is to keep each responsibility in the component that is most appropriate for it, rather than putting all the logic in one class.

## Author
Enoch Joshua V. Antonio  
MS Geomatics Engineering

## References
- Shapely User Manual: https://shapely.readthedocs.io/en/stable/manual.html
- Shapely API — Geometry Predicates: https://shapely.readthedocs.io/en/stable/reference/shapely.intersects.html
- Python Tutorial — Errors and Exceptions: https://docs.python.org/3/tutorial/errors.html

Edited on GitHub web interface and VS Code