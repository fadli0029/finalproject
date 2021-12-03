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
  * [Discussions of Improvements & Features](#improvements-and-features-gc1-hammer_and_wrench)
  * [Controller Instructions](#dummy)
  * [Implementations](#implementations-gc1-computer)
  * [Demo](#demo-gc1-clapper)
* [Grand Challenge 2](#grand-challenge-2-trophy)
  * [Descriptions & Discussions](#dummy)
  * [Features](#features-star2)
  * [Controller Instructions](#dummy)
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
In this challenge, we are tasked to make a __game controller__ for the game called __Space Invader__ :space_invader:.

Objectives GC1 :bulb:
---------------------
The objective of this challenge is to __encourage students to use the knowledge they learned throughout all 7 labs__, by making a __fully-functionaly game controller__, which not only __improves the game mechanics__, but also has some __extra features__! Students work in a team of 2 and try to come up with a series of improvements and feature to add to the game. This ultimately tests their understanding in the concepts taught in the previous labs.

Discussions of Improvements & Features GC1 :hammer_and_wrench:
----------------------------------------------------------------
__Improvements:__  
1. __Smoother tilting__ when moving left and right, smooth like butter :butter:.
   - When playing the game first time, we realize the tilting is not smooth, there's no way one can be a pro player at this :frowning_face:. So, we thought why not *"clean"* the data first? Fortunately, the previous labs have equipped us with this skill. Hence, we __implemented Digital Signal Processing__, utilizing the `ECE16Lib` module, to resolve this issue! (see implementation for details).
2. __Decoupled moving and firing__, user can do both silmutaneously!
   - In any shooting games, any player would want to be able to move while shooting; this is essential to not die early and quit-rage. So we decided to make this possible in the game. By sending the right command (see implementation for details), the server can interpret and respond when the player intend to both move and shoot.
3. Player can ideally and effectively __fire via button__ instead of tilting the breadboard.
   - We found out that tilting the breadboard upwards/downwards to fire is very inefficient, kind of too much work at some point for such a simple task. So we came up with the idea of using the button as the trigger to fire, which is not only more efficient but very easy to use! Full-Auto? No problemo!  

__Features:__  
1. Player can see their __score displayed on the OLED__.
   - (note: need to satisfy discussion of design choices here, see improvements above for example)
2. Making use of the __buzz motor__, player will feel __vibration on the controller__ when he/she gets hit by the space invaders! Don't worry, it ~~doesn't~~ hurts.
   - (note: need to satisfy discussion of design choices here, see improvements above for example)
3. __Game statistics__, such as __lives count__, __game over status__, and __score__, can be seen directly from the OLED
   - (note: need to satisfy discussion of design choices here, see improvements above for example)

Controller Instructions
-----------------------

Demo GC1 :clapper:
------------------

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

</br>  

Grand Challenge 2 :trophy:
==========================
For this Design Challenge, we choose to make a __game controller__ for the famous classic __Mine Sweeper__ game!

Descriptions & Discussions :bulb:
---------------------------------
The idea of this design challenge is to build a fun light work-out environment for people who like staying at home, especially during the pandemic (though it's almost over, is it? :thinking:). By *"forcing"* the player to do a certain number of jumping jacks to be granted the tile of his/her choosing, he/she for sure sweat!  

In terms of how is this project relevant to ECE16, we believe it encompasses everything that was taught in this class, from as basic as good __Object-Oriented Programming__ implementation, to __Digital Signal Processing__, concepts of __Finite State Machines__ in deriving a solution effectively and efficiently, and etc.  

TLDR:  
> Our goal is to make this old game enjoyable again, and promotes healthy lifetyle, especially during this pandemic LOL. It looks simple, but it's tiring :cold_sweat: !

Features :star2:
----------------
__Features:__  
1. Players can __select tiles, restart game, by pressing the button on the MCU__, eliminating the need to interact with the keyboard/mouse.
   - We want to give a 'workout-like' experience to the user; think of the controller like a skipping rope handle. While working out, in this case doing the jumping jacks, we wouldn't want the user to go back and forth interacting with the keyboard/mouse. Thus, we made everything is at a touch of a button.
2. Accurate jumping jacks counter, achieved via __Digital Signal Processing__.
   - We implemented __moving average__ on the __*l1-norm*__ of the three axes coming in from the accelerometer sensors. Doing this __eliminate the noise__, and make it __more reliable__.
   - Then using the `find_peaks()` method from the `scipy.signal` module, we calculated the peaks that indicates a valid jumping jack.
   - All of this is made even simpler thanks to our `ECE16Lib` which we built upon finishing series of labs in this class!
3. __Game statistics__, displaying __jumping jack counts__ on the OLED display.
   - As mention in point no. 1, the user can directly look at the OLED display to know how many more jumping jacks are needed to select the tile they choose.

Controller Instructions
-----------------------
The following is the procedure to use the controller:  
1. Upload the sketch, `MineSweeper.ino` to the MCU.
2. Run the game by running the command: `python Minesweeper.py`
3. Instantiate the client-server connection, run the command to activate the controller: `python minesweeper_controller.py`
4. You will be asked to select a tile. Input the `x` and `y` coordinates, where __x is the m'th row__, and __y is the n'th column__. Do this by pressing the button on the breadboard(x-coord), and the built-in button (y-coord) on the microcontroller. You will see your selection on the OLED display.
5. Then, the program will calculate the required number of jumping jacks you need to do to grant you that tile, in the following way:
   - `number of jumping jacks = | (previous x-coord - current x-coord) | + | (previous y-coord - current y-coord) |`
6. Do the jumping jacks! After satisfying the jumping jacks counts, your tile will be selected on the game.
7. Continue playing until you win/lose, good luck :thumbsup: !
8. If you win/lose and would like to restart the game, press the button once.
9. Enjoy!

Demo GC2 :clapper:
------------------

Implementations GC2 :computer:
------------------------------

</br>  

Teammates Roles :boy: :man: :
=============================
<ins>__Muhammad Fadli Alim Arsani :boy:__</ins>  

<ins>__Justin Volheim :man:__</ins>  


