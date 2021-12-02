# Final Project | 12/07/2021 :writing_hand:
### Prepared by:  
> Muhammad Fadli Alim Arsani :boy: | A16468481  
> Justin Volheim :man: | A16582348  

</br>  

Table of contents :bookmark_tabs:
=================================
* [Final Project Objective](#final-project-objective-mag)
* [Python Sockets Tutorial](#python-sockets-tutorial-memo)
* [Grand Challenge 1](#grand-challenge-1-trophy)
  * [Objectives](#objectives-gc1-bulb)
  * [Improvements & Features](#improvements-and-features-gc1-hammer_and_wrench)
  * [Implementations](#implementations-gc1-computer)
  * [Demo](#demo-gc1-clapper)
* [Grand Challenge 2](#grand-challenge-2-trophy)
  * [Objectives](#objectives-gc2-bulb)
  * [Features](#features-star2)
  * [Implementations](#implementations-gc2-computer)
  * [Demo](#demo-gc2-clapper)
* [Teammates Roles](#teammates-roles-boy-man-)

</br>  

Final Project Objective :mag:
=============================

</br>  

Python Sockets Tutorial :memo:
==============================

</br>  

Grand Challenge 1 :trophy:
==========================
Space Invader :space_invader:!

Objectives GC1 :bulb:
---------------------

Improvements and Features GC1 :hammer_and_wrench:
-------------------------------------------------
__Improvements:__  
1. __Smoother tilting__ when moving left and right, smooth like butter :butter:. This is achieved via __Digital Signal Processing__, utilizing `ECE16Lib` modules.
2. __Decoupled moving and firing__, user can do both silmutaneously!
3. Player can ideally and effectively __fire via button__ rather then tilting the breadboard.

__Features:__  
1. Player can see their __score displayed on the OLED__.
2. Making use of the __buzz motor__, player will feel __vibration on the controller__ when he/she gets hit by the space invaders! Don't worry, it ~~doesn't~~ hurts.
3. __Game statistics__, such as __lives count__, __game over status__, and __score__, can be seen directly from the OLED

Implementations GC1 :computer:
------------------------------
> __Improvements:__  

<ins>1. Obtaining seamless movements via DSP</ins>  
Achieving this is a two-part process: __finding the right threshold__ and __applying the DSP__. For the DSP, we applied __moving average__ on the accelerometer data coming in:  
```python
def moving_average(self, x, win):
  ma = np.zeros(100)
  for i in np.arange(0,len(x)):
    if(i < win):
      ma[i] = np.mean(x[:i+1])
    else:
      ma[i] = ma[i-1] + (x[i] - x[i-win])/win
  return ma

def process(self, target, win):
  out = self.moving_average(target, win)
  return out
```
We noticed that this was sufficient enough to give us not just smoother tilting, but less delay. Further processing didn't turn out as good as this one. As for thresholding the accelerometer value, such that it's not too sensitive, we decided to make two __sensitivity levels__ available, __level 1__ and __level 2__.  

__Level 1:__ the program will respond to a tilt (left or right) only up to __45 degrees__.  

__Level 2:__ the program will respond to a tilt (left or right) up to __90 degrees__.  

Then, from our observation, the desired thresholds for each axis are as the following:  

<ins>Stationary</ins>:     __1950__  `<=`  __x-axis__-acclerometer-value `<=` __1970__  

<ins>Tilting left</ins>:   __x-axis__-acclerometer-value `<=` __2300__  

<ins>Tilting right</ins>:  __x-axis__-acclerometer-value `>=` __1655__  

> :heavy_exclamation_mark: In both cases, __z-axis__-accelerometer-value `>` 2200

Should 2 be choosen as the sensitivity level, then those values are scaled in the following manner:  
```python
if (self.the_sensitivity == 2):
  adj_xLeft = 500
  adj_xRight = 140
  adj_z = 230

adjusted_thresLeft = 2300+adj_xLeft
adjusted_thresRight = 1655-adj_xRight
adjusted_thresZ = 2200-adj_z
```

<ins>2. Decoupling moving and firing</ins>  
This is achieved by __sending 4 different direction__ messages to `spaceinvaders.py` via socket. The following are the 4 different messages:  
- `"LFIRE"` 
  - Indicates that the player is moving __left__ (tilting left) whilst pressing the button to __fire__.
- `"LEFT"` 
  - Indicates that the player is moving __left__ only, __without firing__.
- `"RFIRE"` 
  - Indicates that the player is moving __right__ (tilting right) whilst pressing the button to __fire__.
- `"RIGHT"` 
  - Indicates that the player is moving __right__ only, __without firing__.

The server, `spaceinvaders.py` will receive one of these messages from its client `space_invaders_controller.py`.   
In `space_invaders_controller.py`, we implemented two functions as helpers in generating those messages:  

```python
def is_between(self, target, x, y):
  return (target >= x and target <= y)

def generatingCommand(self, xf_input, yf_input, zf_input, is_fire):
  adj_xLeft = 0
  adj_xRight = 0
  adj_z = 0
  if (self.the_sensitivity == 2):
    adj_xLeft = 500
    adj_xRight = 140
    adj_z = 230

  adjusted_thresLeft = 2300+adj_xLeft
  adjusted_thresRight = 1655-adj_xRight
  adjusted_thresZ = 2200-adj_z

  command = None

  x_cmd = np.array(xf_input)
  y_cmd = np.array(yf_input)
  z_cmd = np.array(zf_input)

  if (is_fire == 2):
    # shooting but not moving
    command = "FIRE"

  if (self.is_between(x_cmd[-1], 1950, 1970) == False):
    # tilting
    # az can drop to lowest to 2.2k, regardless tilted left or right
    # ax can go up to 2300 when tilt left and as low as 1655 when tilt right
    if (x_cmd[-1] <= adjusted_thresLeft and x_cmd[-1] > 1950 and z_cmd[-1] > adjusted_thresZ):
      # tilt left
      if (is_fire == 2):
        command = "LFIRE"
      else:
        command = "LEFT"
    if (x_cmd[-1] >= adjusted_thresRight and x_cmd[-1] < 1950 and z_cmd[-1] > adjusted_thresZ):
      # tilt right
      if (is_fire == 2):
        command = "RFIRE"
      else:
        command = "RIGHT"

  return command, x_cmd[-1], z_cmd[-1]
```
Then, in `run()`, we did the regular implementations of receiving accelerometer data from the MCU, process it via DSP, and etc, as previously learned from the lab assignments. See [here]) for the full source code.  

On the `space_invaders_controller.py` side, we added the following lines after the block `if msg == "FIRE"`:  

```python
...
...
elif msg == "LFIRE" or msg == "RFIRE":
    if len(self.bullets) == 0 and self.shipAlive:
        if self.score < 1000:
            bullet = Bullet(self.player.rect.x + 23,
                            self.player.rect.y + 5, -1,
                            15, 'laser', 'center')
            self.bullets.add(bullet)
            self.allSprites.add(self.bullets)
            self.sounds['shoot'].play()
            # added - Fade
            self.player.update_udp_socket(msg)
            # ...
        else:
            leftbullet = Bullet(self.player.rect.x + 8,
                                self.player.rect.y + 5, -1,
                                15, 'laser', 'left')
            rightbullet = Bullet(self.player.rect.x + 38,
                                    self.player.rect.y + 5, -1,
                                    15, 'laser', 'right')
            self.bullets.add(leftbullet)
            self.bullets.add(rightbullet)
            self.allSprites.add(self.bullets)
            self.sounds['shoot2'].play()
            # added - Fade
            self.player.update_udp_socket(msg)
            # end of additions ...
else:
    self.player.update_udp_socket(msg)
...
...
```
And then added the following lines in the `update_udp_socket()` method:  

```python
def update_udp_socket(self, direction):
    if direction == "LEFT" and self.rect.x > 10:
        self.rect.x -= self.speed
    if direction == "RIGHT" and self.rect.x < 740:
        self.rect.x += self.speed
    # added - Fade
    if direction == "LFIRE" and self.rect.x > 10:
        self.rect.x -= self.speed
    # end of additions ...

    # added - Fade
    if direction == "RFIRE" and self.rect.x < 740:
        self.rect.x += self.speed
    # end of additions ...

    game.screen.blit(self.image, self.rect)
```

<ins>3. Enabling button press as firing mechanism</ins>  
As already seen in previous code snippets for the other implemtations above, the `is_fire` boolean is invoked if the button is pressed. In the `run()` method inside `space_invaders_controller.py` (I represent other lines as '...' if they are not important to demonstrate this concept):
```python
  def run(self):

    # send "start" message to MCU
    ...
    ...

    previous_time = 0
    while True:
      message = self.comms.receive_message()

      if(message != None):
        f_command = None
        try:
          (m0, m1, m2, m3, m4) = message.split(',')
        except ValueError:
          continue

        # add m1,m2,m3,m4 to ax, ay, az circular lists
        ...
        ...
        ...

        current_time = time()
        if (current_time - previous_time > self.refresh_time):
          previous_time = current_time

          # DSP
          ...
          ...

          f_command, valx, valz = self.generatingCommand(self.ax_f, self.ay_f, self.az_f, int(m0))
          # m0 = 2, means the player press the button to fire
          # m0 = 7, means the player press the button to fire
          if f_command is not None:
            mySocket.send(f_command.encode("UTF-8"))

        # receives message from server (for displaying game statistics on OLED)
        ...
        ...
        ...
```
The value of `m0` is determined by the button press. In the arduino side, `SpaceInvadersController.ino`:  

```cpp
currentState = !digitalRead(buttonPin);
if (currentState != lastButtonState) { 
  if (oldStatus) {
    isShoot = false;
  }
  if (oldStatus == false) {
    isShoot = true;
  }
}
lastButtonState = currentState;

// other stuffs like OLED, etc
...
...
...

if(sending && sampleSensors()) {
  String response = String(sampleTime) + ",";
  response += String(ax) + "," + String(ay) + "," + String(az);

  if (isShoot) {
    sendMessage(String(2) + "," + response);
  }
  else {
    sendMessage(String(7) + "," + response);
  }
}

...
...
```

Hence, in the `generatingCommand()` function inside our client `space_invaders_controller.py`, if `m0` is `2` (the player is firing), the server `spaceinvaders.py` will receive either one of these messages, `FIRE`, `LFIRE`, `RFIRE`.  

```python
def generatingCommand(self, xf_input, yf_input, zf_input, is_fire):
  # thresholding settings
  ...
  ...
  ...

  if (is_fire == 2):
    # shooting but not moving
    command = "FIRE"

  if (self.is_between(x_cmd[-1], 1950, 1970) == False):
    if (x_cmd[-1] <= adjusted_thresLeft and x_cmd[-1] > 1950 and z_cmd[-1] > adjusted_thresZ):
      # tilt left
      if (is_fire == 2):
        command = "LFIRE"
      else:
        command = "LEFT"
    if (x_cmd[-1] >= adjusted_thresRight and x_cmd[-1] < 1950 and z_cmd[-1] > adjusted_thresZ):
      # tilt right
      if (is_fire == 2):
        command = "RFIRE"
      else:
        command = "RIGHT"

  return command, x_cmd[-1], z_cmd[-1]
```

> __Features:__  

<ins>1. Displaying score on the OLED</ins>  
<!--NOTE: Start here justin-->


<ins>2. Buzzing the motor when getting hit</ins>  
<!--NOTE: Start here justin-->


<ins>3. Integrating game statistics</ins>  
<!--NOTE: Start here justin-->


Demo GC1 :clapper:
------------------

</br>  

Grand Challenge 2 :trophy:
==========================

Objectives GC2 :bulb:
---------------------

Features :star2:
----------------

Implementations GC2 :computer:
------------------------------

Demo GC2 :clapper:
------------------

</br>  

Teammates Roles :boy: :man: :
=============================

