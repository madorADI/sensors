import unittest
import borderCheckPolygon
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

polygon = Polygon( [[52, 111], [137,35], [170,119], [230,146], [277,175], [277,293], [157,240], [65,215], [45,225] , [11,178] ] )

class TestBorderCheck(unittest.TestCase):
    def test_location_in_border(self):
        result = borderCheckPolygon.change_location_polygon(polygon, 0.1, 5, 5, 0, 0, Point(100, 100)  )
        self.assertEqual(
            result, (105.0, 105.0), "ASSERT IS WRONG"
        )

    def test_location_out_of_border_both_x_y(self):
        result = borderCheckPolygon.change_location_polygon(polygon, 0.1, 5, 5, 0, 0, Point(500, 500)  )
        self.assertEqual(
            result, "point is out of bounds", "ASSERT IS WRONG"
        )

    def test_location_out_of_border_y(self):
        result = borderCheckPolygon.change_location_polygon(polygon, 0.1, 5, 5, 0, 0, Point(100, 500)  )
        self.assertEqual(
            result, "point is out of bounds", "ASSERT IS WRONG"
        )

    def test_location_out_of_border_x(self):
        result = borderCheckPolygon.change_location_polygon(polygon, 0.1, 5, 5, 0, 0, Point(500, 100)  )
        self.assertEqual(
            result, "point is out of bounds", "ASSERT IS WRONG"
        )
    
unittest.main(argv=[""], exit=False)

