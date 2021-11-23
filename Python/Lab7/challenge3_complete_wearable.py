### ECE16Lib ESSENTIALS ###
from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
from ECE16Lib.HRMonitor import HRMonitor
### MACHINE LEARNING ###
from sklearn.mixture import GaussianMixture as GMM
import ECE16Lib.GMMTrain as gmmt
### WEATHER ###
from pyowm.utils import timestamps
from pyowm.utils import config
from pyowm import OWM
### TIMINGS ###
from time import sleep
from time import time
import datetime
### DATA ###
from matplotlib import pyplot as plt
import numpy as np


if __name__ == "__main__":

  ### Sampling/Timings ###
  fs = 50                         # sampling rate
  num_samples = 500               # 10 seconds of data @ 50Hz
  refresh_time = 1                # process data every one second

  ### HeartRate, GMM ###
  directory = "./data"
  subjects = gmmt.get_subjects(directory)

  ### PEDOMETER ###
  ped = Pedometer(num_samples, fs, [])

  ### Communication ###
  comms = Communication("/dev/ttyUSB0", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message(" ")         # begin sending data

  ### Data ### 
  times = CircularList([], num_samples)
  ppg = CircularList([], num_samples)

  ### Init Weather API ###
  owm = OWM('dd25a8ed48b2b2b12d7a71c45e5ca1eb').weather_manager()

  try:
    previous_time = time()
    sample = 0
    last_hr = 0
    steps = 0
    theTime = ""
    printDate = False
    lastState = False

    # retrieving/updating weather data
    fade = owm.weather_at_place('san diego,ca,us')
    weather = fade.weather
    final_output = weather.status + ' ' + str(weather.temperature('celsius')['temp_max'])

    while(True):
      mcuInput = "" # to send to the MCU
      message = comms.receive_message()
      anotherMsg = comms.rec_msg()
      if (str(anotherMsg) == "b'm'"): # button is pressed
        if (lastState == True):
          printDate = False # print weather instead
        elif (lastState == False):
          printDate = True  # print date

      lastState = printDate # update last state

      if (message != None):
        try:
          # in the order: t, ppg, ax, ay, az 
          (m1, m2, m3, m4, m5) = message.split(',')
        except ValueError:  # if corrupted data, skip the sample
          continue

        ### collecting data for PPG & Pedometer ###
        ped.add(int(m3),int(m4),int(m5))

        if (sample < num_samples):
          times.add(int(m1))
          ppg.add(int(m2))
          sample += 1

        ### PPG processing ###
        if (sample == num_samples):
          data = np.column_stack([times, ppg])
          t = data[:,0]
          t = (t - t[0])/1e3 # make time range from 0-10 in seconds
          ppgf = data[:,1]
          hr_monitor = HRMonitor(500, 50)
          # predicting hr with gmm
          hr, peaks = hr_monitor.predict(subjects, directory, ppgf, fs)
          last_hr = hr
          sample = 0 # reset sample to 0

        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time

          # Pedometer processing
          steps, peaks, filtered = ped.process()

          # Updating Time & Date
          theTime = datetime.datetime.now().strftime("%H:%M:%S")
          theDate = datetime.date.today()
          outputDate = theDate.strftime("%b-%d- %Y")

          ### Sending data to MCU ###
          if (printDate):
            # button was pressed, so display date instead of weather
            mcuInput += "h"+str(round(last_hr,2)) + \
                        "x"+str(steps) + \
                        "t"+(theTime) + \
                        "q"+outputDate+"z"
          else:
            mcuInput += "h"+str(round(last_hr,2)) + \
                        "x"+str(steps) + \
                        "t"+(theTime) + \
                        "q"+final_output+"z"

          comms.send_message(mcuInput)

  except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
  finally:
    print("Closing connection.")
    comms.send_message("sleep")  # stop sending data
    comms.close()
