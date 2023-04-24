import cv2
import numpy as np
import requests

url = 'http://10.72.102.58:5000/down_feed'

# Open a connection to the video stream
response = requests.get(url, stream=True)
if response.status_code != 200:
    print(f"Request failed with status code {response.status_code}")
    exit(1)

# Read frames from the stream and process them
bytes_ = b''
for chunk in response.iter_content(chunk_size=1024):
    bytes_ += chunk
    a = bytes_.find(b'\xff\xd8')
    b = bytes_.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes_[a:b+2]
        bytes_ = bytes_[b+2:]
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Process the frame
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([90,50,50])
        upper_blue = np.array([150,255,255])
        # lower_blue = np.array([90,50,50])
        # upper_blue = np.array([150,255,255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # res = cv2.bitwise_and(img,img, mask= mask)

        # Find contours of blue objects
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on frame
        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

        cv2.imshow('preview', img)

        # Exit on ESC
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

# Cleanup
cv2.destroyAllWindows()
response.close()
