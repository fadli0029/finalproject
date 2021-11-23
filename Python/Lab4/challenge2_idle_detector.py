from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time

# Helper functions: 
def getAvg(alist):
  return (sum(alist)/len(alist))

# main:
if __name__ == "__main__":
  num_samples = 250               # 5 seconds of data @ 50Hz
  refresh_time = 0.1              # update the plot every 0.1s (10 FPS)
  one_sec = 1
  counter = 0

  timestamp = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)
  average_x = CircularList([], num_samples)

  comms = Communication("/dev/ttyUSB0", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    previous_time = 0
    previous_time2 = 0  # tracking inactiviy
    previous_time3 = 0  # tracking activity
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
          # getting accelerometer values
        except ValueError:        
          continue
          # if corrupted data, skip the sample

        # add the new values to the circular lists
        timestamp.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))

        # I will only need average_x for my implementation:
        average_x.add(getAvg(ax))

        current_time = time()
        if (current_time - previous_time > refresh_time):
          plt.clf()

          theplot = plt.plot(average_x, color='g')
          determ = theplot[-1].get_data()
          theInput = ((determ)[-1])[-1]
          print(theInput) # just for me to see data
          if (theInput >= 1951 and theInput <= 1955):
            # inactive, check 5 secs passed here
            if (current_time - previous_time2 > one_sec):
              counter += 1
              previous_time2 = current_time
            if (counter == 5):
              # 5 seconds passed, send message
              comms.send_message("walk")
              # reset counter
              counter = 0

          else:
            if (current_time - previous_time3 > one_sec):
              # one sec has passed of person being active
              comms.send_message("Good")
              previous_time3 = current_time

          previous_time = current_time

  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()
