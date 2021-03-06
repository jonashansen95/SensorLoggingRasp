import os
from gps import *
import time
import threading
import requests

gpsd = None  # seting the global variable

os.system('clear')  # clear the terminal (optional)


class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd  # bring it in scope
        gpsd = gps(mode=WATCH_ENABLE)  # starting the stream of info
        self.current_value = None
        self.running = True  # setting the thread running to true

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()  # this will continue to loop and grab EACH set of gpsd info to clear the buffer


if __name__ == '__main__':
    gpsp = GpsPoller()  # create the thread
    try:
        gpsp.start()  # start it up
        while True:
            url = "https://api.joerha.dk/gps"
            headers = {"X-API-Key": "d2c9c21f077d65cfe53388a976764472"}

            payload = {"time": gpsd.utc, "longitude": gpsd.fix.longitude, "latitude": gpsd.fix.latitude,
                       "altitude": gpsd.fix.altitude, "speed": gpsd.fix.speed, "heading": gpsd.fix.track,
                       "longitudeErr": gpsd.fix.eps, "latitudeErr": gpsd.fix.ept, "altitudeErr": gpsd.fix.epv,
                       "timeOffset": gpsd.fix.time}
            r = requests.post(url, headers=headers, data=payload)
            print(r.status_code)

            time.sleep(0.5)  # set to whatever

    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print"\nKilling Thread..."
        gpsp.running = False
        gpsp.join()  # wait for the thread to finish what it's doing
    print"Done.\nExiting."
