import random
import time
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

location_x = 3.03
location_y = 4.5
point = Point(location_x, location_y)

polygon = Polygon( [[52, 111], [137,35], [170,119], [230,146], [277,175], [277,293], [157,240], [65,215], [45,225] , [11,178] ] )


def loop_location_change():
    while True:
        print(
            (
                generateAllInfoAndApply(
                    2.5, 31.2, 3.1, 41.5, 0, 5, location_x, location_y
                )
            )
        )


def changeLocation_rect(
    min_limit_x,
    max_limit_x,
    min_limit_y,
    max_limit_y,
    sleep_time,
    x_change,
    y_change,
    x_dir,
    y_dir,
    location_x,
    location_y,
):
    # sleep_time, x_change, y_change, x_dir, y_dir = generateAllInfo(min_time, max_time)
    time.sleep(sleep_time)
    x_in_border = checkByDirection(
        min_limit_x, max_limit_x, location_x, x_change, x_dir
    )
    y_in_border = checkByDirection(
        min_limit_y, max_limit_y, location_y, y_change, y_dir
    )
    if x_in_border and y_in_border:
        location_x = changeByDirection(location_x, x_change, x_dir)
        location_y = changeByDirection(location_y, y_change, y_dir)
        return ("location changed successfully", location_x, location_y)
    else:
        return "new location is out of borders, no changes were made"

def change_location_polygon(polygon,
    sleep_time,
    x_change,
    y_change,
    x_dir,
    y_dir,
    point):
    time.sleep(sleep_time)
    point = Point(location_x, location_y)
    inPolygon, new_point = checkInPolygon(polygon, point, x_change, y_change, x_dir, y_dir)
    if(inPolygon):
        point = new_point
        print(new_point)
    else: 
        print("point is out of bounds")



def generateAllInfoAndApply(
    min_limit_x,
    max_limit_x,
    min_limit_y,
    max_limit_y,
    min_time,
    max_time,
    location_x,
    location_y,
):
    MIN_BORDER = 0.0
    MAX_BORDER = 10.0
    sleep_time = generateNumber(min_time, max_time)
    x_change = generateNumber(MIN_BORDER, MAX_BORDER)
    y_change = generateNumber(MIN_BORDER, MAX_BORDER)
    x_dir = generateDirection()
    y_dir = generateDirection()
    return changeLocation_rect(
        min_limit_x,
        max_limit_x,
        min_limit_y,
        max_limit_y,
        sleep_time,
        x_change,
        y_change,
        x_dir,
        y_dir,
        location_x,
        location_y,
    )

def generateAllInfoAndApplyToPolygon(
    min_limit_x,
    max_limit_x,
    min_limit_y,
    max_limit_y,
    min_time,
    max_time,
    point
):
    MIN_BORDER = 0.0
    MAX_BORDER = 10.0
    sleep_time = generateNumber(min_time, max_time)
    x_change = generateNumber(MIN_BORDER, MAX_BORDER)
    y_change = generateNumber(MIN_BORDER, MAX_BORDER)
    x_dir = generateDirection()
    y_dir = generateDirection()
    return change_location_polygon(
        min_limit_x,
        max_limit_x,
        min_limit_y,
        max_limit_y,
        sleep_time,
        x_change,
        y_change,
        x_dir,
        y_dir,
        point
    )


def generateNumber(min_limit, max_limit):
    return random.uniform(min_limit, max_limit)


def generateDirection():
    return random.randint(0, 1)

def checkInPolygon(polygon, point, change_x, change_y, dir_x, dir_y):
    new_point = Point()
    if dir_x == 0: 
        new_point.x = point.x + change_x
    else: 
        new_point.x = point.x - change_x
    if dir_y == 0: 
        new_point.y = point.y + change_y
    else: 
        new_point.y = point.y - change_y
    
    return polygon.contains(new_point), new_point




def checkByDirection(min_limit, max_limit, base_location, location_change, dir):
    if dir == 0:
        return max_limit > (base_location + location_change)
    return min_limit < (base_location - location_change)


def changeByDirection(base_location, location_change, dir):
    if dir == 0:
        return base_location + location_change
    return base_location - location_change


#loop_location_change()
