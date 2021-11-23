import numpy as np

# Question 1:

array1 = np.array([0, 10, 4, 12])
print(array1 - 20)
# output:
# [-20 -10 16 -8]
print(np.shape(array1))
# output:
# (4,)


# Question 2:

temp_array2 = [[0, 10, 4, 12], [1, 20, 3, 41]]
array2 = np.array(temp_array2)
# output:
# [[ 0 10  4 12]
# [ 1 20  3 41]]

temp_array2_new = np.array([4, 12, 1, 20])
array2_new = temp_array2_new.reshape(2,2)
# I use the .reshape method from numpy
# output:
# [[ 4 12]
# [ 1 20]] 


# Question 3:

array3_temp = np.hstack((array1, array1))
for i in range(2):
    array3_temp = np.vstack((array3_temp,array3_temp))
# output:
# [[ 0 10  4 12  0 10  4 12]
# [ 0 10  4 12  0 10  4 12]
# [ 0 10  4 12  0 10  4 12]
# [ 0 10  4 12  0 10  4 12]]


# Question 4:
array4a = np.arange(-3,16,6)
# output:
# [-3  3  9 15] 

array4b = np.arange(-7,-20,-2)
# output:
# [ -7  -9 -11 -13 -15 -17 -19]


# Question 5:

array5 = np.linspace(0, 100, 49, True)
# When we know a fix value of how many numbers we want between the
# start and end point, then linspace is the preferred method imo.


# Question 6

array6 = np.zeros([3,4], dtype = int)
array6[0] = [12, 3, 1, 2]
array6[1, 0] = 0
array6[:, 1] = [3, 0, 2]
array6[2, :2] = [4, 2]
array6[2, 2:] = [3, 1]
array6[:, 2] = [1, 1, 3]
array6[1, 3] = 2
#print(array6[0])     # [12 3 1 2]
#print(array6[1, 0])  # 0
#print(array6[:, 1])  # [3 0 2]
#print(array6[2, :2]) # [4 2]
#print(array6[2, 2:]) # [3 1] 
#print(array6[:, 2])  # [1 1 3]
#print(array6[1, 3])  # 2
# print(array6)



# Question 7

string7 = "1,2,3,4"
content = string7.split(",")
content = np.array(content)
temp = content
temp2 = temp
print(type(content))
print(content)
for val in range(6):
    content = np.vstack((content,content))
for val in range(5):
    temp = np.vstack((temp, temp))
for val in range(2):
    temp2 = np.vstack((temp2, temp2))
ans = np.vstack((content, temp))
ans2 = np.vstack((ans, temp2))
array7 = ans2
print(np.shape(array7))

