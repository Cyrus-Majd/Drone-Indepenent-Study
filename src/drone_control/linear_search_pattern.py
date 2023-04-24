import init

class Linear_Search:
    def __init__(self, multiplier):
        print("constructed")
    
    # PARAMS:
    # x_distance (METERS) is the width of your search area
    # y_distance (METERS) is the depth of your search area
    # visibility_radius (METERS) is the max distance the camera can see. Dependent upon height and camera FOV
    def navigate(self, x_distance, y_distance, visibility_radius):
        drone = Drone_Control(1)
        drone.climb(10)

        while(y_distance > 0):
            drone.forwards(x_distance)
            drone.turn_right(90)
            drone.forwards(visiblity_radius)
            drone.turn_right(90)
            drone.forwards(x_distance)
            drone.turn_left(90)
            drone.forwards(visibility_radius)
            drone.turn_left(90)
            y_distance = y_distance - (2 * visibility_radius)

        # drone ends up on bottom right always
        drone.turn_left(90)
        drone.move_forwards(y_distance)
        drone.turn_right(90)
        drone.descend()
