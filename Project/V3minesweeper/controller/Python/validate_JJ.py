'''
    msg      -> timestamp & accelerometer values
    no_of_jj -> number of jumping jacks to validate
    samples  -> number of samplings
             -> default: 250 (5 seconds of data @ 50hz)
    r_time   -> refresh time of doing DSP for jumping jacks
    fs       -> freq of pedometer, required to instantiate pedometer 
             -> default: 50
    lt       -> lower threshold to count peaks
             -> default: 100
    ut       -> upper threshold to count peaks
             -> default: 850
'''
def validateJumpingJacksCount(self, msg, no_of_jj, \
                              samples=250, r_time=0.1, fs=50, \
                              lt=100, ut=850):

    ped = Pedometer(samples, fs, [])
    ped.threshSetter(lt, ut)   # to set the threshold

    try:
      theSteps = 0
      previous_time = 0
      while(True):
        # message = comms.receive_message()
        if(msg != None):
          try:
            (m1, m2, m3, m4) = msg.split(',')
          except ValueError:        # if corrupted data, skip the sample
            continue

          # add the new values to the circular lists
          ped.add(int(m2),int(m3),int(m4))


          # if enough time has elapsed, clear the axis, and plot
          current_time = time()
          if (current_time - previous_time > refresh_time):
            previous_time = current_time

            steps, peaks, filtered = ped.process()
            theSteps = steps
            #print("theSteps: "+str(theSteps))
            if (theSteps == no_of_jj):
                return True

