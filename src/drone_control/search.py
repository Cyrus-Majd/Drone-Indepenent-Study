import requests, math
import PIL
from PIL import Image
from io import BytesIO
import webbrowser
import urllib.parse
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


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

def plot_path_on_dynamic_map(coords_list, api_key):
    # Define the base URL for the dynamic maps API
    base_url = "https://www.google.com/maps/embed/v1/directions?"

    # Define the path parameters
    path_params = "origin=" + str(coords_list[0][0]) + "," + str(coords_list[0][1])
    path_params += "&destination=" + str(coords_list[-1][0]) + "," + str(coords_list[-1][1])
    path_params += "&waypoints="
    for lat, lon in coords_list[1:-1]:
        path_params += "via:" + urllib.parse.quote(str(lat) + "," + str(lon)) + "|"

    # Add the API key to the URL
    url = f"{base_url}{path_params}&key={api_key}"

    # Open the URL in a web browser
    print(path_params)
    webbrowser.open_new_tab(url)

def plot_path_on_basemap(coords_list):
    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='merc', resolution='h', lat_0=0, lon_0=0, llcrnrlon=-180, urcrnrlon=180, llcrnrlat=-80, urcrnrlat=80)
    m.drawcoastlines()
    m.drawmapboundary(fill_color='lightblue')
    m.fillcontinents(color='white',lake_color='lightblue')
    lats = [coord[0] for coord in coords_list]
    lons = [coord[1] for coord in coords_list]
    x, y = m(lons, lats)
    m.plot(x, y, marker=None, color='blue', linewidth=2)
    plt.show()

def plot_path_on_map(coords):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Create Basemap object with the desired projection and limits
    m = Basemap(projection='merc', llcrnrlon=min([c[1] for c in coords])-0.1,
                llcrnrlat=min([c[0] for c in coords])-0.1,
                urcrnrlon=max([c[1] for c in coords])+0.1,
                urcrnrlat=max([c[0] for c in coords])+0.1)

    # Draw coastlines and countries
    m.drawcoastlines()
    m.drawcountries()

    # Draw the path
    for i in range(len(coords) - 1):
        lat1, lon1 = coords[i]
        lat2, lon2 = coords[i + 1]
        x, y = m(lon1, lat1)
        m.plot(x, y, 'bo', markersize=5)
        m.drawgreatcircle(lon1, lat1, lon2, lat2, linewidth=1, color='b')

    # Save the figure
    fig.savefig('path.png', bbox_inches='tight')

    # Display the figure
    plt.show()

def plot_path_on_dynamic_map_meme(coords_list, api_key):
    # Define the base URL for the dynamic maps API
    base_url = "https://www.google.com/maps/embed/v1/directions?"

    # Define the path parameters
    path_params = "origin=" + str(coords_list[0][0]) + "," + str(coords_list[0][1])
    path_params += "&destination=" + str(coords_list[-1][0]) + "," + str(coords_list[-1][1])
    path_params += "&waypoints="
    for lat, lon in coords_list[1:-1]:
        path_params += str(lat) + "," + str(lon) + "|"

    # Define the marker parameters
    marker_params = ""
    for i, (lat, lon) in enumerate(coords_list):
        if i == 0:
            label = "A"
        elif i == len(coords_list) - 1:
            label = "B"
        else:
            label = str(i)
        marker_params += "&markers=color:red%7Clabel:" + label + "%7C" + str(lat) + "," + str(lon)

    # Add the API key and parameters to the URL
    url = f"{base_url}{path_params}{marker_params}&key={api_key}"

    # Open the URL in a web browser
    webbrowser.open_new_tab(url)




plot_path_on_dynamic_map_meme(square_search(hill_coords[0],hill_coords[1],10,1), api_key)
# plot_path_on_map(square_search(hill_coords[0],hill_coords[1],10,1))