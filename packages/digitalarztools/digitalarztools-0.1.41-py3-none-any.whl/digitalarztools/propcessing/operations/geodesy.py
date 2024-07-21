from math import floor

from pyproj import Proj, transform
from shapely import Point


class GeodesyOps:

    @staticmethod
    def utm_srid_from_extent( west, south, east, north):
        """
            Calculate the UTM zone for a given extent.
            :param west: min longitude bounding box in degrees
            :param south: min latitude bounding box in degrees
            :param east: max longitude bounding box in degrees
            :param north: max latitude bounding box in degrees
        """

        center_long = (west + east) / 2
        utm_zone = int(((center_long + 180) / 6) % 60) + 1
        # Determine if it's in the northern or southern hemisphere
        hemisphere = 'north' if (south + north) / 2 > 0 else 'south'
        # Determine the EPSG code for the UTM projection
        epsg_code = 32600 + utm_zone if hemisphere == 'north' else 32700 + utm_zone
        return epsg_code

    @staticmethod
    def utm_srid_from_coord(long, lat):
        zone = (floor((long + 180) / 6) % 60) + 1
        dir = 6 if lat >= 0 else 7
        return int(f"32{dir}{zone}")

    @staticmethod
    def meter_2_dd(length: float):
        return length / (110 * 1000)

    @classmethod
    def meters_to_dd_wgs_84(cls, point, distance_m):
        """
        Convert a buffer distance from meters to decimal degrees accurately.

        :param point: A shapely Point in geographic coordinates (decimal degrees).
        :param distance_m: Distance in meters.
        :return: A buffer in decimal degrees as a shapely Polygon.
        """
        # Define projections
        proj_latlon = Proj(proj='latlong', datum='WGS84')
        srid = cls.utm_srid_from_coord(point.x, point.y)
        proj_utm = Proj(f"epsg:{srid}")

        # Transform point to UTM
        x, y = transform(proj_latlon, proj_utm, point.x, point.y)

        # Create buffer in UTM coordinates
        buffer_utm = Point(x, y).buffer(distance_m)  # Buffer in meters

        # Transform buffer back to geographic coordinates
        buffer_latlon = transform(proj_utm, proj_latlon, buffer_utm.exterior.coords.xy[0],
                                  buffer_utm.exterior.coords.xy[1])
        buffer_latlon_polygon = Point(buffer_latlon[0], buffer_latlon[1]).buffer(0)  # Convert to shapely Polygon

        return buffer_latlon_polygon
