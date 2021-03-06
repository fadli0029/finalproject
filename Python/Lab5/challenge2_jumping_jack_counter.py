from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
from matplotlib import pyplot as plt
from time import time
from time import sleep
import numpy as np

if __name__ == "__main__":
  fs = 50                         # sampling rate
  num_samples = 250               # 5 seconds of data @ 50Hz
  process_time = 1                # compute the step count every second

  ped = Pedometer(num_samples, fs, [])

  comms = Communication("/dev/ttyUSB0", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  ped.threshSetter(75, 1500) # to set the threshold

  try:
    previous_time = time()
    sleep(2) # so i can skip first peak due to picking up the watch
    theSteps = 0
    while(True):
      message = comms.receive_message()
      anotherMsg = comms.rec_msg()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue

        ped.add(int(m2),int(m3),int(m4))

        # if enough time has elapsed, process the data and plot it
        current_time = time()
        if (current_time - previous_time > process_time):
          previous_time = current_time

          steps, peaks, filtered = ped.process()
          theSteps = steps

          plt.cla()
          plt.plot(filtered)
          plt.title("Step Count: %d" % steps)
          plt.show(block=False)
          plt.pause(0.001)

      # checking if button is pressed, if yes
      # send step count to terminal, and MCU
      # then display on OLED (dealt by MCU)
      if (str(anotherMsg) == "b'm'"):
        comms.send_message(str(theSteps))
        print("Step count: {:d}".format(theSteps))

  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    print("Closing connection.")
    comms.send_message("sleep")  # stop sending data
    comms.close()
