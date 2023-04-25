import requests, math
import PIL
from PIL import Image
from io import BytesIO


api_key = "AIzaSyDOUOjCUfAoWjm7pAsSDnwqXgXPZeaylQY"
hill_coords = (40.52200411620839, -74.46292879108148)

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

def square_search(center_lat, center_long, max_radius, visibility_radius):
    pattern = [(center_lat,center_long)]
    
    visibility_multiplier = 1
    max_range_in_terms_of_VR = max_radius/visibility_radius
    current_lat = center_lat
    current_long = center_long

    while(max_range_in_terms_of_VR > visibility_multiplier/2):
        current_lat, current_long = move_point(current_lat, current_long,0,visibility_multiplier * visibility_radius)
        pattern.append((current_lat,current_long))

        current_lat, current_long = move_point(current_lat, current_long, 270,visibility_multiplier * visibility_radius)
        pattern.append((current_lat,current_long))

        visibility_multiplier+=1

        current_lat, current_long = move_point(current_lat, current_long, 180,visibility_multiplier * visibility_radius)
        pattern.append((current_lat,current_long))

        current_lat, current_long = move_point(current_lat, current_long, 90,visibility_multiplier * visibility_radius)
        pattern.append((current_lat,current_long))

        visibility_multiplier+=1

    return pattern

import requests

def plot_path_on_google_maps(coords_list, api_key):
    # Define the base URL for the static maps API
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"

    # Define the path parameters
    path_params = "path=color:0x0000ff|weight:5"

    # Add the coordinates to the path parameters
    for lat, lon in coords_list:
        path_params += f"|{lat},{lon}"

    # Add the API key to the URL
    width, height = 640, 640
    url = f"{base_url}{path_params}&size={width}x{height}&key={api_key}"

    # Send a HTTP GET request to the Google Maps API
    response = requests.get(url)

    print(response.content)

    # Try opening the image from the response with PIL
    try:
        img = Image.open(BytesIO(response.content))
    except PIL.UnidentifiedImageError:
        print("Response content is not valid image data.")
        return

    # Save the image to a file
    img.save(filename)

plot_path_on_google_maps(square_search(hill_coords[0],hill_coords[1],10,1), api_key)