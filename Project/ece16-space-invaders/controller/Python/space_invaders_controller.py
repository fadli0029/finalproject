"""
@author: Ramsin Khoshabeh
"""

from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from time import sleep
from time import time
import socket, pygame
import numpy as np

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)

class PygameController:
  comms = None

  num_samples = 0
  refresh_time = 0
  the_sensitivity = 0

  times = None
  ax = None
  ay = None
  az = None
  ax_f = None
  ay_f = None
  az_f = None

  def __init__(self, serial_name, baud_rate, samplings_Num, refresh_rate, sens):
    self.the_sensitivity = sens

    self.num_samples = samplings_Num
    self.refresh_time = refresh_rate

    self.comms = Communication(serial_name, baud_rate)

    self.times = CircularList([], self.num_samples)
    self.ax = CircularList([], self.num_samples)
    self.ay = CircularList([], self.num_samples)
    self.az = CircularList([], self.num_samples)

    self.ax_f = CircularList([], self.num_samples)
    self.ay_f = CircularList([], self.num_samples)
    self.az_f = CircularList([], self.num_samples)

  def moving_average(self, x, win):
    ma = np.zeros(100)
    for i in np.arange(0,len(x)):
      if(i < win): # use mean until filter is "on"
        ma[i] = np.mean(x[:i+1])
      else:
        ma[i] = ma[i-1] + (x[i] - x[i-win])/win
    return ma

  def process(self, target, win):
    out = self.moving_average(target, win)
    return out

  def is_between(self, target, x, y):
    return (target >= x and target <= y)

  def generatingCommand(self, xf_input, yf_input, zf_input):
    adj_xLeft = 0
    adj_xRight = 0
    adj_z = 0
    if (self.the_sensitivity == 2):
      adj_xLeft = 500
      adj_xRight = 140
      adj_z = 230

    adjusted_thresLeft = 2300+adj_xLeft
    adjusted_thresRight = 1655-adj_xRight
    adjusted_thresZ = 2200-adj_z

    command = None
    # this functiong takes in self.ax_f, etc
    x_cmd = np.array(xf_input)
    y_cmd = np.array(yf_input)
    z_cmd = np.array(zf_input)

    #print(2300+adj_x)

    # previous upper bound: 1956
    if (self.is_between(x_cmd[-1], 1950, 1970) == False):
        # tilting
        # az can drop to lowest to 2.2k, regardless tilted
        # left or right
        # ax can go up to 2300 when tilt left
        # and as low as 1655 when tilt right
      if (x_cmd[-1] <= adjusted_thresLeft and x_cmd[-1] > 1956 and z_cmd[-1] > adjusted_thresZ):
        # tilt left
        command = "LEFT"
      if (x_cmd[-1] >= adjusted_thresRight and x_cmd[-1] < 1950 and z_cmd[-1] > adjusted_thresZ):
        # tilt right
        command = "RIGHT"

    return command, x_cmd[-1], z_cmd[-1]

  def run(self):

    # 1. make sure data sending is stopped by ending streaming
    lastMessage =  None
    shoot = False

    self.comms.send_message("stop")
    self.comms.clear()

    # 2. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    self.comms.send_message("start")

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Use <CTRL+C> to exit the program.\n")
    previous_time = 0

    while True:
      message = self.comms.receive_message()

      if(message != None):
        f_command = None
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        self.times.add(int(m1))
        self.ax.add(int(m2))
        self.ay.add(int(m3))
        self.az.add(int(m4))

        # if enough time has elapsed, clear the axis, and plot az
        current_time = time()
        if (current_time - previous_time > self.refresh_time):
          previous_time = current_time
          #plt.cla()

          az_process = self.process(self.az, 20)
          self.az_f.add(az_process.tolist())
          #plt.plot(times, np.array(az_f), color='tab:gray')
          #plt.plot(times, az, color='tab:orange')

          ax_process = self.process(self.ax, 20)
          self.ax_f.add(ax_process.tolist())
          #plt.plot(times, np.array(ax_f), color='r')
          #plt.plot(times, ax, color='b')

          ay_process = self.process(self.ay, 20)
          self.ay_f.add(ay_process.tolist())
          #plt.plot(times, np.array(ay_f), color='c')
          #plt.plot(times, ay, color='k')

          f_command, valx, valz = self.generatingCommand(self.ax_f, self.ay_f, self.az_f)

          #plt.show(block=False)
          #plt.pause(0.001)
          if f_command is not None:
            #print(f_command + '[' + str(valx) + ']' + '[' + str(valz) + ']')
            mySocket.send(f_command.encode("UTF-8"))
          #if f_command is None:
          #  print("None" + '[' + str(valx) + ']' + '[' + str(valz) + ']')


      # if the last message is similar to current message,
      # don't send any message to avoid lagging due
      # to continuously sending messages 
      #if ((message != lastMessage) and (message != None)):
      #  command = None
      #  message = int(message)

      #  if message == 23:
      #    command = "RFIRE"
      #  elif message == 24:
      #    command = "LFIRE"
      #  elif message == 20:
      #    command = "FIRE"
      #  elif message == 74:
      #    command = "LEFT"
      #  elif message == 73:
      #    command = "RIGHT"

      #  if command is not None:
      #    mySocket.send(command.encode("UTF-8"))

      #lastMessage = message

if __name__== "__main__":
  #serial_name = "/dev/cu.BTDemo-ESP32SPP"
  the_num_samples = 100               # 2 seconds of data @ 50Hz
  the_refresh_time = 0.01              # update the plot every 0.1s (10 FPS)
  sensitivity = 2

  serial_name = "/dev/ttyUSB0"
  baud_rate = 115200
  controller = PygameController(serial_name, baud_rate, the_num_samples, the_refresh_time, sensitivity)

  try:
    controller.run()
  except(Exception, KeyboardInterrupt) as e:
    print(e)
  finally:
    print("Exiting the program.")
    controller.comms.send_message("stop")
    controller.comms.close()
    mySocket.send("QUIT".encode("UTF-8"))
    mySocket.close()

  input("[Press ENTER to finish.]")
