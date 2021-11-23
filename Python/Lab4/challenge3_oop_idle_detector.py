from ECE16Lib.IdleDetector import IdleDetector
from time import time

if __name__ == "__main__":

  num_samples = 250
  refresh_time = 0.1

  setLowerBound = 1951
  setUpperBound = 1955
  inactivity = 5

  # init default constructor
  amIdle = IdleDetector(num_samples, refresh_time, "/dev/ttyUSB0", 115200) 

  try:
    while(True):
      message = amIdle.getData()
      # retrive data.
      if (message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
          # extract the data, only get the timestamp, ax, ay, az.
        except ValueError:
          continue

        amIdle.updateData(m1, m2, m3, m4)
        # update the data to the circular list.
        current_time = time()
        # get current time to handle timed events

        if (amIdle.enoughTime(current_time) == True): 
          # if enough time elapsed to begin plotting
          amIdle.beginPlotting() # begin plotting
          if (amIdle.isIdle(current_time, setLowerBound, setUpperBound, inactivity) == True):
            # if idle, send command to MCU
            amIdle.cmd_goWalk()
          else:
            amIdle.cmd_good()
            # if not idle, send command to MCU too.

  except(Exception, KeyboardInterrupt) as e:
    print(e)   
  finally:
    amIdle.finish()

