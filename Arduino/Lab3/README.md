# ECE16 Lab 3 Report :writing_hand:
## Prepared by: Muhammad Fadli Alim Arsani
## Student ID: A16468481
## Date: 10/17/2021

### Lab 3 Objective :pushpin:  

I'm gonna start by saying, this lab is so __FUN__! I believe one of the main aims is to develop the skills of making software and hardware interact, utilizing real world data, within students. And this is ultimately the final goal of this class. The challenges are, as the name implies, challenging. They, again, test on students' understandings in handling multiple timed events, working with python libraries, and re-using codes in such a way that is efficient and beneficial for both the user and programmer.  

</br>

### Tutorials :memo: 

<ins>__Tutorial 1: I2C Communication & OLED Display__</ins>  

In this tutorial, we learned about I2C communication and OLED display.  

I2C is a communication protocol, very common in almost any microcontrollers. As mentioned in the lecture video, I2C allows a single "mster" IC (integrated circuit), in this case the MCU, to communicate  with multiple "slave" ICs, for example sensors, actuators and etc.  

There are many reasons why we would want to utilize this communication protocol; One of them is because it has a clock, so we won't have to keep an eye on things like baud rate and etc. We can also literally connect with multiple devices with only two wires, SDA (for data)  and SCL (for clock).  

OLED stands for Organic Light Emitting Diode. The OLED communicates via I2C, with 2 data lines as mentioned before - SDA and SCL. In this Lab, we are making use of the `U8g2` to simplify things and make everything more efficient when working with the OLED. We also made a very useful `Display.ino` file which we made full use of throughout the entire lab!  

<ins>__Tutorial 2: Analog Input (Accelerometer)__</ins>  

In this tutorial, we learned how to read data from and analog input, and we worked with Accelerometer (ADXL335) - a device that measures acceleration in the X, Y, and Z direction. 

We first need to understand what it means to measure __"analog"__ data. Analog data is a continuous type of data. Unlike digital data, which are __discrete signals__ with only 0's and 1's, analog data can be 0.2, 0.3, 6.2, 3.4, basically any __continuous signals__.

When we take analog inputs from a sensor, let's say temperature sensor, the temperature is that analog data, which is measured in terms of voltage. Then, we process this analog data using what is called __ADC__ (Analog-to-Digital Converter). This ADC will take input anywhere between 0V to its reference voltage, either 3.3V or 5V. Then it outputs the corresponding values representing these analog data, i.e: the voltages. Hence, a 10-bit ADC will produce values from 0 to 1023, with code 0 being 0V and code 1023 being the highest voltage, 3.3V or 5V.

There are built-in functions in the Arduino IDE which allow us to work with Analog Signals. For example, to read the analog signal from the accelerometer, we use `analogRead()`. Similar to working with Digital data, we need to specify the pins, but for analog pins, we declare them with the `A` prefix before the pin number; for example, analog pin 3 would be: `A3`.

Another cool thing is we can use Serial plotter in the Arduino IDE to look at the changes in the analog values read by our accelerometer.

Then, we also learned how to organize our codes (reusable functions) into tabs (other `.ino` files) which we can easily reuse for other projects.  

<ins>__Tutorial 3: Analog Ouput (PWM)__</ins>  

This tutorial introduced the concept of __PWM__, __Pulse Width Modulation__, a very commonly used technique, where we toggle the GPIO Pins at a certain frequency. There are essentialy 3 important terminologies in understanding PWM -  __Duty Cycle__, __PWM Frequency__, and __Bit Resolution__:  

- <ins>Duty Cycle</ins>: 
  - We can think of duty cycle as the ratio of how long is our device on to the total time of its on and off. For example, a 50% duty cycle means the device is on (HIGH) 50%  of the time, and off (LOW) 50% off the time, and so this also affect the average voltage, making the vcc now is 0.5vcc.

- <ins>PWM Frequency</ins>:
  - How many times we do this toggling is called the PWM Frequency.

- <ins>Bit Resolution</ins>:
  - I think of this as the range of plotting the analog values. For example, if we have an 8-bit resolution PWM, that means we can produce 256 __distinct__ output values (from 0, 1/256, 2/256, 3/256, ...). So the higher the bit, the better the outcome is.

Like working with Analog and Digital data, there are also functions built into the Arduino IDE to help us set up PWM, and some of them are:  

- `ledcSetup()`: use this to setup the PWM channel with the `frequency` and `resolution` we want. The resolution depends on the microprocessor we are using.

- `ledcAttachPin()`: this allows us to attach the physical GPIO pin to the PWM channel. 

- `ledcWrite()`: this sets the duty cycle for the PWM channel. In the tutorial, there's a really good way to think about this function - "You can think of `ledcWrite()` as an analog output function with the duty cycle resolution as possible values". This means, for an 8-bit resolution, if we want a 50% duty cycle, we'd do `ledcWrite(channel_number, 127)` because 2^8 is 255 if we start with 0, and half of that (50%) is 127.  


<ins>__Tutorial 4: Sampling__</ins>  

Tutorial 4 is probably the one of the most important tutorial in this lab, besides the State Machine tutorial video. Let's first understand what sampling really means:  

When we take data of temperature around us, we are __sampling__ data, in this case that data is the temperature. How much we sample that data is called the __sampling rate__. For example, I could sample that data every 1 week, but would that be a realiable data? No. But if I sample it every hour, or every minute, maybe that would be a more reliable data. Notice that this temperature data we are talking about is considered analog data, its values are continuous. And of course, how much we sample matters. By the __Nyquist Sampling Theorem__:  

> we should sample an analog signal __at least 2x faster than the fastest changing portion of the signal (but in practice, sampling around 4x is "safer")__. Insufficient sampling can caused aliasing.  

And as Prof. Ramsin says in his video tutorial:  
> High bit ADC and more frequent sampling will give you a more accurate representation of your analog signals.

> -> Ramsin, Video Tutorial: Analog Signals (13:06)  

<!-- should i include any relevant images? -->

<ins>__Tutorial 5: Python Serial & BT Communication__</ins>  

In this tutorial, we learned how to communicate with the MCU using Python via the Python library called `PySerial`. Why would we want to accomplish this when we have successfully used Serial Monitor and all that before? Because with Python Serial Communication, we can do so so many more advanced things; it's Python, it's powerful.  

We needed to specifiy serial name and baud rate always, and made some functions for later use as they are very common and will be used extensively. These functions are `setup()`, to setup serial connection, and `close()` to close the serial connection. We also made the `send_message()` and `receive_message()` methods to send and receive message with the MCU.  

Then we set up the Arduino sketch for bluetooth communication. This way, we can safely unplug the cable from the ESP32 and information to the MCU through our Python script. Very cool!!  

</br>

### EXTRAS :arrow_right: Understanding Finite State Machines (FSM)  

Many things we did in the previous labs actually make use of FSM approach without us realising it. To begin defining it, I'd like to reference a definition given by [this website](https://bit.ly/3mODj2h) because it's so concise yet capture the concepts behind the implementations of an FSM.  

> A state machine is not a machine in the same way that a lawn mower or a typewriter is a machine. It is more of an abstract concept or system that helps you systematically design and implement the logic behaviour of an embedded system. In fact, the state machine concept is so abstract that you can use it to much more than just embedded system logic

<ins>What it's all about.</ins>  

*The big idea:* 
> only a single state can be activated at any given time, so the machine must transition from one state to another in order to perform different actions.

*What we need to create a state machine:*

- states
- inputs
- outputs
- triggers

<ins>Why use it.</ins>
- Useful for non-blocking code, making things happen at once in embedded programming.
- Flexible.
- Help us move from abstraction to code implementation.
- Gives us the big picture of the goals we want to achieve in our program.

Consider this `blink.ino` example:

```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}
   
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
```

Of course, it is unnecessary to take an FSM approach for this example, but for demonstration purposes, this will be perfect. Consider the same application but using an FSM approach:  


```cpp
void blink(bool reset = false) {
	const uint32_t LED_DELAY = 1000;
	static enum { LED_DELAY, WAIT_DELAY } state = LED_TOGGLE;
	// we define states as an enumerated type.
	// this makes it so much easier to read and follow the code.
	// also because we usually number the states in FSM approach,
	// using enum type does that for us.
	// this avoids renumbering all states when we add or delete states.
	static uint32_t timeLastTransition = 0;

	if (reset) {
		state = LED_TOGGLE;
		digitalWrite(LED_BUILTIN, LOW);
	}

	switch (state)
	{
		case LED_TOGGLE: // toggle the LED
			digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
			timeLastTransition = millis();
			state = WAIT_DELAY;
			break;
		case WAIT_DELAY:
			if (millis() - timeLastTransition >= LED_DELAY) {
				state = LED_TOGGLE;
			}
			break;
		default:  // for Safety purposes
			state = LED_TOGGLE;
			break;
	}
}
```

This gives us many advantages: 
- more readable.
- easily maintainable.
- it takes a boolean parameter which allows the code to __reset the FSM to a known state__.
- the `default` state acts as a defensive measure to make sure that any undefined or corrupted state does not stop the FSM. Things like this can happen during events like memory becomes corrupted for some reason.

<ins>Sources:</ins>  

[Ramsin Khoshabeh - Finite State Machines](https://www.youtube.com/watch?v=wXZsapI1hPg)  

[Another good YouTube Video on FSM](https://www.youtube.com/watch?v=v8KXa5uRavg)  

Some other good links for extra readings:  

[Mealy vs. Moore machine](https://www.youtube.com/watch?v=S352lyPZP00)  

[by arduinoplusplus.com](https://arduinoplusplus.wordpress.com/2019/07/06/finite-state-machine-programming-basics-part-1/)  

[by hackster.io](https://www.hackster.io/tolentinocotesta/let-s-learn-how-to-use-finite-state-machine-with-arduino-c524ac)  

[by iotsharing.com](http://www.iotsharing.com/2017/05/how-to-apply-finite-state-machine-to-arduino-esp32-avoid-blocking.html)  

[by espruino.com](https://www.espruino.com/StateMachine)  

[by norweigiancreations.com](https://www.norwegiancreations.com/2017/03/state-machines-and-arduino-implementation/)  

[by teachmemicro.com](https://www.teachmemicro.com/arduino-state-machine-tutorial/)  

[by instructables.com](https://www.instructables.com/Finite-State-Machine-on-an-Arduino/)  

[by arduino forum](https://forum.arduino.cc/t/state-machines/580593)  



</br>

### Challenges :desktop_computer:

<ins>__Challenge 1: Gesture Detection__</ins>  

Challenge 1 is about working with analog input device, in this case the Accelerometer. Not just that, this challenge also made use of the Sampling.ino file and the concepts we learned in Tutorial 4 regarding sampling and how it works.  

We were required to analyze data from the Accelerometer when there is a tap on it; this can be accomplished by analyzing the Serial Plot and the Serial monitor, oberseving changes/spikes/drops when there is a tap.  

My approach was collecting as much information as I could from the Serial Plot and Serial Monitor, noting all the `ax`, `ay`, `az`, values, and how they change when there is a tap. Then with a conditional statement, I only increase the `numTaps` value when the value sent by the Accelerometer on all three axes exceeded the threshold I set according to my observation. I also added a 40ms delay to remove the shock affect after tapping.  

![GestureDetectionGIF](https://bit.ly/2YVWK10)  

<ins>__Challenge 2: Gesture-Controlled Watch__</ins>  

Challenge 2 is probably the most important one in this Lab, as it tests on students understanding in Finite State Machines (FSM). This concept is very crucial in solving problems.  

We were required to make a finite state machine diagram prior to coding the solution, as this helped to really see the bigger picture of the challenge, and how to go about solving it. Below is my Finite State Machine Diagram:  

![FSM diagram](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Arduino/Lab3/images/FiniteStateMachine.jpg)
I could make another state after the buzzer is activated, and go back to reset mode, awaiting for a new tap. But I didn't as it is not compulsory and I feel satisfied with my buzzer buzzing noisily when it reached 0, i could use it as my wake-up alarm (just kidding hehe).  

![Challenge2GIF](https://media.giphy.com/media/rVrdZ4I1RifSSGvBXN/giphy-downsized.gif)

`NOTE:` __A gif is too short to show full functionality, so,__ click [here](https://youtube.com/shorts/Me1XXvLT8Xk?feature=share) for a 12 seconds video of buzzer and everything else working.  

<ins>__Challenge 3: Wireless Weather Watch__</ins>  

This challenge is SO FUNNNN!! In this challenge, we use the data from Open Weather Map API, to retrieve the current temperature at our choosen location. And then I used the `datetime` module to retrieve current date and time, and I refresh it both in the arduino sketch and the `.py` file every 1 second.  

The following is my approach:  

In `challenge_weather_watch.py`:  

```python
owm = OWM('dd25a8ed48b2b2b12d7a71c45e5ca1eb').weather_manager()
fade = owm.weather_at_place('san diego,ca,us')
weather = fade.weather
final_output = weather.detailed_status + ' ' + str(weather.temperature('celsius')['temp_max'])
```
Here, I get the detailed status of the weather in san diego by calling `weather.detailed_status`, then i concatenated it with `weather.temperature('celsius')['temp_max']` after converting the temperature into a string using the `str()` method.  

Then, in my `main()` method:  

```python
def main():
    ser = setup("/dev/rfcomm0", 115200)
    theTime = datetime.datetime.now().strftime("%H:%M:%S")
    theDate = datetime.date.today()
    outputDate = theDate.strftime("%b-%d-%Y")
    place = "San Diego, CA"
    send_message(ser, theTime)
    send_message(ser, final_output)
    send_message(ser, outputDate)
    send_message(ser, place)
    time.sleep(1)
    close(ser)
```

Here, I just call the `setup()` method, specify the bluetooth name of my ESP32, and baudrate. Then I use the `datetime` module to get the current time and today's date, and output it as a Month-Day-Year format. Then I just use a regular string for the place. Finally, I call the `send_message()` method and pass in the strings, to be received by the MCU. Also, I call the `time.sleep(1)` method to give me a 1s period to see the output on the OLED.  

In the `ChallengeWeatherWatch.ino` sketch:  

```cpp
void loop() {
  String message1 = receiveMessage();
  if(message1 != "") {
    writeDisplay(message1.c_str(), row, true);
    sendMessage(message1);
    row++;
    if (row == 4) {
      row = 0;
    }
  }
}
```

I declared a global variable, `row` and increment it everytime I write a Display, but make it 0 once row is 4. This is to allow me print all the information on the OLED in each line.  

![Challenge3Gif](https://media.giphy.com/media/0iqCiBMevg7sIzYnsG/giphy.gif)


