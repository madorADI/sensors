import random
import time
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

location_x = 100
location_y = 100
point = Point(location_x, location_y)
polygon = Polygon( [[52, 111], [137,35], [170,119], [230,146], [277,175], [277,293], [157,240], [65,215], [45,225] , [11,178] ] )

def change_location_polygon(polygon,
    sleep_time,
    x_change,
    y_change,
    x_dir,
    y_dir, curr_point):
    global point
    time.sleep(sleep_time)
    inPolygon, new_point = checkInPolygon(polygon, curr_point, x_change, y_change, x_dir, y_dir)
    if(inPolygon):
        print(point, "old")
        point = Point(new_point.x, new_point.y)
        return  point.x, point.y
    return point.x, point.y
    # return "point is out of bounds"


def generateAllInfoAndApplyToPolygon(
    polygon,
    min_time,
    max_time,
    curr_point,
):
    MIN_BORDER = 0.0
    MAX_BORDER = 10.0
    sleep_time = generateNumber(min_time, max_time)
    x_change = generateNumber(MIN_BORDER, MAX_BORDER)
    y_change = generateNumber(MIN_BORDER, MAX_BORDER)
    x_dir = generateDirection()
    y_dir = generateDirection()
    return change_location_polygon(
        polygon,
        sleep_time,
        x_change,
        y_change,
        x_dir,
        y_dir,
        curr_point
    )

def generateNumber(min_limit, max_limit):
    return random.uniform(min_limit, max_limit)

def generateDirection():
    return random.randint(0, 1)

def checkInPolygon(polygon, curr_point, change_x, change_y, dir_x, dir_y):
    if dir_x == 0: 
        new_x = curr_point.x + change_x
    else: 
        new_x = curr_point.x - change_x
    if dir_y == 0: 
        new_y = curr_point.y + change_y
    else: 
        new_y = curr_point.y - change_y
    new_point = Point(new_x, new_y)
    
    return polygon.contains(new_point), new_point

def loop_location_change():
    global point
    while True:
            (
                print(generateAllInfoAndApplyToPolygon(polygon, 0, 1, point))
            )
