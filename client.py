#!/usr/bin/env python

#from geopy.geocoders import Nominatim
#from geopy.exc import GeocoderTimedOut
import serial
import time 
import asyncio
import websockets
import json as j
#import pynmea2
#from pynmea2 import ChecksumError
#from pynmea2 import ParseError

ser =serial.Serial("/dev/ttyAMA0", 9600, timeout=1)

async def hello():
    async with websockets.connect('ws://192.168.1.222:8765') as websocket:
            while True:
                    print("connected !")
                    data = await retrieve()
                    await websocket.send(str(data))
                    print("> {}".format(data))
                    greeting = await websocket.recv()
                    print("< {}".format(data))
                    time.sleep(10)


async def retrieve():
        #print("I am debugging before read :)")
        data = ser.readline().decode()
        #print("I am debugging after read :(")
        print(data)
        data_to_be_sent = await concurrent(data)
        return(data_to_be_sent)

async def concurrent(data):    
    #while True:
    for line in data.split('\n'):
        unit = line[4:8]
        load = line[13:17]
        power_factor = line[20:24]
        data = {"unit":unit, "load":load, "power_factor":power_factor}
        #data_json = j.loads(data)
        print(data['unit'])
        return data
        #if line.startswith('$GPGGA'):
            #if pynmea2.ChecksumError(line):
            #try:
                #msg = pynmea2.parse(line)
                #print(msg)
                #lat = msg.latitude
                #lng = msg.longitude
                #print(lat, lng)
                #coordinate = str(lat) + ', ' + str(lng)
                #print(coordinate)
                #geolocator = Nominatim()
                #location = geolocator.reverse(coordinate,timeout=10)
                #return(location.address)
            #except(ChecksumError, ParseError, KeyError) as e:
                #print(e)
                
            




asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
