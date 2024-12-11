import sys 
import math
import numpy as np

# angles in degrees
# heights/distance in meters
def calculate_distance_straight_line(target_height, launcher_angle=60, rover_angle=0, launcher_height=1/3):

    effective_angle = launcher_angle + rover_angle
    tan_angle = math.tan(math.radians(effective_angle))

    if (math.radians(effective_angle) == 0 or math.radians(effective_angle) == math.pi/2):
        print("Error: Division by zero")
        return -1

    distance = (target_height - launcher_height) / tan_angle

    return distance

def calculate_distance_curve(target_height, speed_const, drag_const, launcher_height=1/3, launcher_angle=60, rover_angle=0):

    effective_angle = launcher_angle + rover_angle
    effective_angle_rad = math.radians(effective_angle)
    sin_angle = math.sinh(effective_angle_rad)
    cos_angle = math.cosh(effective_angle_rad)

    # calculate the distance
    distance = (drag_const * cos_angle) * (math.asinh((target_height - launcher_height + (drag_const * sin_angle))/(speed_const)))

    return distance

def new_waypoint(x, y, target_height):

    r = math.sqrt(x**2 + y**2)
    offset = calculate_distance_straight_line(target_height)
    new_x = x * (r - offset) / r
    new_y = y * (r - offset) / r

    return new_x, new_y



def main ():

    print("Test calculate_distance.py")
    test_calculate_distance_straight_line()
    test_calculate_distance_curve()

def test_calculate_distance_straight_line():
    # Test case 1
    result = calculate_distance_straight_line(1, 10, 45, 0)
    print(f"Test case 1 - Expected: {9.0}, Got: {result}")

    # Test case 2
    result = calculate_distance_straight_line(2, 8, 30, 15)
    print(f"Test case 2 - Expected: {6.0}, Got: {result}")

    # Test case 3
    result = calculate_distance_straight_line(0, 5, 60, 30)
    print(f"Test case 3 - Expected: {5.0}, Got: {result}")

def test_calculate_distance_curve():
    # Test case 1
    result = calculate_distance_curve(1, 10, 45, 0, 5, 2)
    print(f"Test case 1 - Expected: TBD, Got: {result}")

    # Test case 2
    result = calculate_distance_curve(2, 8, 30, 15, 4, 1.5)
    print(f"Test case 2 - Expected: TBD, Got: {result}")

    # Test case 3
    result = calculate_distance_curve(0, 5, 60, 30, 3, 1)
    print(f"Test case 3 - Expected: TBD, Got: {result}")

if __name__ == "__main__":
    main()