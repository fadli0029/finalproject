# ECE16 Lab 4 Report :writing_hand:
## Prepared by: Muhammad Fadli Alim Arsani
## Student ID: A16468481
## Date: 10/24/2021

### Lab 4 Objective :pushpin:  

The objective of this lab is to teach students OOP in Python, and how can we leverage the powerful packages in Python like `matplotlib`, `numpy`, and even our own package, `ECE16Lib`. This lab also put an emphasis on using `matplotlib` to plot real-world data, particularly the data from out accelerometer.  

### Tutorials :memo:  

<ins>__Tutorial 1: Object-Oriented Python__</ins>  

:thought_balloon: <ins>Questions from the tutorial:</ins>  

> Q1. What is the output of the `print(scout)` statement? Explain it.  

The output was: `<__main__.Dog object at 0x7f1c66de2fd0>`  

This `__main__` is the name of the module which our `Dog` class belongs to, and `main` is the python interpreter. Then the `Dog` following `__main__` is the name of our class, and the `0x7f1c66de2fd0` is the memory address.

> Q2. What would happen if we were to change the second print statement to print out the breed with `print(scout.__breed)`? Explain this result. What does this mean in terms of the Dog class and Object-Oriented Programming?  

It gives us an error: `AttributeError: 'Dog' object has no attribute '__breed'`  

This just means that we are not allowed to access encapsulated objects, unless we make getter and setter methods to retrieve them. This is a common practice in OOP to encapsulate objects. Because sometimes we want to 'protect' the object from being modified or altered by user unintentionally.  

> Q3. At the end of the Python file, add a second Dog object named skippy and make scout and skippy buddies. Then use scout to print out skippy’s description.  

See `tutorial_oop_dog.py`.  

In this tutorial, we learned OOP in Python, with emphasis on concepts like encapsulation, private methods/variables, and etc.  

We also built our own package, `ECE16Lib` to be used in future labs!  

<ins>__Tutorial 2: Python Plotting__</ins>  

This tutorial is regarding plotting in Python, particularly utilizing the `matplotlib` library. We learned basic methods like `plot()`, `show()`, `subplot()`, and etc. We also used the `Numpy` library for the tutorial.  

The `subplot()` allows us to have multiple plots in one figure, which is useful if we don't want more than one figure.  

Using this tool, we plot data from the Accelerometer, and observe how `matplotlib` can be used in plotting real-world data.  

<ins>__Tutorial 3: Live Plotting__</ins>  

In the last tutorial, although `matplotlib` is powerful enough to plot data, we would need to be able to plot live data for our wearable watch, like serial plot in the Ardunio IDE; tutorial 3 teaches how to achieve this.  

We implement this by making what's called a __Circular List__. It is a data structure whose data is implemented under FIFO structure (first in first out). We shift out accelerometer data for every new data we added to our circular list. This allows us to keep taking data and plot it.  

This Data Structure is implemented as one of our module in our `ECE16Lib` package.

### Challenges :desktop_computer:

<ins>__Challenge 1: Sensing the Sensor__</ins>  

In challenge 1, we use `numpy` to implement various transformations on our data, namely `average_x`, `delta_x`, `L2-Norm`, `L1-Norm`, and another transformation of my choice, `x**2`, which is essentially just the square of the x-axix values, which I think would give me a more sensitive yet flexible axis data.  

To apply live plotting in this challenge, we use the `CircularList` library from our `ECE16Lib` package, and constantly updating out axis list.  

The following are gifs of the transformations implemented in this challenge:  

<img src="https://media.giphy.com/media/uXzkedbx6QwtMH2pP2/giphy.gif" width="900" height="500"/>  

<img src="https://media.giphy.com/media/8B9oxN1X07dGhQweHA/giphy.gif" width="900" height="500"/>  

<img src="https://media.giphy.com/media/wrvtsGywqG17eTQPts/giphy.gif" width="900" height="500"/>  

<!-- 
![chal1p1](https://media.giphy.com/media/uXzkedbx6QwtMH2pP2/giphy.gif)  

![chal1p2](https://media.giphy.com/media/8B9oxN1X07dGhQweHA/giphy.gif)  

![chal1p3](https://media.giphy.com/media/wrvtsGywqG17eTQPts/giphy.gif)  
-->  

<ins>__Challenge 2: Idle Detector__</ins>  

As can be seen in the image below, when the user is inactive we can see a "clean" constant `average_x` value.  

![image2](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab4/images/inactiveState2.jpg)  

If we look closely, during an inactive state, it fluctuates between `1951` and `1954` (it does went over/lower than those values, but after observing the plot repeatedly, i've decided to take that range)  

![image1](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab4/images/inactiveState.png)  

So the following is my approach:  
1. Extract the most recent value from the `average_x` circular list, by doing:  
```python
theplot = plt.plot(average_x, color='g')
determ = theplot[-1].get_data()
theInput = ((determ)[-1])[-1]
```

2. Then, I can make a conditional statement, and use a timed event approach to send the desired message on the OLED:  
```python
if (theInput >= 1951 and theInput <= 1954):
	if (current_time - previous_time2 > one_sec):
		counter += 1;
		# counter will be incremented by 1 every one second
		previous_time2 = current_time
	if (counter == 5):
		comms.send_message("walk")
		counter = 0
else:
	if (current_time - previous_time3 > one_sec):
		comms.send_message("Good")
		previous_time3 = current_time
```

3. Next, on the `Challenge2IdleDetector` side I make an FSM as shown below:  

![fsm_image](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab4/images/fsm.jpg)  

I reuse the `timeElapsed.ino` tab that I made in Lab 3 (`ChallengeGestureDetection`), to take care of the timed events like buzzing the motor. The following is my implementation of the FSM in `Challenge2IdleDetector.ino`:  

```cpp
switch (fsm_state) {
  case 0: // neutral (i.e: state checking)
    if (oneSecPassed(currentMillis) == true) {
      digitalWrite(buzzerPin, LOW);
    }
    if (command == "walk") {
      fsm_state = 1;
    }
    else if (command == "Good") {
      fsm_state = 2;
    }
    break;

  case 1: // inactive state
    writeDisplay("Go WALK!", 0, true);
    digitalWrite(buzzerPin, HIGH);
    if (oneSecPassed(currentMillis) == true) {
      counter++;
    }
    if (counter == 1) {
      counter = 0;   // reset counter
      digitalWrite(buzzerPin, LOW);
      fsm_state = 0; // go to case 0, to check state again
    }
    break;

  case 2: // active state
    writeDisplay("Good!", 0, true);
    fsm_state = 0; // go to case 0, to check state again
    break;
}
sending = true;
```

__Idle Detector in Action!__  

![chal2gif](https://media.giphy.com/media/oFup8MLU0kRJ5kJRQ4/giphy.gif)  

*(notice how the Breadboard moved a bit as soon as the "Go Walk!" message popped up, that's the buzzer functioning!)*  

<ins>__Challenge 3: OOP Idle Detector__</ins>  

A detail of what each methods does can also be seen in `IdleDetector.py` under the respective methods' docstrings.  

The following are the methods I implemented for the library:  

1.
```python
__init__(self, num_samples=None, refresh_time=None, serial_name=None, baud_rate=None)
```

The default constructor setup the __number of samples, refresh time, serial name, baud rate, circular list objects, and communication__.  

2.
```python
__setupCircularList(self, samplesArg)
```

Setup the circular list and initialize `ax`, `ay`, `az`, timestamp, `average_x` with the given `samplesArg`.

3.
```python
__setupCommunication(self, serialName, baudRate)
```

initalize `__comms` by calling the constructor `Communication(serialName, baudRate)`. Then call the `clear()` method, and finally call `send_message("wearable")`.

4.
```python
__getAvg(self, alist)
```

returns the average of `ax` values.

5.
```python
getData(self)
```

call `self.__comms.receive_message()` and assign it to `theMessage`. Then returns `theMessage`.

6.
```python
updateData(self, m1__, m2__, m3__, m4__)
```

call `add()` on each of the ciruclar lists (`timestamp`, `ax`, `ay`, `az`), and on `average_x` by calling `self.__getAvg(self.ax)`.

7.
```python
enoughTime(self, theTime)
```

takes in `theTime` as a parameter which is `time()` and checks if enough time has elapsed. It returns `True` if enough time has elpased based on the specified `refreshTime`.

8.
```python
beginPlotting(self)
```

start plotting by calling the methods from `matplotlib`, extract most recent value of `average_x` plot, print it on the terminal (for my convenience).

9.
```python
isIdle(self, theTime, lowerBound, upperBound, inactivity=5)
```

checks if a user is active, depending on the specified inactivity value (5 seconds as default). Alter lowerBound and upperBound to tune sensitivity. It returns boolean `True` if a person is idle.

10.
```python
cmd_goWalk(self)
```

sends __"walk"__ to the MCU.

11.
```python
cmd_good(self)
```

sends __"Good"__ to the MCU.

12.
```python
finish(self)
```

call `self.__comms.send_message("sleep")` and `self.__comms.close()` to end communication.  

__IdleDetector Library in Action!__  

<img src="https://media.giphy.com/media/u8geEDn8Qbn5UUsyGj/giphy.gif" width="900" height="500"/>
<!-- ![chal3](https://media.giphy.com/media/u8geEDn8Qbn5UUsyGj/giphy.gif)  -->

![chal3p2](https://media.giphy.com/media/oFup8MLU0kRJ5kJRQ4/giphy.gif)  

*(notice how the Breadboard moved a bit as soon as the "Go Walk!" message popped up, that's the buzzer functioning!)*
