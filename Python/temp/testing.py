from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from scipy.signal import savgol_filter
import numpy as np
from matplotlib import pyplot as plt
from time import time

def moving_average(x, win):
  ma = np.zeros(100)
  for i in np.arange(0,len(x)):
    if(i < win): # use mean until filter is "on"
      ma[i] = np.mean(x[:i+1])
    else:
      ma[i] = ma[i-1] + (x[i] - x[i-win])/win
  return ma

def process(target, win):
  out = moving_average(target, win)
  return out

if __name__ == "__main__":
  num_samples = 100               # 2 seconds of data @ 50Hz
  refresh_time = 0.1              # update the plot every 0.1s (10 FPS)

  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)

  ax_f = CircularList([], num_samples)
  ay_f = CircularList([], num_samples)
  az_f = CircularList([], num_samples)

  comms = Communication("/dev/ttyUSB0", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    previous_time = 0
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))

        # if enough time has elapsed, clear the axis, and plot az
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time
          plt.cla()

          az_process = process(az, 20)
          az_f.add(az_process.tolist())
          plt.plot(times, np.array(az_f), color='tab:gray')
          #plt.plot(times, az, color='tab:orange')

          ax_process = process(ax, 20)
          ax_f.add(ax_process.tolist())
          plt.plot(times, np.array(ax_f), color='r')
          #plt.plot(times, ax, color='b')

          ay_process = process(ay, 20)
          ay_f.add(ay_process.tolist())
          plt.plot(times, np.array(ay_f), color='c')
          #plt.plot(times, ay, color='k')

          plt.show(block=False)
          plt.pause(0.001)

  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()
