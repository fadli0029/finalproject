###################################################
# VARIABLE ASSIGNMENTS AND SYNTAX, 0.3: Exercises #
###################################################

# Question 1:
list_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# Question 2:
list_2 = [11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]


# Question 3:
list_1[0] = "one" 
list_1[1] = "two" 
list_1[2] = "three" 


# Question 4:
my_tuple = ("eleven", "twelve", "thirtheen")
x = 0
for index in my_tuple: 
    list_2[x] = index
    x += 1


# Question 5:
# i.
joint_1 = [] 
joint_1.extend(list_1)
joint_1.extend(list_2)
print(joint_1)

# ii.
joint_2 = list_1 + list_2 
print(joint_2)


# Question 6:
def list_shift(base_list, new_data):
    temp = base_list + new_data
    i = len(new_data)
    result = temp[i:]
    base_list = result
    return base_list
    
# what i did in this function is 
# merged the base_list and new_data, then store it in temp
# find the length of new_data with len(), store it in i
# then the result is just slicing the temp from i to end
# the copy result into base_list coz that's the requested
# signature of the function
# tester:
# fixed_length_list = [1,2,3,4]
# new_data = [5,6]
# print(list_shift(fixed_length_list, new_data))


# Question 7:
# -> Bonus: are there any edge cases that the your function doesn't handle? Can you think how you might address them?



#####################################
# EXECUTION CONTROL, 1.4: Exercises #
#####################################

# Question 1:
commands_list = ["STATUS", "ADD", "COMMIT", "PUSH"]


# Question 2:
for index in range(0, len(commands_list)):
    print(commands_list[index])


# Question 3:
list_comments = ["PUSH FAILED", "BANANAS", "PUSH SUCCESS", "APPLES"]


# Question 4:
text = "SUCCESS" 


# Question 5:
# i.
if "SUCCESS" in "SUCCESS":
    print("True")
else:
    print("FALSE")

# ii.
if "SUCCESS" in "ijoisafjoijiojSUCCESS":
    print("True")
else:
    print("FALSE")

# iii.
if "SUCCESS" == "ijoisafjoijiojSUCCESS":
    print("True")
else:
    print("FALSE")

# iv.
if "SUCCESS" == text:
    print("True")
else:
    print("FALSE")

# v.
# i. and ii. are comparing character by character
# iii. and iv. are comparing the whole string


# Question 6:
for index,elem in enumerate(list_comments):
    if text in list_comments[index]:
        print("This worked!")
        break
    print(elem)
        


##################################
# ERROR HANDLING, 2.2: Exercises #
##################################

# Question 1:
name = "Muhammad"


# Question 2:
byte_name = name.encode('utf-8')


# Question 3:
byte_name_bad = byte_name + b'\xef'


# Question 4:
# byte_name_bad.decode()
# The error is UnicodeDecodeError


# Question 5:
try:
    byte_name_bad.decode()
    print(byte_name_bad.decode())
except UnicodeDecodeError:
    byte_name_bad = ''
    print(byte_name_bad)
 

# Question 6:
try:
    byte_name.decode()
    print(byte_name.decode())
except UnicodeDecodeError:
    byte_name = ''
    print(byte_name)


