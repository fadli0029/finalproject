# ECE16 Lab 5 Report :writing_hand:
## Prepared by: Muhammad Fadli Alim Arsani
## Student ID: A16468481
## Date: 10/31/2021

### Lab 5 Objective :pushpin:  

The ultimate goal for this challenge is to build upon our previous project in Lab 4, but instead now with better accuracy by applying __Digital Signal Processing__ on our Accelerometer Data. We also make use of our OOP knowledge by building new modules for our `ECE16lib` library.  

### Tutorials :memo:

<ins>__Tutorial 1: Offline Data Analysis__</ins>  

In this tutorial, we learned how to read and write to a file, particularly a `.csv` file, and doing a little bit of analysis using DSP on the data stored in the file.  

We can easily create a `.csv` file using the `','` delimeter, with the following command `np.savetxt(filename, data, delimeter=",")`. And to load this data to a variable, let's call it `my_data` we can do the following command: `my_data = np.genfromtxt(filename, delimeter=",")`.  

Now, we can analyze this `.csv` file using the DSP methods we build (or "will build" in the next tutorial).  

What we did in this tutorial is creating a method call `collect_samples()` to collect data, and then return it in the form of `ndarray`. The method's return value is this data itself.  

Then, as shown in the beginning of this tutorial, we create a `.csv` file by first calling out `collect_samples()` method, assign it to, for example, a variable called `data`, then call: `save_data(filename, data)` and `load_data()`, which is nothing but our user-defined functions, which calls the `np.savetxt()` and `np.genfromtxt()` respectively.  

Then we can just do a bunch of slicings on this data, for example for the `ax` data, we can do: `ax = data[:,1]`, then proceed with doing our DSP on these data.  

<ins>__Tutorial 2: Digital Signal Processing (DSP)__</ins>  

This is a pretty long tutorial, but very dense in terms of its content regarding DSP and how to implement them in Python. This tutorial introduces mainly 8 DSP techniques:  

- L1-Norm
- Moving Average
- Detrending
- Gradients
- Power Spectral Density
- Low-pass Filter
- High-pass Filter

Then, since we are interested in detecting spikes (due to walking/jumping), logically the kind of signal post-processing we'd do is __finding the peaks__ and __counting them__, which is what we did in this tutorial.  

Next, we created a DSP module to ease our workflow in working with our sensor data. This moudle, `DSP.py` contains all the methods which implemented the DSP techniques, as listed previously. Now, we can just import this file from our `ECE16lib`, and start analyzing our data.  

<ins>__Tutorial 3: Pedometer Class__</ins>  

In this Tutorial, we made a Pedometer class. The goal is to make our programming and hacking experience whilst doing this lab more manageable and smooth. The constructor is essentially initializing all the necessary attributes, like our Circular List, filters, and etc.  

Then we have the `add()` method whcih applies `l1_norm` to all three axes, and add it to `l1`. Then we have the `process()` method; this is where all the DSP is happening. Finally, we have the `reset()` method to clear the data. This tutorial tested the class both online and offline and they worked incredibly well!  

### Challenges :desktop_computer:

<ins>__Challenge 1: Complete Pedometer__</ins>  

This challenge requires me to implement an algorithm, utilizing our __DSP__ module and __Pedometer class__, that counts steps while walking. My algorithm is pretty straightforward and simple, and I didn't need to make too many changes, as I am satisfied with the performance :)  

First I needed to change the threshold:  

```python
__thresh_low = 60
__thresh_high = 300
```

Then, I use the `moving_averag` and `detrend()` methods, to accurately detect when there is a step from the plots. The following is how it is implemented:  

```python
def process(self):
  # Grab only the new samples into a NumPy array
  x = np.array(self.__l1[ -self.__new_samples: ])

  # Filter the signal (detrend, LP, MA, etc…)
  x = filt.moving_average(x, 20)
  x = filt.detrend(x)

  # Store the filtered data
  self.__filtered.add(x.tolist())

  # Count the number of peaks in the filtered data
  count, peaks = filt.count_peaks(x, self.__thresh_low, self.__thresh_high)

  # Update the step count and reset the new sample count
  self.__steps += count
  self.__new_samples = 0

  # Return the step count, peak locations, and filtered data
  return self.__steps, peaks, np.array(self.__filtered)
```

Gif of my housemate attempting to walk as naturally as he could, while I gather all my energy within myself to get a perfect gif for this lab:  

![walking](https://media.giphy.com/media/VUBykJsTXxbftesglk/giphy.gif)  

`Note`: The gif is obviouly to short to see my friend walking 13 steps, so [here](https://youtube.com/shorts/G0ULXH5WHUY?feature=share) is a link to a short on YouTube.  

And this is my __Teammate's GIF's__:  

![gideon](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab5/images/teammateGideonChal1.gif)  

<ins>__Challenge 2: Jumping Jack Counter__</ins>  

In this Challenge, we were tasked to create a jumping jack counter, which only displays count on the OLED when a button is pressed. I can divide this challenge in two parts:  

1. establishing the button trigger mechanism
2. the algorithm to count the jumping jacks  

As for (1), I reused the algorithm I implemented for Lab 2, `Challenge2Stopwatch`. I needed to catch the button state and remember the last state, and that algorithm is perfect, as shown below:  
```cpp
currentState = !digitalRead(buttonPin);
if (currentState != lastButtonState) { // button is pressed
  if (currentState == HIGH) {
    processingData = true;
    if (oldStatus == true) {
      processingData = false;
    }
    if (oldStatus == false) {
      processingData = true;
    }
  }
}
lastButtonState = currentState;

if (processingData == true) {
  // button is pressed
  sending = false;
  Serial.print('m');
  // tell python program to process the data
  // and show jump counts
}

else if (processingData == false) {
  // button is not pressed, keep taking data
  sending = true;
}
oldStatus = processingData;
```

I added the line `Serial.print('m');`, this is to enable my Python program catch the changes in the Button state if it occurs, as shown below:  

```python
...
while(True):
  ...
  anotherMsg = comms.rec_msg()
  ...
  ...
  ...
  if (str(anotherMsg) == "b'm'"):
    comms.send_message(str(theSteps))
    print("Step count: {:d}".format(theSteps))
...
```

I added the `rec_msg()` method in our `Communication.py` module, to enable me catch characters in the buffer. This method is implemented as follows:  

```python
def rec_msg(self):
  return self.__ser.read()
```

As for (2), the algorithm from challenge1 didn't change much, except that I tuned the threshold until I get a pretty accurate one. I added a `setter` in the Pedometer module:  

```python
def threshSetter(self, t_low, t_high):
  self.__thresh_low = t_low
  self.__thresh_high = t_high
```

This way, it is easier for me to tune the sensitivity of where the `process()` method will decide to detect peaks. I realize the peak is more "aggressive" and huge when jumping, hence why the big value of the threshold. I am to make future improvements in terms of DSP, to make this counter more accurate :)  

As of now, the following is what has been set up for the counter:  

```python
ped.threshSetter(75, 1500) # to set the threshold
...
...
...
steps, peaks, filtered = ped.process()
theSteps = steps

plt.cla()
plt.plot(filtered)
plt.title("Step Count: %d" % steps)
plt.show(block=False)
plt.pause(0.001)
```

As can be seen, I still implement the plotting; this is so I can keep track of how my jumps affect the peaks.  

GIF of my attemping jumping jacks (embarassing):  

![jumpingJacks](https://media.giphy.com/media/HNdU5Tv8UUMJb0RVXo/giphy.gif)  

`Note:` As we can see here, only when the button pressed the count is printed on the screen, and hence displayed on the OLED. And the plotting is paused when this happened, because we only want to __collect data__ when button is not pressed (plot ongoing), and __process data__ when button is presson (plot stopped, and analyzed).  

