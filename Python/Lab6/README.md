# ECE16 Lab 6 Report :writing_hand:
## Prepared by: Muhammad Fadli Alim Arsani
## Student ID: A16468481
## Date: 11/07/2021

### Lab 6 Objective :pushpin:  

The objective of this lab is to build a reliable heart beat rate monitor, using a photodetector, through our understanding in how PPG works. We built another module for our `ECE16lib`in this lab, the `HRMonitor.py` module, to aid us and smooth our journey in building our "fitbit". We were also introduced to OpenCV, a powerful library mainly for image/video processing, very cool!

### Tutorials :memo:  

<ins>__Tutorial 1: Heuristic Heart Rate Monitor & Evaluation__</ins>  


In this tutorial, we learned about the concept of __Photoplethysmography (PPG)__, and how we can implement it pretty efficiently with a photodetector chip and some nifty python codes!  

The idea of PPG is from __Plethysmography__, which is the scientific measurement of volumetric changes. PPG uses the idea of using light to measure these changes, hence why the name PPG. Here's how it works:  

- Shining a light on a surface, like our skin, causes the some of the light to get absorbed and reflected back.  
- Now what if we know very well the property of the surface like our skin?  
- To put it simply, __the light source emits light to a tissue and the photodetector measures the reflected light from the tissue. The reflected light is proportional to blood volume variations__ ([cool article on this](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6426305/))  

We can technically build a device to achieve this, however engineers like to make people's life easier, including themselves, so we're just gonna grab __photodetector chip__ from Maxim called the __MAX30101__. Not only this chip is awesome for its built-in highly sensitive photon detector, it also communicates via __I2C__ communication protocol, so our OLED can connect to the same pin as this chip, very cool!  

We are using the `MAX3015.h` library, and here are the ideal settings for me:  
```cpp
byte ledBrightness = 0x1F; // Options: 0==Off to 255==50mA (0x1F==50/8mA)
byte sampleAverage = 4;    // Options: 1, 2, 4, 8, 16, 32
byte ledMode = 3;          // Options: 1==R, 2==R+IR, 3==R+G+IR
int sampleRate = 400;      // Options: 50,100,200,400,800,1000,1600,3200
int pulseWidth = 411;      // Options: 69, 118, 215, 411
int adcRange = 16384;      // Options: 2048, 4096, 8192, 16384

// Configure sensor with these settings
photoSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);
```

On the __Python__ side, the way we are receiving the readings from the photodetector is pretty much the same as before with the accelerometer, we just add a new circular list to catch and store the ppg data, and now instead of 4 readings, we're taking 5:  

```python
ppg = CircularList([], num_samples)

...
...
...

  try:
    previous_time = time()
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4, m5) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))
        ppg.add(int(m5))

		...
		...
		...
```
  

:thought_balloon: <ins>Questions from the tutorial:</ins>  

> Q1. Note that you can connect both the heartbeat sensor and your OLED at the same time, both of which use the I2C, SDA, and SCL lines. Why does this work?  
__I2C communication protocol allows more than one I2C peripherals to be connected to a single I2C controller.__

> Q2. Notice the while(1) statement. What happens if the device is not connected? What happens if the error is printed and then you connect the device? Will the code proceed? Try it and describe the behavior.  
__It keeps checking if a device is connected__

> Q3. What would the settings look like if you were to: set the led brightness to 25mA, use only the Red + IR LEDs, sample at 200Hz, and use an ADC range of 8192?  

```cpp
byte ledBrightness = 0x7F; // Options: 0==Off to 255==50mA (0x1F==50/8mA)
byte sampleAverage = 4;    // Options: 1, 2, 4, 8, 16, 32
byte ledMode = 2;          // Options: 1==R, 2==R+IR, 3==R+G+IR
int sampleRate = 200;      // Options: 50,100,200,400,800,1000,1600,3200
int pulseWidth = 411;      // Options: 69, 118, 215, 411
int adcRange = 8192;       // Options: 2048, 4096, 8192, 16384
```

> Q4. What are the units of the pulse width? Would the bigger pulse width result in a more intense or less intense measurement (intensity refers to the intensity of light)? Why?  
__Hz, yes greater pulse width, greater amp.__

> Q5. How many bits are needed for an ADC range of 16384?  
__14 bits__
 
> Q6. What is the peak wavelength of the R, IR, and G LEDs?  
__645nm, 1.45μm, 550nm, respectively__

> Q7. If you want to read the green value, what ledMode do you need to set and what function will you need to use to get the green signal (HINT: it is not getIR()!)?  
__set `ledMode` to 3 and call `.getGreen()`__


<ins>__Tutorial 2: PPG Filtering & Class__</ins>  

In this tutorial, we learn how to filter our PPG data and we made our PPG filtering class.  

Here's how we are filtering the data from the photodetector:  

- Detrend the signal to remove the drift
  - We can just reuse the method from we use for our accelerometer filtering.
- Then to remove the noise, we use moving average.
  - This is to smooth our plotting. And again, we can resuse the method from previous labs.
- To get a very sharp peak, for better calculation later, we take the gradient
  - Again, same technique as in previous lab.
- Then we normalize the signal
  - we're doing this to make analyzing the data easier for us, since we wont be having a sudden spike of heartbeat anyway (hopefully!).
- Then we make a theshold like what we did in lab 5, for peaks counting
  - 0.6 seems pretty good for now : )
- Then, we compute the heart rate:

```python
avg_beat_time = np.mean(np.diff(t[peaks]))
bpm = 60/avg_beat_time
```

Then our `HRMonitor.py` class is basically the implementation of all of this.  

<ins>__Tutorial 3: Data Collection for ML__</ins>  

In this tutorial, we collect our hearbeat data, with a variety of different heartbeat state (chilling | active). We will need this data for our machine learning approach on achieving a heartbeat monitor later. We must make sure the distinct peaks are clear on the plot.  

We will collect the data, and save it in a `.csv` using the `np.savetext(filename, date, delimeter=",")`, and then load it later for analyzing using `np.genfromtxt(filename, delimeter=",")`. Then in our `collect_samples()` method, we collect 500 samples of data at 50hz, then return the data as a single stacked ndarray, easier to save and load it later as a `.csv`  

### Challenges :desktop_computer:

<ins>__Challenge 1: Heuristic Heart Rate Monitor & Evaluation__</ins>  

I didn't do much changes on the algorithm as it worked perfect for me. Regardless, here's the Bland-Altman Plot:  

![chal1PLOT](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab6/images/chal1LAB6.png)  

As can be seen, the estimates have an accuracy of __97%__, awesome!

I also use the `os` module to read through the `a16468481` data directory, get the `.csv` filenames, sort them alphabetically, then loop through them while calling the `process()` method to process the data in each file. This way, I could analyze each datum from everyone in the class efficiently. Here are code snippets of the implementations:  

```python
if __name__ == "__main__":

  # get/list all csv files in the path
  path = './data/a16468481/'
  files = os.listdir(path)
  thefiles = []
  for f in files:
    thefiles.append(f)
    # append all the file names inside thefiles list.
  
  thefiles.sort()
  # sort it alphabetically

  estimates = []
  peaks_count = [12,14,11,16,18,14,15,15,15,15,18,14,16,16,16] # for ground truth
  ground_truth = []
  for item in peaks_count:
    ground_truth.append((item/10)*60)
    # bpm for ground truth
  
  for f in thefiles:
    data = np.genfromtxt(path+f, delimiter=",")
    t = data[:,0]
    t = (t - t[0])/1e3
    ppg = data[:,1]
    count, peaks = process(ppg)
    avg_beat_time = np.mean(np.diff(t[peaks]))
    bpm = 60/avg_beat_time
    estimates.append(bpm)
  
  eval_hr_monitor(ground_truth, estimates)
```

The `process()` method:  

```python
def process(x):
  x = filt.detrend(x, 25)
  x = filt.moving_average(x, 5)
  x = filt.gradient(x)
  x = filt.normalize(x)

  thresh = 0.6
  count, peaks = filt.count_peaks(x, thresh, 1)

  return count, peaks
```

The fill in the blank codes in eval_hr_monitor():  

```python
def eval_hr_monitor(): 
  ...
  ...
  ...

  # Bland-Altman Plot
  avg = [(a+b)/2 for a, b in zip(grnd, est)]
  # take the average between each element of the ground_truth and
  # estimates arrays and you should end up with another array
  
  dif = grnd - est
  # take the difference between ground_truth and estimates
  
  std = np.std(dif)
  # get the standard deviation of the difference (using np.std)
  
  bias = np.mean(dif)
  # get the mean value of the difference
  
  upper_std = bias + 1.96*std
  # the bias plus 1.96 times the std
  
  lower_std = bias - 1.96*std
  # the bias minus 1.96 times the std
  ...
  ...
  ...
```

<ins>__Challenge 2: Online Heart Rate Monitor__</ins>  

In this challenge, we are tasked to make an online Heart Rate Monitor by retrieving data from our photodetector, process them, then send the Heart Beat Rate calculated back to the MCU to be displayed on the OLED.  

On the Arduino side, I added an `else` statment to catch other message besides "wearable" and "sleep" from the python program. When this message is captures, it is the reading of the heart rate processed by the python program; so, I just write this on the OLED display.  

Here's my implementation on the arduino side:  

```cpp
// received BPM measured from python
// print it out on the OLED
else {
  String HR = String(command);
  writeDisplay(HR.c_str(), 2, false, true);
}
```

On the Python side, it's almost identical with the pedometer logic, except that I didn't need to keep track of the accelerometer this time (yeay!). I waited until 500 samples are collected, then only I process the data like so:  

```python
...
...
...
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
...
...
...
```

Here's a working GIF of my Webcam Heart Beat Monitor:  

![HBmonitorCHAL2](https://media.giphy.com/media/4XvdKpdSd9z42squPJ/giphy.gif)  

<ins>__Challenge 3: OpenCV Heart Rate Monitor__</ins>  

In this challenge, we learned how to measure heartbeat using a webcam, with the same concept of PPG, utilising the __OpenCV__ libray.  

The code logic on the Arduino side is similar to of challenge 2, except that I got rid completely of the photodetector chip logic, since I won't be needing it at all:  

```cpp
...
...
void loop() {
  String command = receiveMessage();

  if(command == "sleep") {
    writeDisplay("Sleep", 0, true, false);
  }
  else if(command == "wearable") {
    writeDisplay("Wearable", 0, true, false);
  }

  else if(command == "measuring") {
    writeDisplay("Heart Rate: ", 0, true, false);
    writeDisplay("measuring...", 1, true, false);
  }

  else {
    String HR = String(command);
    writeDisplay(HR.c_str(), 2, false, true);
  }
}
```

On the python side, I wrap the processing-webcam-data logic inside a `while(true)` loop, but every time 500 samples is collected, I process the data, send Heart Rate measured to MCU, call `release()` and `destoryAllWindows()`, then back to top of the loop to call webcam video feed again with `cv2.VideoCapture()`:  

```python
...
...
while(true):
  sample = 0
  cap = cv2.VideoCapture(2)
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
...
...
```

:thought_balloon: <ins>Questions from Challenge 3:</ins>  

> For the tutorial, finish off by taking a plot of your own heartbeat and calculating your own heart rate in BPM by hand. What is the sampling rate in terms of samples/s? How consistent is the sampling rate?  
__peak counts = 14, in 10 seconds, BPM: 84, hmm I'd say it's pretty accurate :)__  

The plot:  

![plottutoOPENCV](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab6/images/challenge3BPMtuto.png)  

Gif made from the OpenCV tutorial:  

![opencv](https://media.giphy.com/media/qX8FYfJWleYSL8P5b8/giphy.gif)  

Here's a working GIF of my Webcam Heart Beat Monitor:  

![opencvwebcamHR](https://media.giphy.com/media/4ws5wDkd8umHgneGOZ/giphy.gif)  

