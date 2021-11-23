from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HRMonitor import HRMonitor
from matplotlib import pyplot as plt
from time import sleep
import numpy as np
import time
import cv2

if __name__ == "__main__":
  fs = 50                         # sampling rate
  num_samples = 500               # 10 seconds of data @ 50Hz
  refresh_time = 1                # process data every one second

  comms = Communication("/dev/ttyUSB0", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  # create a circular list to store timestamp and ppg data
  times = CircularList([], num_samples)
  ppg = CircularList([], num_samples)

  try:
    previous_time = time.time()
    while(True):
      sample = 0
      cap = cv2.VideoCapture(2) # get webcam feed
      while (sample < num_samples):
        ret, frame = cap.read() # read webcam feed
        new_sample = frame.mean(axis=0).mean(axis=0)

        time_nanosec = time.time_ns()

        # processing the incoming data from webcam:
        new_sample = new_sample[2] # get red channel only
        times.add(int(time_nanosec/(10**9)))  # add timestamp data
        ppg.add(int(new_sample)) # add the ppg data
        print(new_sample) # for me to monitor
        cv2.imshow('Input', frame) # show video output window
        
        current_time = time.time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time
          comms.send_message("measuring") # to refresh oled

        sample += 1

        c = cv2.waitKey(1)
        if c == 27:
          break

      # processing data (500 samples):
      data = np.column_stack([times, ppg])
      t = data[:,0]
      t = (t - t[0]) # make time range from 0-10 in seconds
      ppgf = data[:,1]
      hr_monitor = HRMonitor(500, 50)
      hr_monitor.add(t, ppgf)
      hr, peaks, filtered = hr_monitor.process()
      # send hr to MCU, round to 2 dp
      comms.send_message(str(round(hr, 2)))

      # release and destroy windows
      cap.release()
      cv2.destroyAllWindows()

  except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
  finally:
    print("Closing connection.")
    comms.send_message("sleep")  # stop sending data
    comms.close()
