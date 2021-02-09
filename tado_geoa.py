#
# tado_geoa.py (Geofencing Assist for Tado)
# Created by Adrian Slabu <adrianslabu@icloud.com> on 08.02.2021
# 

import sys
import time

from PyTado.interface import Tado

def main():

    login()
    homeStatus()
    
def login():

    global t

    try:
        t = Tado('your_username@mail.com', 'your_password') # tado account and password

    except Exception as e:
        print (e)
        if (str(e).find("ConnectionError") != -1):
            print ("Connection Error, retrying in 30 sec..")
            time.sleep(30) # retrying interval (in seconds), in case of connection error
            login()
        else:
            print ("Login error.")
            sys.exit(0)

def homeStatus():

    global devicesHome

    try:

        homeState = t.getHomeState()["presence"]
        devicesHome = []

        for mobileDevice in t.getMobileDevices():
            if (mobileDevice["location"]["relativeDistanceFromHomeFence"] == 0.0):
                devicesHome.append(mobileDevice["name"]) 

        if (len(devicesHome) > 0 and homeState == "HOME"):
            if (len(devicesHome) == 1):
                print ("Your home is in HOME Mode, the device " + devicesHome[0] + " is at home.")
            else:
                devices = ""
                for i in range(len(devicesHome)):
                    if (i != len(devicesHome) - 1):
                        devices += devicesHome[i] + ", "
                    else:
                        devices += devicesHome[i]
                print ("Your home is in HOME Mode, the devices " + devices + " are at home.")
        elif (len(devicesHome) == 0 and homeState == "AWAY"):
            print ("Your home is in AWAY Mode and are no devices at home.")
        elif (len(devicesHome) == 0 and homeState == "HOME"):
            print ("Your home is in HOME Mode but are no devices at home.")
            print ("Activating AWAY mode.")
            t.setAway()
            print ("Done!")
        elif (len(devicesHome) > 0 and homeState == "AWAY"):
            if (len(devicesHome) == 1):
                print ("Your home is in AWAY Mode but the device " + devicesHome[0] + " is at home.")
            else:
                devices = ""
                for i in range(len(devicesHome) - 1):
                    if (i != len(devicesHome) - 1):
                        devices += devicesHome[i] + ", "
                    else:
                        devices += devicesHome[i]
                print ("Your home is in AWAY Mode but the devices " + devices + " are at home.")

            print ("Activating HOME mode.")
            t.setHome()
            print ("Done!")

        devicesHome.clear()
        print ("Waiting for a change in devices location..")
        checkDevicesLocation()

    except KeyboardInterrupt:
        print ("Interrupted by user.")
        sys.exit(0)

    except Exception as e:
        print(e)
        if (str(e).find("ConnectionError") != -1):
            print ("Connection Error, retrying in 30 sec..")
    
            time.sleep(30) # retrying interval (in seconds), in case of connection error
            homeStatus()

def checkDevicesLocation():

    try:

        homeState = t.getHomeState()["presence"]

        for mobileDevice in t.getMobileDevices():
            if (mobileDevice["location"]["relativeDistanceFromHomeFence"] == 0.0):
                devicesHome.append(mobileDevice["name"]) 

        if (len(devicesHome) > 0 and homeState == "AWAY"):
            if (len(devicesHome) == 1):
                print (devicesHome[0] + " is at home, activating HOME mode.")
            else:
                devices = ""
                for i in range(len(devicesHome)):
                    if (i != len(devicesHome) - 1):
                        devices += devicesHome[i] + ", "
                    else:
                        devices += devicesHome[i]
                print (devices + " are at home, activating HOME mode.")
            t.setHome()
            print ("Done!")
            print ("Waiting for a change in devices location..")

        elif (len(devicesHome) == 0 and homeState == "HOME"):
            print ("Are no devices at home, activating AWAY mode.")
            t.setAway()
            print ("Done!")
            print ("Waiting for a change in devices location..")
    
        devicesHome.clear()

        time.sleep(5) # checking interval (in seconds)
        checkDevicesLocation()

    except KeyboardInterrupt:
        print ("Interrupted by user.")
        sys.exit(0)

    except Exception as e:
        print(e)
        if (str(e).find("ConnectionError") != -1):
            print ("Connection Error, retrying in 30 sec..")
    
            time.sleep(30) # retrying interval (in seconds), in case of connection error
            checkDevicesLocation()

main()