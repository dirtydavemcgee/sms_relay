#!/usr/bin/env python
#starter.py - a quick and dirty remote start via SMS project
#came about when I was driving a work truck to my personal truck located at the shop I work in
#the thermometer in the work truck told me it was 17 degrees. I wished there was a way to start my personal
#from wherever I am instead of the limited range of the keyfob I have to remote start it normally.
#add 
#    "sudo python /home/pi/starter.py &"
#to the file "/etc/rc.local" before the end where it says
#   exit 0
#The personal has an Avitol 4103 remote start installed, with an activation pin.
#all the wiring I am going to do is tied in to the wiring for the remote start.
#First ever python project. 
import time #import some stuff to help us out
import datetime
import sys
from Hologram.HologramCloud import HologramCloud #this one helps the most
import RPi.GPIO as GPIO #this one is awesome too
GPIO.setwarnings(False) #turn off warnings
GPIO.setmode(GPIO.BCM) #initialize gpio mode and set pins to off by default
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH) #GPIO wired to start relay
GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH) #GPIO wired to flash parking lights
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH) #GPIO wired to door lock relay
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH) #GPIO wired to door unlock relay
print 'Remote Start SMS Controller' #welcome message for console
hologram=HologramCloud(dict(), network='cellular') #setup hologram cloud
hologram.enableSMS #tell hologram to listen for sms
recv=None #if we dont set initial variables the loop breaks
cmd=None
while True: #start the loop
	recv = hologram.popReceivedSMS() #this works, makes the recv variable equal an incoming message
	if recv is not None: #works, run the following code when a message comes in
		print 'SMS From: ', recv.sender #print the sender of the sms
		cmd = recv.message #works, makes the cmd variable the payload of the message.
		print cmd #works, prints only what the sms message is.
		#we want to look for 3 commands, start, lock, or unlock. I have no clue how to deal with mismatched cases so I did this.
		#we also have parking light flash on the lock and unlock functions. the remote starter flashes the lights during the start command.
		if cmd == 'Start' or cmd == 'start': #works,(thanks Gary H.) checks for start or Start
			print 'Start command received' #let the console show we know the SMS had the word start and we will process it
			GPIO.output(17, GPIO.LOW) #close the starter relay. The remote start expects a pattern.
			time.sleep(1) #wait one second with the relay closed
			GPIO.output(17, GPIO.HIGH) #open the relay
			time.sleep(1) #wait one sec, relay open
			GPIO.output(17, GPIO.LOW) #close the relay again
			time.sleep(1) #wait one, relay closed
			GPIO.output(17, GPIO.HIGH) #open the relay again, completeing the expected activation pulse to the remote start.
			print 'Start command executed' #let the console know we did it
		elif cmd == 'Lock' or cmd == 'lock': #works, checks for lock or Lock
			print 'Door lock command received' #let the console know the SMS was lock or Lock
			GPIO.output(18, GPIO.LOW) #Close the light relay
			GPIO.output(22, GPIO.LOW) #Close the door lock relay
			time.sleep(.5) #wait half a second
			GPIO.output(18, GPIO.HIGH) #Open the light relay
			GPIO.output(22, GPIO.HIGH) #open the door lock relay
			print 'Door lock command executed' #let the console know we did it
		elif cmd == 'Unlock' or cmd == 'unlock': #works, checks for unlock
			print 'Door unlock command received' #let the console know unlock or Unlock
			GPIO.output(18, GPIO.LOW) #Close the light relay
			GPIO.output(27, GPIO.LOW) #Close the door unlock relay
			time.sleep(.5) #wait half a second
			GPIO.output(18, GPIO.HIGH) #open the light relay
			GPIO.output(27, GPIO.HIGH) #open the door unlock relay
			time.sleep(.5) #wait again
			GPIO.output(18, GPIO.LOW) #close light relay
			time.sleep(.5) #wait one more time
			GPIO.output(18, GPIO.HIGH) #open relay
			print 'Door unlock command executed' #let console know we did it
	if recv is None: #works, runs the following code when there is no message
		print 'No Command, sleep 60 seconds', datetime.datetime.now() #works, prints timestamp, handy for troubleshooting
		time.sleep(60) # one minute checks for new messages seems reasonable
		print '' #prints a blank line in the console between timestamps when we have no messages for my personal prefrence
