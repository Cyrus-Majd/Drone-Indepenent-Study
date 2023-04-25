import init

class Linear_Search:
    def __init__(self, multiplier):
        print("constructed")

    def move_point(lat, lon, bearing, distance):
        # Earth's radius in meters
        R = 6378137

        # Convert lat/lon to radians
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        bearing_rad = math.radians(bearing)

        # Calculate new latitude and longitude
        new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(distance/R) + math.cos(lat_rad) * math.sin(distance/R) * math.cos(bearing_rad))
        new_lon_rad = lon_rad + math.atan2(math.sin(bearing_rad) * math.sin(distance/R) * math.cos(lat_rad), math.cos(distance/R) - math.sin(lat_rad) * math.sin(new_lat_rad))

        # Convert new lat/lon back to degrees
        new_lat = math.degrees(new_lat_rad)
        new_lon = math.degrees(new_lon_rad)

        return new_lat, new_lon
    
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
