from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
import math

# Helper functions: 
def getAvg(alist):
  return (sum(alist)/len(alist))

def getDelta_x(curr, prev):
  return (curr - prev)

def getL2_norm(x, y, z):
  return (math.sqrt((x**2)+(y**2)+(z**2)))

def getL1_norm(x, y, z):
  return (abs(x[-1])+abs(y[-1])+abs(z[-1]))

def getTransform(x):
  return (x**2)

# main:
if __name__ == "__main__":
  num_samples = 250               # 5 seconds of data @ 50Hz
  refresh_time = 0.1              # update the plot every 0.1s (10 FPS)

  timestamp = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)

  average_x = CircularList([], num_samples)
  delta_x = CircularList([], num_samples)
  L1 = CircularList([], num_samples)
  L2 = CircularList([], num_samples)
  transformed = CircularList([], num_samples)

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
          # getting accelerometer values
        except ValueError:        # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        timestamp.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))

        average_x.add(getAvg(ax))
        delta_x.add(getDelta_x(ax[-1], ax[-2]))
        L2.add(getL2_norm(ax[-1], ay[-1], az[-1])) 
        L1.add(getL1_norm(ax,ay,az))
        transformed.add(getTransform(az[-1]))

        # if enough time has elapsed, clear the axis, and plot az
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time
          # clearing figure
          plt.clf()

          ### plotting ###
          # ax
          plt.subplot(3,1,1)
          plt.plot(ax, color='r')
          plt.title('ax (original x axis plot)')

          # average_x (comment me or delta_x)
          plt.subplot(3,1,2)
          test2 = plt.plot(average_x, color='g')
          plt.title('average_x')
          # NOTE: the plot for average_x might look
          # like a weird straight line at first, dw just wait
          # it will show pattern overtime.

          # delta_x (comment me or average_x)
          # plt.subplot(3,1,2)
          # plt.plot(delta_x, color='tab:orange')
          # plt.title('delta_x')

          # L2 (comment me or L1)
          # plt.subplot(3,1,3)
          # plt.plot(L2, color='b')
          # plt.title('L2')

          # L1 (comment me or L2)
          # plt.subplot(3,1,3)
          # plt.plot(L1, color='m')
          # plt.title('L1')

          # transformed (comment me or L2 AND L1)
          # plt.subplot(3,1,3)
          # plt.plot(transformed, color='c', linestyle='dashed')
          # plt.title('transformed (custom)')

          plt.show(block=False)
          plt.pause(0.001)

  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()
