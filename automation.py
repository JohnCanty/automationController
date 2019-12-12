#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 19:29:10 2019

@author: johncanty
"""
from datetime import datetime, timedelta
from phue import Bridge
from itachip2ir import VirtualDevice, iTach
import logging
import logging.handlers
import wifiStat as stat
import time
import re
import requests
import random

def set_light_time(Brightness, lightid, status, current_brightness):
        if current_brightness != Brightness:
            if status == True:
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
            logger.error("State not supported " + state)
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
    timing['current_epoch:'] = int(time.time())

def time_passed(marker, hms): #check to see if an hour passed
    t1 = marker
    t2 = datetime.now()
    diff = t2 - t1
    if hms == 'm':
        return int(diff.seconds / 60) # will return the number of minutes passed since the first timestamp
    if hms == 'h':
        return int(diff.seconds / 3600) # will return the number of hours passed since the first timestamp
    else:
        return int(diff.seconds) # will return the number of seconds passed since the first timestamp
    
def time_until(time_point):
    t1 = datetime.now()
    t2 = time_point
    diff = t2 - t1
    return int(diff.seconds / 60) # will retyrn the number of minutes until a future time point

def generate_rand(high):
    for x in range(1):
        result = int(random.randint(1,high))
    return result

def future_time(advance):
    timing['future_time:'] = datetime.now() + timedelta(minutes=int(advance))
    timing['future_year:'] = int(timing['future_time:'].strftime('%Y'))
    timing['future_month:'] = int(timing['future_time:'].strftime('%m'))
    timing['future_day:'] = int(timing['future_time:'].strftime('%d'))
    timing['future_day_week:'] = int(timing['future_time:'].strftime('%w'))
    timing['future_hour:'] = int(timing['future_time:'].strftime('%H'))
    timing['future_minute:'] = int(timing['future_time:'].strftime('%M'))
    timing['future_second:'] = int(timing['future_time:'].strftime('%S'))
    
def day_period(hour):
    if int(hour) >= 0 and int(hour) < 10:
        return 0
    if int(hour) >= 10 and int(hour) < 17:
        return 1
    if int(hour) >= 17 and int(hour) <= 23:
        return 2
    else:
        logger.error("Day period Failed!")
        return 5

class status(object):
          def indirect(self,i):
                   state['time_of_change'] = datetime.now()
                   state['satisfied'] = False # can't get no satisfaction upon change
                   state['stereo_on'] = False # Reset the state of the stereo off timer
                   method_name='state_'+str(i)
                   method=getattr(self,method_name,lambda :1)
                   return method()
          def state_0(self):
                   state['armed'] = bool(True)
                   state['disarmed'] = bool(False)
                   state['away'] = bool(False)
                   state['spare'] = bool(False)
                   return 0
          def state_1(self):
                   state['armed'] = bool(False)
                   state['disarmed'] = bool(True)
                   state['away'] = bool(False)
                   state['spare'] = bool(False)
                   return 0
          def state_2(self):
                   state['armed'] = bool(False)
                   state['disarmed'] = bool(False)
                   state['away'] = bool(True)
                   state['spare'] = bool(False)
                   return 0
          def state_3(self):
                   state['armed'] = bool(False)
                   state['disarmed'] = bool(False)
                   state['away'] = bool(False)
                   state['spare'] = bool(True)
                   return 0

# function to return key for any value 
def get_key(val, dictionary): 
    for key, value in dictionary.items(): 
         if val == value: 
             return key 
    logger.error("Key not found")
    return 1  

# Setup Logging
logger = logging.getLogger('Python')
logger.setLevel(logging.INFO)

# Create a dictionary with the parameters from the config file
parameters = dict()
timing = dict()
state = dict()

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

#add handler to the logger
handler = logging.handlers.SysLogHandler(address=(parameters['syslog_ip:'], int(parameters['syslog_port:'])))
#add formatting to handler
formatter = logging.Formatter('AutomationController: { "loggerName":"%(name)s", "timestamp":"%(asctime)s", "pathName":"%(pathname)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}')
handler.formatter = formatter
logger.addHandler(handler)

#Get initial time for setup
get_time()
logger.info("Controller Started")

#Get initial period
period = int(day_period(timing['current_hour:'])) # 0 Morning, 1 Afternoon, 2 Evening, 5 Oh Shit
logger.info("Starting Period " + str(period))
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

#seccode = stat.login(parameters['wifistat_ip:'], int(parameters['wifistat_port:']), parameters['wifistat_password:'])
#stat.set_time(parameters['wifistat_ip:'], int(parameters['wifistat_port:']), seccode, str(timing['current_epoch:']))
#stat.send_schedule(parameters['wifistat_ip:'], int(parameters['wifistat_port:']), seccode, '5', 'W,7,00,67,70;L,10,0,67,70;R,18,0,67,70;S,22,0,60,65' )

#setting a time in the future for events that get run via CRON Use Minutes in integer value
#future_time(30)

shat = int(0)
st = status()
st.indirect(shat)
while(True):
    if state['satisfied'] == False: # If there was a change, fall into this block of code
        if get_key(True,state) == 'armed': # The change was to arm the system (away mode)
            for lightid,attribute in lights.items(): # Shut shit down
                b.set_light( lightid, 'on', False)
            motion_detect('on', parameters['number_motion:']) #Turn motion detectors on
            state['stereo_on'] = True # assume the stereo is on, start the off timer 
            cameras_rec('on', parameters['number_cameras:']) #Start recording
        state['satisfied'] = True # The program has satisfied the change condition
        if get_key(True,state) == 'disarmed': # The change was to disarm the system
            cameras_rec('off', parameters['number_cameras:']) #Stop the cameras from recording
            motion_detect('off', parameters['number_motion:']) #Turn motion detectors off
            if period == 0: #morning
                b.set_light( [6,7,8,10], 'on', True) # Turn on the livingRoom, Bathroom and Kitchen lights
                time.sleep(1) # Give the bridge a second to update all the statuses
                lights = b.get_light_objects(mode='id') # Pull the latest status
                for lightid,attribute in lights.items(): # Set everything to full brightness
                    if attribute.type == ("Dimmable light" or "Extended color light"): #Keep from trying to set attributes to on/off switches
                        set_light_time(254, lightid, attribute.on, attribute.brightness)
            if period == 1: #afternoon
                pass # nothing else to do place holder
            if period == 2: #evening
                b.set_light( [6,7], 'on', True)
    if timing['current_hour:'] > int(18) and timing['current_hour:'] < int(22):
        timestamp1800 = datetime(year=timing['current_year:'], month=timing['current_month:'], day=timing['current_day:'], hour=18, minute=0, second=0)
        brightness_dim = int(254 - time_passed(timestamp1800, 'm'))
        lights = b.get_light_objects(mode='id') # Pull the latest status
        for lightid,attribute in lights.items():
            if attribute.type == ("Dimmable light" or "Extended color light"): #Keep from trying to set attributes to on/off switches
                set_light_time(brightness_dim, lightid, attribute.on, attribute.brightness)
        
    else:
        get_time()
        period = int(day_period(timing['current_hour:'])) # 0 Morning, 1 Afternoon, 2 Evening, 5 Oh Shit
        break

# testing to get the key that has changed
#shat = int(2)
#st = status()
#st.indirect(shat)
#print(get_key(True,state))

# testing of state switching
#while(True):
#    shat = int(input('state:'))
#    st = status()
#    st.indirect(shat)
#    print(state['time_of_change'])
#    print(state['wake'])
#    print(state['sleep'])
#    print(state['away_wake'])
#    print(state['away_sleep'])

# Calculate time until action
#print(time_until(timing['sunrise_timestamp:']))

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

# Get the brightness of a light
# alight = b.get_light(4, 'bri')

#Changing the light brightness for all lights
#for lightid,attribute in lights.items():
#    if attribute.type == ("Dimmable light" or "Extended color light"): #Keep from trying to set attributes to on/off switches
#        set_light_time(144, lightid, attribute.on, attribute.brightness)