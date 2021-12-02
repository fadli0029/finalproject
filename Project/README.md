# Final Project | 12/07/2021 :writing_hand:
### Prepared by:  
> Muhammad Fadli Alim Arsani :boy: | A16468481  
> Justin Volheim :man: | A16582348  

</br>  

Table of contents :bookmark_tabs:
=================================
* [Final Project Objective](#final-project-objective) 
* [Python Sockets Tutorial](#python-sockets-tutorial) 
* [Grand Challenge 1](#grand-challenge-1) 
  * [Objectives](#objectives-gc1) 
  * [Features & Improvements](#features-and-improvements-gc1) 
  * [Implementations](#implementations-gc1) 
  * [Demo](#demo-gc1) 
* [Grand Challenge 2](#grand-challenge-2) 
  * [Objectives](#objectives-gc2) 
  * [Features](#features)
  * [Implementations](#implementations-gc2) 
  * [Demo](#demo-gc2) 

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

Features and Improvements GC1 :hammer_and_wrench:
-------------------------------------------------
__Improvements:__  
1. __Smoother tilting__ when moving left and right, smooth like butter :butter:. This is achieved via __Digital Signal Processing__, utilizing `ECE16Lib` modules.
2. __Decoupled moving and firing__, user can do both silmutaneously!

__Features:__  
1. User can see their __score dispalyed on the OLED__.
2. Making use of the __buzz motor__, player will feel __vibration on the controller__ when get hit by the space invaders! Don't worry, it ~~doesn't~~ hurts.
3. __Game statistics__, such as __lives count__, __game over status__, and __score__, can be seen directly from the OLED

Implementations GC1 :computer:
------------------------------
<ins>1. Obtaining seamless movements via DSP </ins>  
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
We noticed that this was sufficient enough to give us not just smoother tiling, but less delay. Further processing didn't turn out as good as this one. As for thresholding the accelerometer value, such that it's not too sensitive, we decided to make two __sensitivity levels__ available, __level 1__ and __level 2__.  

Level 1: the program will respond to a tilt (left or right) only up to __45 degrees__.  

Level 2: the program will respond to a tilt (left or right) up to __90 degrees__.  

Then from our observation, the desired thresholds for each axis are as the following:  

<ins>Tilting left</ins>  
The accelerometer value of for the x-axis is less than or equal to 2300__.


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

