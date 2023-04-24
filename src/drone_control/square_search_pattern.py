import init
import Math

class Square_Search:
    def __init__(self, multiplier):
        print("constructed")
    
    # PARAMS:
    # max_radius (METERS) is the max radius of your search area
    # visibility_radius (METERS) is the max distance the camera can see. Dependent upon height and camera FOV
    def navigate(self, max_radius, visibility_radius):
        drone = Drone_Control(1)
        visibility_multiplier = 1
        
        drone.climb(10)
        max_range_in_terms_of_VR = max_radius/visibility_radius
        

        while(max_range_in_terms_of_VR > visibility_multiplier/2):
            drone.forwards(visibility_multiplier * visibility_radius)
            drone.turn_right(90)
            drone.forwards(visibility_multiplier * visibility_radius)
            drone.turn_right(90)
            visibility_multiplier++
            drone.forwards(visibility_multiplier * visibility_radius)
            drone.turn_right(90)
            drone.forwards(visibility_multiplier * visibility_radius)
            drone.turn_right(90)
            visibility_multiplier++

        # Drone must finish at bottom left corner always, so RTB.
        drone.turn_right(45)
        drone.forwards(Math.sqrt(2) * (visibility_multiplier/2) * visibility_radius)
        drone.turn_left(45)
        drone.descend()
