from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
from matplotlib import pyplot as plt
import ECE16Lib.DSP as filt
from time import time
import numpy as np


if __name__ == "__main__":
  fs = 50
  num_samples = 250                # 5 seconds of data @ 50Hz
  refresh_time = 0.1               # update the plot every 0.1s (10 FPS)

  ped = Pedometer(num_samples, fs, [])

  comms = Communication("/dev/ttyUSB0", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  #TEST 1
  #ped.threshSetter(100, 1000) # to set the threshold

  #TEST 2
  #ped.threshSetter(100, 500)  # to set the threshold

  #TEST 3
  ped.threshSetter(100, 850)   # to set the threshold

  try:
    theSteps = 0
    previous_time = 0
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        ped.add(int(m2),int(m3),int(m4))


        # if enough time has elapsed, clear the axis, and plot
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time

          steps, peaks, filtered = ped.process()
          theSteps = steps
          print("theSteps: "+str(theSteps))
          
          plt.cla()
          # plt.plot(filtered) #UNCOMMENT THIS LINE TO SEE PLOT

          plt.show(block=False)
          plt.pause(0.001)

  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()
