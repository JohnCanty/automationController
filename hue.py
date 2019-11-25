#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 19:29:10 2019

@author: johncanty
"""
from datetime import datetime, timedelta
from phue import Bridge
from itachip2ir import VirtualDevice, iTach
import time
import re
import requests
import random

def set_light_time(Brightness, lightid, status, current_brightness):
        if current_brightness != Brightness:
            if status == False:
                b.set_light(lightid, 'on',  value=True)
                b.set_light(lightid, 'bri',  value=Brightness)
                b.set_light(lightid, 'on',  value=False)
            else:
                b.set_light(lightid, 'bri',  value=Brightness)
                
def get_sun_time(func, file):
    try:
        fh = open(file)
    except:
        if func == 'Sunrise':
            return 612
        if func == 'Sunset':
            return 1700
    for line in fh:       
        return line

def cameras_rec(state, number):
    i = int(0)
    while i < int(number):
        d = i + 1
        uname = str('axis_' + str(d) + '_username:')
        pword = str('axis_' + str(d) + '_password:')
        ip = str('axis_' + str(d) + '_ip:')
        if state == 'on': #turn on recording we drop the presence bit in the camera.
            url = 'http://' + parameters[ip] + '/axis-cgi/virtualinput/deactivate.cgi?schemaversion=1&port=1'
        if state == 'off': #turn the camera off we let it know we are here.
            url = 'http://' + parameters[ip] + '/axis-cgi/virtualinput/activate.cgi?schemaversion=1&port=1'
        else:
            print('not a supported state: ' + state)
        username = parameters[uname]
        password = parameters[pword]
        requests.get(url, auth=(username, password)).content
        i=i+1

def sonoff_state(state, ip):
    if state == 'on': #turning Motion detectors on
        url = 'http://' + ip + '/on'
    if state == 'off': #turning motion detectors off
        url = 'http://' + ip + '/off'
    else:
        print('not a supported state: ' + state)
    requests.get(url).content
        
def motion_detect(state, number):
    i = int(0)
    while i < int(number):
        d = i + 1
        ip = str('motion_' + str(d) + '_ip:')
        if state == 'on': #turning Motion detectors on
            url = 'http://' + parameters[ip] + '/on'
        if state == 'off': #turning motion detectors off
            url = 'http://' + parameters[ip] + '/off'
        else:
            print('not a supported state: ' + state)
        requests.get(url).content
        i = i + 1

def send_ir_command(ip, port, command):
    commands = {"toggle_power":command}
    itach = iTach(ipaddress=ip, port=int(port))
    stereo = itach.add(VirtualDevice(name="stereo", commands=commands))
    if __name__ == "__main__": print(stereo.toggle_power())

def get_time():
    timing['current_time:'] = datetime.now()
    timing['current_year:'] = int(timing['current_time:'].strftime('%Y'))
    timing['current_month:'] = int(timing['current_time:'].strftime('%m'))
    timing['current_day:'] = int(timing['current_time:'].strftime('%d'))
    timing['current_day_week:'] = int(timing['current_time:'].strftime('%w'))
    timing['current_hour:'] = int(timing['current_time:'].strftime('%H'))
    timing['current_minute:'] = int(timing['current_time:'].strftime('%M'))
    timing['current_second:'] = int(timing['current_time:'].strftime('%S'))

def time_passed(marker): #check to see if an hour passed
    t1 = marker
    t2 = datetime.now()
    diff = t2 - t1
    return int(diff.seconds / 60) # will return the number of minutes passed since the first timestamp
    
def time_until(time_point):
    t1 = datetime.now()
    t2 = time_point
    diff = t2 - t1
    return int(diff.seconds / 60) # will retyrn the number of minutes until a future time point

def generate_rand(high):
    for x in range(1):
        result = int(random.randint(1,high))
    return result

# Create a dictionary with the parameters from the config file
parameters = dict()
timing = dict()
fname = './automation.cfg'
try:
    fh = open(fname)
except:
    print('Filename not found:', fname)
    quit()
for line in fh:
    if '#' in line: continue
    else:
        parameter = str(re.findall('.+: (.+)', line))
        parameter = parameter.strip("['']")
        parameter_name = str(re.findall('.+: ', line))
        parameter_name = parameter_name.strip("[' ']")
        if parameter_name == '': continue
        else: parameters[parameter_name] = parameters.get(parameter_name,parameter)

#Get initial time for setup
get_time()

# Establish sunrise and sunset times from the files indicated in the config file setup
timing['sunrise_time:'] = get_sun_time('Sunrise', parameters['Sunrise:'])
timing['sunrise_hour:'] = int(str(timing['sunrise_time:'])[:-2])
timing['sunrise_minute:'] = int(str(timing['sunrise_time:'])[-2:])
timing['sunset_time:'] = get_sun_time('Sunset', parameters['Sunset:'])
timing['sunset_hour:'] = int(str(timing['sunset_time:'])[:-2])
timing['sunset_minute:'] = int(str(timing['sunset_time:'])[-2:])
sunrise = datetime(year=timing['current_year:'], month=timing['current_month:'], day=timing['current_day:'], hour=timing['sunrise_hour:'], minute=timing['sunrise_minute:'], second=0)
timing['sunrise_timestamp:'] = datetime.fromtimestamp(time.mktime(sunrise.timetuple()))
sunset = datetime(year=timing['current_year:'], month=timing['current_month:'], day=timing['current_day:'], hour=timing['sunset_hour:'], minute=timing['sunset_minute:'], second=0)
timing['sunset_timestamp:'] = datetime.fromtimestamp(time.mktime(sunset.timetuple()))

# create a bridge instance with the IP address and API key from the config file setup
b = Bridge(parameters['hue_ip:'], parameters['hue_api:'])

# turn on bridge logging
#b.logging=('ERROR')
# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the light information from the bridge and store it in a dictionary based on ID as the key.
lights = b.get_light_objects(mode='id')

# Calculate time since an action
#device = str('sheisse')
#parameters[device + '_start_time:'] = datetime.now() - timedelta(minutes=15)
#print(time_passed(parameters['sheisse_start_time:']))

#generate a random number lower than 60
#print(generate_rand(60))

# Example of getting time passed since a device was turned on
#print(time_passed(parameters['sheisse_start_time:']))

# This executes the gcir_payload
#send_ir_command(parameters['gcir_ip:'], parameters['gcir_port:'], parameters['gcir_payload_1:'])

#Changing state of motion detectors
#motion_detect('on', parameters['number_motion:']) #Turn motion detectors on
#motion_detect('off', parameters['number_motion:']) #Turn motion detectors off

#Changing the camera states
#cameras_rec('off', parameters['number_cameras:']) #Stop the cameras from recording
#cameras_rec('on', parameters['number_cameras:']) #Start recording

#set lights to alert mode change lselect to select to turn off
#b.set_light( [1,2,3,4,5,6,7,8], 'alert', 'lselect')

#Changing the light brightness for all lights
#for lightid,attribute in lights.items():
#    print(lightid)
#    print(attribute.name)
#    print(attribute.on)
#    print(attribute.type)
#    if attribute.type == ("Dimmable light" or "Extended color light"): #Keep from trying to set attributes to on/off switches
#        print(attribute.brightness)
#        print(datetime.now().strftime('%H'))
#        set_light_time(255, lightid, attribute.on, attribute.brightness)