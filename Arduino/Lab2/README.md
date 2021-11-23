<!--- To insert a new line(break), the fastest way -->
<!--- is to just do (space)(space)(return) -->  

# ECE16 Lab 2 Report
## Prepared by: Muhammad Fadli Alim Arsani
## Student ID: A16468481
## Date: 10/10/2021

### Lab 2 Objective:  

The main objective of Lab 2 is to introduce microcontrollers and how to work and communicate with them. We learned a lot of things regarding embedded system proramming, though we scratched the surface only, we understood how to work with timings when dealing with microcontrollers like ESP32.  

The knowledge learned in this lab is crucial for future labs and ultimately the final project, for microcontrollers as small as ESP32 contain the fundamentals of the Internet of Things applications.  

</br>

### Tutorials

__Tutorial 1: Arduino Setup__  

In this tutotial, we learned how to setup an environment for programming microcontrollers, specifically the __ESP32__, using the __Aruduino IDE__ which allows easier code uploads to the MCU.  

The Arduino IDE is installed [here](https://www.arduino.cc/en/software), and then setup the ESP32 by doing the following:  

- Plug in the ESP 32, and paste the given link in the tutorial in the section "Additional Boards Manager URLs", providing board definitions is important to allow us to work in the Arduino Environment without actually using Arduino.  

- Then, we search for ESP32 in "Boards Manager" and install it.

- Finally, we select our board in: "Tools -> Board -> ESP32 Arduino -> Adafruit ESP32 Feather", and we're good to go!  

*(note: some machines didn't came with the driver needed for the ESP32, so it can be downloaded [here](https://learn.sparkfun.com/tutorials/esp32-thing-plus-hookup-guide#CP2104). Luckily my Linux system came along with it!)*

__Tutorial 2: Digital Communication__  

In this tutorial we learned how to "talk" to microcontrollers by sending digital signals in the form of input and outputs.  

We can communicate with our ESP32 or with any other microcontrollers through their Input and Output pins, or a.k.a GPIO pins. We can set the value of these pins to either __HIGH__ (bool 1) or __LOW__ (bool 0), with `digitalWrite()`.

Then we learned about the two main functions in any Arduino IDE sketch:  

- __Setup__: this is where we "set up" everything, like the name implies, for example giving the pins of the LED's, and indicating if it's an input or output, and etc.

- __Loop__: this is where we implement everything, and as the name implies, this function runs continuously.  

This is how it would look like:  
```arduino
void setup() {

}

void loop() {

}
```
We can also read from a pin, with `digitalRead()`.  

__Tutorial 3: Serial Communication__  

In this tutorial, we learned about the Serial Monitor and some serial communications commands like `Serial.begin,()`, `Serial.println()`, `Serial.available()`, `Serial.read()`, and etc.  

We first need to establish a Serial connection with our MCU to be able to talk to it serially, by calling `Serial.begin()` in the `void setup()` function. This function initiate the sending and receiving of serial information at the specified communication speed we passed into the parameter of the function, for example if it's 9600 baud rate, then: `Serial.begin(9600)`. This baud rate just means the serial communication takes place at 9600 bits per second. This needs to match on both ends, the serial monitor needs to have 9600 baud rate too.

We can send data using the `Serial.println()` as mentioned before, which takes an input message and prints it out on the Serial Monitor.  

Just like we can send data from the MCU to the computer, we can also receive data from the computer to the MCU. We can do so with the `Serial.available()` function, which checks the serial port to see if it has received any data. The `Serial.read()` reads a single byte at a time. 
<!--- A brief description of what you understand/learned from the tutorial -->  

### Challenges  

<ins>__Challenge 1: LED Blink Frequency__</ins>  

In this challenge, we are tasked to make LED's blink at a particular frequency, testing on our understanding on how to read and write to the GPIO pins.  

I made a function that takes in a frequency as a parameter, and returns an unsigned long value, which will be passed into the `delay()`. This returned value is obtained by taking 1/frequency, which gives period, T. But since I call the `delay()` function between a HIGH and a LOW of the LED, i needed to return T/2.  

Then we are also required to make the LED blink such that it turns on for a time t and off for a time t2. I solved this using a function too, which takes in on time, off time, and pin of the LED as a parameter.  


![part1challenge1RED](https://bit.ly/3iNMjU8) | ![part1challenge1BLUE](https://bit.ly/3FzhagL) | ![part1challenge1YELLOW](https://bit.ly/3oM02hV)
:--------------------------------------------:|:----------------------------------------------:|:------------------------------------------------:

![part2challenge1RED](https://bit.ly/3DsaUpw) | ![part2challenge1BLUE](https://bit.ly/3DtPNTy) | ![part2challenge1YELLOW](https://bit.ly/3v0of5f)
:--------------------------------------------:|:----------------------------------------------:|:------------------------------------------------:


<ins>__Challenge 2: Stopwatch__</ins>  

In this challenge we are required to make a stopwatch which works using a `counter` that is incremented every 1 second, with allows functionality of starting the stopwatch with a button, pausing it, and resuming it.  

The way I implemented it is using the `millis()` function, which returns the time in miliseconds since the ESP32 has been powered up.  

Then I use it at my advantage to handle two timed events which occur only when a certain time is reached, that is 1000ms to increment the counter, and 100 ms to print the counter value.  

This is probably the most useful part of the lab as it teaches us how to handle time-dependent events with the `millis()` function without having to interfere and halt the other process in the code, which is the case with `delay()` method.  

![Challenge2](https://bit.ly/3BxMABO)

<ins>__Challenge 3: Timer__</ins>  

Challenge 3 is pretty much based of our understanding in utilizing `millis()` as required in challenge 2. 

We needed to both increment and decrement a variable called `timer`. The way it works is when a user push the button, it's like we want to set up the timer to a specific time, so the `timer` need to be incremented. However, when the user is no longer pushing the button for at least 3 seconds, the timer should be activated and hence `timer` will countdown.  

Again, this requires handiling timed events, and this time there are 3 of them:  

- 1000ms mark, when the timer is supposed to be decremented, i.e: countdown started.  

- 100ms mark, when the timer value is to be printed on the serial monitor to maintain its responsiveness.  

- 3000ms mark, when we need to activate the timer.  

![Challenge2](https://bit.ly/2YDVdws)



