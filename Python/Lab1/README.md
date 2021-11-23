<!--- To insert a new line(break), the fastest way -->
<!--- is to just do (space)(space)(return) -->  

# ECE16 Lab 1 Report
## Prepared by: Muhammad Fadli Alim Arsani	
## Student ID: A16468481
## Date: 10/02/2021

</br>

### Lab 1 Objective:  

The main objective of Lab 1 is to build a strong fundamentals of Python progamming within the students.  

We learn how to work with python whilst utilizing its rich libraries like `numpy` for example.  

This lab prepares students with the basic skills that we need when working with python-based projects like slicing lists, functions, try/except, loopings, strings, etc.


</br>

### Tutorials  

__Tutorial 1: Python Install & Setup__  
<!--- A brief description of what you understand/learned from the tutorial -->  
Tutorial 1 is a brief walkthrough on how to get a python development environment on your laptop/pc. I personally already have python installed on my Linux machine (Manjaro), and I use my favourite editor of all time: __vim__  

For reference, this is how I would install Python on my machine:
```bash
sudo pacman -S python
```  

And this is how I would install vim:
```bash
sudo pacman -S vim
```  


__Tutorial 2: Python Basics__  
<!--- A brief description of what you understand/learned from the tutorial -->  
In this tutorial, I learned the Fundamentals of writing code in Python, focusing on:  

1. Data Types  

2. Lists

3. Strings

4. Looping

5. Functions  


<ins>1. Data Types </ins>  

In Python, when we want to declare an integer, simply doing: `a = 5` will work perfectly unlike most other languages which require us to specify the type like so: `int a = 5`.  
i.e: Python is a __weakly typed language__, as mentioned in the tutorial. One of the reason for this design is to acquire maximum functionality.  

The most common data types in Python, or at least the ones that we will encounter the most in this class, are the following:  
- int

- float

- list (just like an array, kinda)

- str (denoted with `''` or `""`, and one thing to note is there is no such thing of `char` data type in Python)

- dict (a collection of key-valued pairs, very useful imo!)

- tuple (basically an immutable list)  



<ins>2. Python Lists </ins>  

Declared with `[]`, and can contain multiple data types, for example: `an_example = ["ECE16", 2021, "Fall"]`  

We can access an element in a list, by specifying the index of the element like so:
```python 
a_list = ["elem1", "elem2", "elem3"]
# access elem2:
a_list[1]
# because the index starts at 0
```  

We can modify (remove, add, etc) a lists, for example, using the `.append` method allows us to add item to the list:  
```python 
a_list = [3,4,6]
a_list.append(6)
# will add 60 to the a_list
```  

Another cool and useful method is the `del()` method, which remove items from the list: `del(a_list[1])` will remove the 2nd element in `a_list`.


There is also an operation called __slicing__ which is very useful when dealing with lists, for example we can choose which element to take from a list (the simples of all the great things we can do wwith slicing operation):  
```python  
another_list = [1,2,3,4,5]
print(another_list[-2:])
# will output 4 and 5, see documentation for the syntax of slicing.
```

Another probably one of the most useful operation we can do with list is called __list comprehension__. It allows us to loop through elements in a list whilst doing operation on them.  
For example:  
```python  
my_list = [1,2,3,4,5]
add_2 = [elem+2 for elem in my_list]

# output: add_2 = [3,4,5,6,7]
```

<ins>3. Strings </ins>  

An important thing we must note about strings in python is __they are immutable__. For example:  
```python
is_immutable = "Hello" 
is_immutable[2] = "C"

# Output: error
```  

As for operations, there are so many oprations we can do with strings, for example, one that we will use a lot is slicing the string like what we did with lists, and taking the length of a string with the `len()` method:  

```python
this_aString = "Okay"
print(len(this_aString))
# output: 4
```

<ins>4. Looping </ins>  

Anyone who progammed before should know looping is literally super useful and super needed in any program. In python, we can loop in many ways:  

regular looping:
```python
for index in a_list:
	print(a_list[index])
```

we can also use a method call enumerate that gives index to each element in a list, like key-value pair thingy:
```python
for index, elem in enumerate(a_list):
	if elem < 4:
		print(a_list[index])
```

<ins>5. Functions </ins>  

In Python, we create function with this syntax:  
```python
def foo(x):
	x = 0
	return x 
# this function is obviously useless (i think), but it suffices to show how to create a function in python. 
# and remember indentation is significant in python, we can't ignore it, it's not for style/neatless like in other languages.
```

</br>  


__Tutorial 3: Numpy__   
<!--- A brief description of what you understand/learned from the tutorial -->  

This tutorial is probably the most important part of the lab, not only because the challenges build upon it, but because __numpy is such a powerful python library__, ignoring it is like ignoring STL in C++.  

When dealing with data, big or small, it's always good to have a friend name `numpy` to make everything easier and simpler!


In this tutorial, I learn some of the most commonly use functionalities of numpy, namely:

- creating numpy array using `numpy.array()`

- creating an array filled with zeros, using `numpy.zeros()`, or with ones: `numpy.ones()`

- restructuring array the way we want it with `a.reshape()`, where `a` is a `numpy array`

- flatten a numpy array, `a.flatten`

- `numpy.resize()` to resize our array according to how we want it to be.

- stacking array vertically, `numpy.vstack()` or horizontally, `numpy.hstack()`

- indexing and stepping through a numpy array with, `np.arange()`

- `numpy.linspace()` to generate spacing between the elements, with starting and ending according to user.

- slicing and indexing numpy array, pretty much like doing it with a list


</br>  

### Challenges  

<ins>__Challenge 1: Python Worksheet:__</ins>  

This challenge is divided into Variable Assignment and Syntax, Execution Control, Error Handling, and Functions.  

The exercises in challenge 1 for Variable Assignment and Syntax focus on dealing with list and tuple, for example replacing elements in a list, joining lists together with `.extend()` method and `+` operator, and appending a list with a function.  

Then, we focused on Execution Control dealing and making use of loops namely, `for` loop, `while` loops, `if` statements and logic control, and how `in` differes with `==` comparator.

Next, an important feature in python: the `try` and `except`, and `assert` error handling technique. With these, we can catch errors when we need to, to check our program and debugging. The exercises tested our understanding on how to really make use of the error handling in Python, as it is a vital skill in building good Python programming habits.

Finally, it tested understandings in building functions, how to pass arguments, default arguments, and etc. Also, regarding variable scope and what it means to declare as global.


<ins>__Challenge 2: Stock Simulator:__</ins>  

This challenge focuses on our ability to make use of the `numpy` library to the full extent (at least to the max of what has been taught for this particular assignment).  

We are given a stock data, daily, and need to work with it as a numpy array, making use of its built-in methods, so that we can calculate gains and loses according to the given stratergy.  

Although this is a small-scale real-world example of Python and `numpy` in action, it's very important in teaching students getting used to working with the `numpy` library.

Attached is the output for the program:  

![alt text](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab1/images/challenge2.png)  


<ins>__Challenge 3: Piglatin__</ins>  

Challenge 3 is more challenging than I expected :sweat_smile: . The challenge asks us to take an english word as an input, then convert it to pig latin, and vice versa.  

We need to implement two functions here:  

- `english english_to_pig_latin()`

- `pig_latin_to_english()`  

It also trains students to get used to working with libraries in Python, and for this one we needed to work with the `pyenchant` library to verify if a word is a valid english word.  

Finally, we needed to be able to handle edge cases to, which is a key in making good an reliable code/programs.  

Attached is the output for the program:  

![alt text](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab1/images/challenge3.png)



