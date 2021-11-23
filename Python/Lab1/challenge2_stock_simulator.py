import numpy as np

# Question 1:
# a.
# Daily Apple Stock Value from 01-01-2019 - 04-30-2019
apple_stock = [
38.38222885, 34.55907822, 36.03437042, 35.95417023, 36.63956451, 37.26177216, 37.38086700, 37.01386261, 36.45728683, 37.20344162, 37.65793991, 37.88154221, 38.11487198, 37.25934601, 37.41003036, 37.11351776, 38.34333038, 37.98849106, 37.59475327, 40.16376877, 40.45300674, 40.47245026, 41.62205887, 42.33419800, 42.34877777, 41.54671860, 41.59553528, 41.35632706, 41.71270752, 41.53939438, 41.69073868, 41.59797287, 41.72246552, 41.99096680, 41.75419617, 42.22041702, 42.52796555, 42.55237579, 42.68418503, 42.26435089, 42.70859909, 42.92338943, 42.84527588, 42.59875488, 42.10569000, 42.20576477, 43.66787338, 44.15849686, 44.35376358, 44.84682083, 45.43020248, 45.89398193, 45.53028870, 45.92815399, 47.61970139, 46.63357544, 46.06971741, 45.59374619, 46.00382233, 46.06484222, 46.36507416, 46.67995834, 47.35852432, 47.68317032, 47.76615143, 48.08591461, 48.84260559, 48.69614792, 48.96952438, 48.56189346, 48.54235840, 48.63023376, 48.63512039, 49.58219528, 49.76038361, 49.92391968, 50.64399338, 50.56588364, 50.10699081, 49.86777878, 49.94344711
]

# b.
print("apple_stock array type: ")
print(type(apple_stock))

# c.
apple = np.array(apple_stock) 
print("apple numpy array type: ")
print(type(apple))


# Question 2:
strategy = np.zeros(apple.size)
# to get the same size as apple array, i use .size


# Question 3:
for i in range(3,  len(apple)): 
    # I start at 3 bcoz the previous 3 days is "do nothing", i.e: 0
    # then go all the way to the end
    prices = apple[i - 3 : i] 
    # here I put the previous 3 days prices from the current day, i,i.e: idx 0, idx1, idx2]
    last_3_days_ave = np.mean(prices)
    # here, i find the average of that 3 days with np.mean()
    todays_price = apple[i]
    # putting the price of the current day, i, to a var called todays_price
    if last_3_days_ave < todays_price:
        strategy[i] = -1
    elif last_3_days_ave > todays_price:
        strategy[i] = 1
    # then use a conditional statements to populate the
    # strategy array

print("strategy array: ")
print(strategy)


# Question 4:
# strategy = [0, 0, 0, 1,-1, -1, -1, 1, 0, 1]
cash = 10000
num_shares = 100
profits = 0
# these are variables to hold the current cash before buying/selling,
# how much shares I have after each transaction,
# and the profits.
for i in range(len(strategy)):
    # traversing through the stratergy array
    if strategy[i] == 1:
        num_shares += 1
        cash -= apple[i]
    # if I see a 1, that means im buying, so num_shares is increased
    # but, cash is reduced accoding to the amount of the price
    # associated with that index, i, in apple array
    elif strategy[i] == -1:
        num_shares -= 1
        cash += apple[i]
    # same concept applies for buying, except that this is selling
    # so num_shares reduced, cash is increased

profits = cash - 10000
        

# Question 5:
# the num of shares that we have at the end is basically
# equal to my variable, num_shares.
# but just to answer the question:
initial_shares = 100
shares = initial_shares + np.sum(strategy)
# I use np.sum to sum all the values in the strategy array and add it with the initial shares


# Question 6:
print("shares: " + str(shares))
print("profits: " + str(profits))





