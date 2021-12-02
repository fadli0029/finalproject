from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt

"""
FUTURE PLANS:
-> be able to accept a specific transformation type
   as argument, and use that transformation
-> turn on weather forecast
-> choose which data to show in plot
(NOTE: For now, this module only satisfies
challenge3 requirements)
"""

class IdleDetector:
  # samplings/setups
  numSamples = 0
  refreshTime = 0
  __serial_name = ""
  __baud_rate = 115200

  # timings
  __oneSec = 1
  __counter = 0
  __prevTime = 0
  __prevTimeInactive = 0
  __prevTimeActive = 0

  # datas
  ax = CircularList([], numSamples)
  ay = CircularList([], numSamples)
  az = CircularList([], numSamples)
  timestamp = CircularList([], numSamples)
  average_x = CircularList([], numSamples)
  theInput = 0


  """
  IdleDetector constructor:
  ->  initialize numSamples, refreshTime, __serial_name, __baud_rate.
  ->  setup CircularList objects, and setup Communication by calling
      __setupCircularList() and __setupCommunication().

  """
  def __init__(self,  num_samples=None, refresh_time=None,
               serial_name=None, baud_rate=None):
    self.numSamples = num_samples
    self.refreshTime = refresh_time
    self.__serial_name = serial_name
    self.__baud_rate = baud_rate
    self.__setupCircularList(self.numSamples)
    self.__setupCommunication(self.__serial_name, self.__baud_rate)


  """
  setup CircularList objects:
  ->  initialize ax, ay, az, timestamp, average_x.

  """
  def __setupCircularList(self, samplesArg):
    self.ax = CircularList([], samplesArg)
    self.ay = CircularList([], samplesArg)
    self.az = CircularList([], samplesArg)
    self.timestamp = CircularList([], samplesArg)
    self.average_x = CircularList([], samplesArg)


  """
  setup Communication:
  -> initalize Communication object, __comms.
  -> call clear() and send_message() method to start communication.

  """
  def __setupCommunication(self, serialName, baudRate):
    self.__comms = Communication(serialName, baudRate)
    self.__comms.clear()
    self.__comms.send_message("wearable")



  """
  return average of most recent ax data:

  """
  def __getAvg(self, alist):
    return (sum(alist)/len(alist))


  """
  get accelerometer data from MCU:
  -> call receive_message() method, and assign it to theMessage.
  -> returns: theMessage.

  """
  def getData(self):
    self.theMessage = self.__comms.receive_message()
    return self.theMessage


  """
  update CircularList data:
  -> retrieve accelerometer data, assign it to timestamp, ax, ay, az.
  -> compute average, asssign it to average_x.

  """
  def updateData(self, m1_, m2_, m3_, m4_):
    self.timestamp.add(int(m1_))
    self.ax.add(int(m2_))
    self.ay.add(int(m3_))
    self.az.add(int(m4_))
    self.average_x.add(self.__getAvg(self.ax))


  """
  check if enough time has elapsed to begin plotting:
  -> requires current time as parameter.
  -> updates previous time.
  -> returns: Boolean.

  """
  def enoughTime(self, theTime):
    if (theTime - self.__prevTime > self.refreshTime):
      self.__prevTime = theTime
      return True


  """
  start plotting:
  -> clear figure, start plotting, label plot.
  -> extract data from most recent value of average_x, and prints it.

  """
  def beginPlotting(self):
    plt.clf()
    self.theplot = plt.plot(self.average_x, color='g')
    plt.title('average_x')
    # im only gonna plot average_x, to save computing power
    self.determ = self.theplot[-1].get_data()
    self.theInput = ((self.determ)[-1])[-1]
    print(self.theInput)
    plt.show(block=False)
    plt.pause(0.001)


  """
  check if user is idle:
  -> requires lower and upper bound (sensitivity) as parameters.
  -> handles timing, inactivityTime, default is 5 seconds
  -> returns: Boolean (True if idle).

  """
  def isIdle(self, theTime, lowerBound, upperBound, inactivity=5):
    if (self.theInput >= lowerBound and self.theInput <= upperBound):
      if (theTime - self.__prevTimeInactive > self.__oneSec):
        self.__counter += 1
        self.__prevTimeInactive = theTime
      if (self.__counter == inactivity):
        self.__counter = 0 # reset counter
        return True # not active
    else:
      if (theTime - self.__prevTimeActive > self.__oneSec):
        self.__prevTimeActive = theTime
        pass


  """
  send "walk" command to MCU:
  -> MCU will respond with displaying "Go WALK!" on OLED.

  """
  def cmd_goWalk(self):
    self.__comms.send_message("walk")


  """
  send "Good" command to MCU:
  -> MCU will respond with displaying "Good!" on OLED.

  """
  def cmd_good(self):
    self.__comms.send_message("Good")


  """
  send "sleep" command to MCU:
  -> MCU will respond with displaying "sleep" on OLED.
  -> close communication

  """
  def finish(self):
    self.__comms.send_message("sleep")
    self.__comms.close()
