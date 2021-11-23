from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HRMonitor import HRMonitor
from matplotlib import pyplot as plt
from time import sleep
from time import time
import numpy as np

if __name__ == "__main__":
  fs = 50                         # sampling rate
  num_samples = 500               # 10 seconds of data @ 50Hz
  refresh_time = 1                # process data every one second

  comms = Communication("/dev/ttyUSB0", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  # create circular list for timees and ppg
  times = CircularList([], num_samples)
  ppg = CircularList([], num_samples)

  try:
    previous_time = time()
    while(True):
      sample = 0
      while (sample < num_samples):
        # get 500 samples, then only process data, and send bpm
        print(sample)
        message = comms.receive_message()
        if(message != None):
          try:
            (m1, m2) = message.split(',')
          except ValueError:  # if corrupted data, skip the sample
            continue

          times.add(int(m1))
          ppg.add(int(m2))
          sample += 1
          current_time = time()
          if (current_time - previous_time > refresh_time):
            previous_time = current_time
            comms.send_message("measuring")   # to refresh oled

      data = np.column_stack([times, ppg])
      t = data[:,0]
      t = (t - t[0])/1e3 # make time range from 0-10 in seconds
      ppgf = data[:,1]
      # use HR monitor class to process data
      hr_monitor = HRMonitor(500, 50)
      hr_monitor.add(t, ppgf)
      hr, peaks, filtered = hr_monitor.process()
      comms.send_message(str(round(hr, 2)))
      # send bpm to MCU, round to 2dp

  except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
  finally:
    print("Closing connection.")
    comms.send_message("sleep")  # stop sending data
    comms.close()
