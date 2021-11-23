# API key: dd25a8ed48b2b2b12d7a71c45e5ca1eb

import serial   # the PySerial Library
import time     # for timing purposes
import datetime # for retrieving current date and time

# for retrieving weather info
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

owm = OWM('dd25a8ed48b2b2b12d7a71c45e5ca1eb').weather_manager()
fade = owm.weather_at_place('san diego,ca,us')
weather = fade.weather
final_output = weather.detailed_status + ' ' + str(weather.temperature('celsius')['temp_max'])
# for getting status 'clear sky' (at that time) and temp in celsius, specifically the temp_max

def setup(serial_name, baud_rate):
    ser = serial.Serial(serial_name, baudrate=baud_rate)
    return ser

def send_message(ser, message):
    if (message[-1] != '\n'):
        message = message + '\n'
    ser.write(message.encode('utf-8'))
    # to send message to MCU

def receive_message(ser, num_bytes=50):
    if (ser.in_waiting > 0):
        return ser.readline(num_bytes).decode('utf-8')
    else:
        return None
    # to receive message

def close(ser):
    ser.close()
    # to close communication

def main_2():
    ser = setup("/dev/ttyUSB0", 115200)
    time.sleep(3)
    send_message(ser, "fadli alim\n")
    time.sleep(3)
    close(ser)
    # this is from tutorial, I will be using main()
    # for the challenge

def main():
    ser = setup("/dev/ttyUSB0", 115200)
    theTime = datetime.datetime.now().strftime("%H:%M:%S")
    # to retrieve current time, and format it in Hour, Minute, Second
    theDate = datetime.date.today()
    outputDate = theDate.strftime("%b-%d-%Y")
    # to retrive today's date and format in Month, Day, Year
    place = "San Diego, CA"
    # just a regular string
    send_message(ser, theTime)
    send_message(ser, final_output)
    send_message(ser, outputDate)
    send_message(ser, place)
    # sending the string messages to MCU via BT
    time.sleep(1)
    # to see display on OLED
    close(ser)

"""
Main entrypoint for the application
"""

if __name__== "__main__":
    while (True) :
        main()

