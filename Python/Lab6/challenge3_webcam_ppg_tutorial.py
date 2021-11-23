import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# using laptop webcam:
cap = cv2.VideoCapture(2)
# using external webcam:
# cap = cv2.VideoCapture(0)

timestamps = []
ppg = []

while(True):
  _, frame = cap.read() 
  new_sample = frame.mean(axis=0).mean(axis=0)

  time_nanosec = time.time_ns()
  timestamps.append(time_nanosec/(10**9))
  
  new_sample = new_sample[2] # bcoz opencv is BGR, instead of RGB
  print(new_sample)
  ppg.append(new_sample) # append new_sample to ppg
  cv2.imshow('Input', frame)
  c = cv2.waitKey(1)
  if c == 27:
    break

cap.release()
cv2.destroyAllWindows()
fig = plt.figure()
ax = plt.axes()

p = ppg[10:]
t = np.array(timestamps[10:]) # so we can easily subtract the first time

t = t - t[0]
ax.set_xlabel("time(s)")
ax.set_ylabel("Red Channel Value")

ax.plot(t, p)
plt.show()

