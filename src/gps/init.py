import serial
import time
import pyGPs


class GPS:
    def __init__(self, serial_port) -> None:
        if serial_port:
            self.serial_port = serial_port
        else:
            self.serial_port = "/dev/ttyUSB0"
        self.bitrate = 9600
        pass

    def get_gps_data(self):
        # Open serial port
        ser = serial.Serial(self.serial_port, self.bitrate, timeout=5)

        # Create GPS object
        gps = pyGPs.GPS()

        # Read GPS data
        while True:
            data = ser.readline().decode("utf-8").strip()
            if data.startswith("$GPGGA"):
                # Parse GPS data
                gps.parse(data)

                # Get GPS coordinates
                lat = gps.latitude
                lon = gps.longitude
                alt = gps.altitude

                # Return GPS coordinates as a dictionary
                return {"latitude": lat, "longitude": lon, "altitude": alt}

            # Wait for a moment
            time.sleep(0.1)
