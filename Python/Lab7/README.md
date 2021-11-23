# ECE16 Lab 7 Report :writing_hand:
## Prepared by: Muhammad Fadli Alim Arsani
## Student ID: A16468481
## Date: 11/16/2021

### Lab 7 Objective :pushpin:  

This final lab is the culmination of all the previous labs. We were tasked to build a complete wearable, capable of __showing current date and time__, __weather forecast__, __measure heart rate__, and __functions as a pedometer__. Pretty cool!

### Tutorials :memo:

<ins>__Tutorial 1: ML Data Preparation__</ins>  

In this tutorial we learned how to get our collected data, analyze and verify them to be used when constructing our Machine Learning Model later.  

We used a library called `glob` to make it easier for us to retreive the directory and folders, so we can effectively loop through each of our subjects and do what we need with each one of them.  

Then, we also needed to verify the sampling rates of our files. If it's too off from the actual sampling rate, we need to discard it. This is because __good data is important__, especially when we are using them to train our Machine Learning model.  

At the end of this tutorial, we have multiple functions which work together to retrieve our PPG data, clean (process) them, plot them for extra verification, and we're ready to start doing some ML training!  

<ins>__Tutorial 2: GMM HR Monitor__</ins>  

We learned how to train our model using the Gaussian Mixture Training (GMM), `GaussianMixture` from the `sklearn.mixture` module, verify it via looking at the Historgam Distribution, and how to perform validation on our training model using the __cross validation__ technique, specifically the __Leave-One-Subject-Out-Validation (LOSOV)__.  

The __Histogram Distribution Verification__ is essentially a tool for us to see if we're really fitting the training data with the GMM algorithm or not. We implemented the `plot_gaussian(weight, mu, var)` function as follows:  

```python
# Plot each component of the GMM as a separate Gaussian
def plot_gaussian(weight, mu, var):
  weight = float(weight)
  mu = float(mu)
  var = float(var)

  x = np.linspace(0, 1)
  y = weight * norm.pdf(x, mu, np.sqrt(var))
  plt.plot(x, y)
```

Then, using the histogram plot from matplotlib, `plt.hist`(), we compare it with the output of our `plot_gaussian` function to see if they make a good fit, like so:  

![imageOfGaussianAndHistPlotFromTuto2()  

Now that we have our labels, we need to tell our program how to look at these labels and identify heartbeat. The key to achieving this is catching the transition from 0 to 1, or vice versa, not both. We can do this very easily with the `np.diff()` method from the numpy library. This will give us an output with a bunch of 0's , -1's, and 1's, and now catching the transition is easy: we just look at places where the output says 1, which are our peaks. Then we do what we did in the previous lab: __count these peaks, then convert it to BPM__. In the tutorial, we put this into a function:  

```python
# Estimate the heart rate given GMM output labels
def estimate_hr(labels, num_samples, fs):
  peaks = np.diff(labels, prepend=0) == 1
  count = sum(peaks)
  seconds = num_samples / fs
  hr = count / seconds * 60 # 60s in a minute
  return hr, peaks
```

The next thing to do is the validation process via __LOSOV__ technique. It's not complicated as its name, we just need to follow a process:  

- Take all of our training data, but keep one subject.
- For each PPG file, process it, append it to the training vector.
- Train the GMM using that training vector.
- Then remember the subject we excluded from step 1? Load its trials, process it, and use the GMM model we just trained to predict labels on this excluded subject.
- Next, we compute the estimated heart rate, with out function `estimate_hr()`
- Repeat everything for the next subjects, until all of them have been gone through.  

### Challenges :desktop_computer:

<ins>__Challenge 1: GMM Performance__</ins>  

In this challenge, we were tasked to analyze the performance of our Machine Learning Model. I am going to document this challenge in two parts: __Analysis__, & __Implementation__.  

<ins>Analysis: </ins>  

I take, mainly, 3 approaches:  

1. Evaluate the __Root Mean Squared Error (RMSE)__, and observe the 3 key analysis dimensions: __bias__, __correlation__, __precision__
2. Do we actually have a good model, __how do we determine the best model__?
3. What could caused our model to give us the __result below our expectation__?  

> First, we have an RMSE of __14.61__. That is not a really good RMSE to begin with. The following is all 25 plots:  

<!--- tip: write in concise readable paragraphs -->  
<table>
  <tr>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig1.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig2.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig3.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig4.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig5.png"  alt="1" width = 300px height = 250px ></td>
  </tr> 
  <tr>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig6.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig7.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig8.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig9.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig10.png"  alt="1" width = 300px height = 250px ></td>
  </tr>
  <tr>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig11.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig12.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig13.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig14.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig15.png"  alt="1" width = 300px height = 250px ></td>
  </tr> 
  <tr>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig16.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig17.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig18.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig19.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig20.png"  alt="1" width = 300px height = 250px ></td>
  </tr>
  <tr>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig21.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig22.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig23.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig24.png"  alt="1" width = 300px height = 250px ></td>
    <td> <img src="https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig25.png"  alt="1" width = 300px height = 250px ></td>
  </tr> 
</table>  

Let's grab one with a pretty __good__ precision: *Figure 19*  

![fig19](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig19.png)  

As one can see, __only two__ predicted heart rate did not match the ground truth. Awesome!  

However, we know the majority of the plots clearly have problems with being bias, terrible correlation, and not-so-good precision. Let's take a plot for each one and (__try to__) justify why it has bias, loose correlation, and low precison, respectively.  

__Bias__: *Figure 2*  

![fig2](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig2.png)  

Clearly the model over predicted every heart rate for that particular subject :frowning_face: .  

__Low Correlation__: *Figure 8*  

![fig8](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig8.png)  

On first glance, it looks terrible, most of them are scattered. But it actually isn't that bad if we look at the scale. 72 (ground truth) and 78 (precited) aren't too far from each other. Regardless, it's still pretty off.  

__Low Precision__: *Figure 24*  

![fig24](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/figures/fig24.png)  

I think the precision is off for this one due to the predictions plot are scattered, some are off the ground truth line, some are just under (actually, not too bad honestly :nerd_face:).  

> Do we actually have a good model, __how do we determine the best model__?  

We can use __Bayesian Information Criterion (BIC)__ or __Akaike Information Criterion__ (they should both roughly be the same), and fortunately the gaussian mixture module from `sklearn` already has this implemented as can be seen [here](https://github.com/scikit-learn/scikit-learn/blob/0fb307bf3/sklearn/mixture/_gaussian_mixture.py#L727) (I'll talk about how I implemented it in `challenge1_gmm_performance.py` under __implementation__):  

```python
def bic(self, X):
    """Bayesian information criterion for the current model on the input X.
    Parameters
    ----------
    X : array of shape (n_samples, n_dimensions)
    Returns
    -------
    bic : float
        The lower the better.
    """
    return (-2 * self.score(X) * X.shape[0] +
            self._n_parameters() * np.log(X.shape[0]))

def aic(self, X):
    """Akaike information criterion for the current model on the input X.
    Parameters
    ----------
    X : array of shape (n_samples, n_dimensions)
    Returns
    -------
    aic : float
        The lower the better.
    """
    return -2 * self.score(X) * X.shape[0] + 2 * self._n_parameters()
```

As mentioned in the doctrings, we know the best model would have the __lowest BIC/AIC__, let's plot them, all 25 models:  

![bic_aic](https://github.com/UCSD-ECE16/ece-16-fall-2021-fadli0029/blob/main/Python/Lab7/images/aic_bic_PLOT.png)  

We have a pretty good model here, since the difference between max BIC/AIC and lowest BIC/AIC is pretty high if we normailize it (yes, forgive me for not normalizing before plotting :frowning_face:)  

Finally,  

> What could caused our model to give us the __result below our expectation__?  

Well, to be honest, i don't know :clown_face:. Just kidding! :ghost: (Actually, I don't even know if I'm correct). So, if we look at the 25 plots, we can deduce __most of heart beat are overestimated by our model__. Why? I would think it's because the model assume tiny peaks to be a heart beat in some cases. I think __better dsp technique__ and __A LOT MORE__ data will yield better model.  

<ins>Implementation: </ins>  

How I implemented the __RMSE__ plotting:  

```python
# plot from k to N of estimates and ground truth values heart rate
# x1   : ground truth,
# x2   : estimates
# k    : slicing begins at k
# num  : to save figure number
# show : if true, show plot. Default is false.
def plotRMSE(x1, x2, N, k, num, show=False):
  rmse = str(round(mean_squared_error(x1, x2, squared=False), 2))
  y = np.arange(len(x1[k:N]))
  # add rmse on legend
  plt.plot([], [], ' ', label="rsme: "+rmse)
  plt.scatter(y, sorted(x2[k:N]), color="blue", label="predicted")
  plt.plot(y, sorted(x1[k:N]), color="red", label="ground truth")
  plt.legend()
  plt.savefig("./images/figures/fig"+str(num)+".png")
  plt.clf()
  if (show):
    plt.show()
```

In the `__main__` program, I declare two list `hr_val` and `hrEst_val`, and keep appending the ground truth and estimates for each subject to them. The `mean_squared_error` is from `sklearn.metrics`. Then, I save all the figures in the `figures` folder. After trainings and estimations are done, I plot every 10 window of both the ground truth and estimates like so:  

```python
n = 11
k = 0
for i in range (1, 26):
  plotRMSE(hr_val, hrEst_val, n, k, i)
  i+=1
  n+=10
  k+=10
```

How I implemented the __BIC/AIC__ plotting:  

```python
def plotBarBIC_AIC(aBic, aAic):
  thewidth = 0.25
  fig = plt.subplots(figsize=(12,8))
  bar1 = np.arange(len(aBic))
  bar2 = [x+thewidth for x in bar1]

  min_BIC = round(min(aBic), 2)
  min_AIC = round(min(aAic), 2)
  diff_BIC = round(max(aBic)-min(aBic), 2)
  diff_AIC = round(max(aAic)-min(aAic), 2)

  # add min bic and aic on legend
  plt.plot([], [], ' ', label="min BIC: "+str(min_BIC))
  plt.plot([], [], ' ', label="min AIC: "+str(min_AIC))
  plt.plot([], [], ' ', label="max - min BIC: "+str(diff_BIC))
  plt.plot([], [], ' ', label="max - min AIC: "+str(diff_AIC))
  plt.bar(bar1, aBic, color='navy', width=thewidth, edgecolor='grey', label='BIC')
  plt.bar(bar2, aAic, color='darkorange', width=thewidth, edgecolor='grey', label='AIC')

  plt.xlabel('Model', fontweight='bold', fontsize=15)
  plt.ylabel('BIC/AIC Score', fontweight='bold', fontsize=15)
  plt.xticks([r+thewidth for r in range(len(aBic))], \
             ['M1', 'M2', 'M3', 'M4', 'M5', \
              'M6', 'M7', 'M8', 'M9', 'M10', \
              'M11', 'M12', 'M13', 'M14', 'M15', \
              'M16', 'M17', 'M18', 'M19', 'M20', \
              'M21', 'M22', 'M23', 'M24', 'M25', \
              ])

  plt.legend()
  plt.show()
```

This is just a regular bar plotting, with the min of both BIC and AIC in the legend. In the `__main__`, I keep the new gmm model generated after every fitting to two lists, `bic`, and `aic`:  

```python
train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
gmm = GMM(n_components=2).fit(train_data)
bic.append(abs(gmm.bic(train_data)))
aic.append(abs(gmm.aic(train_data)))
```

<ins>__Challenge 2: GMM HR Monitor__</ins>  

In this challenge, we were tasked to make a heart monitor using a GMM-based peak detection. Instead of just using processing like in the previous lab, we are going to let our trained model to predict labels, and then we determine heart rate from there.  

For this challenge, I added a new module in our `ECE16Lib` called, `GMMTrain.py`. It contains all the necessary methods to help me construct the required `train()` method. Most of the methods are from the previous challenge and tutorial 2, namely: `get_subjects()`, `get_data()`, `get_hr()`, `estimate_fs()`, `plot_gaussian()`, `estimate_hr()`, and `process_for_gmm()`. The `train()` method in `HRMonitor.py` class make use of these methods as follows:  

```python
def train(self, subjects, directory, fs):
  print("Training ^_^")
  for exclude in subjects:
    train_data = np.array([])
    for subject in subjects:
      for trial in range(1,11):
        t, ppg, hr, fs_est = gmmt.get_data(directory, subject, trial, fs)

        if subject != exclude:
          train_data = np.append(train_data, gmmt.process_for_gmm(ppg))

    # Train the GMM
    train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
    gmm = GMM(n_components=2).fit(train_data)

    # Test the GMM on excluded subject
    for trial in range(1,11):
      t, ppg, hr, fs_est = gmmt.get_data(directory, exclude, trial, fs)
      test_data = gmmt.process_for_gmm(ppg)
      labels = gmm.predict(test_data.reshape(-1,1))
      hr_est, peaks = gmmt.estimate_hr(labels, len(ppg), fs)

    dump(gmm, "gmm_model")

  print("Done Training! Model saved as \"gmm_model\"")
```

A few things to note here are:  

- I use methods like `get_data()`, `process_for_gmm()`, and `estimate_hr()` from the `GMMTrain.py` module.
- Instead of using `pickle`, I use `dump` which essentially should give the same functionality of saving and loading ML model for later use, but I just think `dump` is easier to use.
- What this function does is basically train the data using the GMM training, and then validate it via __LOSOV__ as taught in tutorial 2.
- Then it saves the model as __"gmm_model"__ in the same directory. This way, I only need to train once!

Now, I need a way to call this method or just load the model later when predicting a user's heart rate. Here's how I implemented the `predict()` method:  

```python
def predict(self, subjects, directory, ppgData, freq):
  target_data = gmmt.process_for_gmm(ppgData)
  if (exists("gmm_model")):
    print("Model already exists, sweet! No training needed")
    gmmModel = load("gmm_model")
    labels = gmmModel.predict(target_data.reshape(-1,1))
    hr_est, peaks = gmmt.estimate_hr(labels, len(ppgData), freq)
  else:
    self.train(subjects, directory, freq)
    # recursion in action
    hr_est, peaks = self.predict(subjects, directory, ppgData, freq)

  return hr_est, peaks
```

Things to note:  

- First, I process the PPG data coming in, then I check if the model exists in the directory using the `exists()` method from the `os.path` library.
- If it exists, then no training is needed. So, I just load the model, and call the `predict()` method, then estimate the heart rate with `estimate_hr()`.
- If it doesn't exists, I call the `train()` method, and make a recursive call to the `predict()` method again. This call should now cause the program to enter the `if` block instead because the gmm model should now exists.  

With all these methods done, in `challenge2_gmm_hr.py`, I use the same logic as before to retrieve the PPG data, process and predict every 500 samples, sampled at 50hz. Then, I instantiate a `HRMonitor(500, 50)` object, then call the `hr_monitor.predict()` method, then send the message (Heart rate predicted) back to the MCU with `comms.send_message()`. The implementation, as a code snippet, is as follows:  

Collecting data:  

```python
...
...

try:
  previous_time = time()
  while(True):
    sample = 0
    while (sample < num_samples):
      # get 500 samples, then only process data, and send bpm
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2) = message.split(',')
        except ValueError:  # if corrupted data, skip the sample
          continue

        times.add(int(m1))
        ppg.add(int(m2))
        sample += 1
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time
          comms.send_message("measuring")   # to refresh oled

        ...
        ...
```

Processing, and predicting heart rate:  

```python
...
...

data = np.column_stack([times, ppg])
t = data[:,0]
t = (t - t[0])/1e3 # make time range from 0-10 in seconds
ppgf = data[:,1]
hr_monitor = HRMonitor(500, 50)
hr, peaks = hr_monitor.predict(subjects, directory, ppgf, fs)
comms.send_message(str(round(hr, 2)))
# send bpm to MCU, round to 2dp
...
...
```

On the MCU side, there is not much changes needed. I added an `else if` block to catch if the Python program is still measuring, and an `else` block to catch if a heart rate value is sent. The implementation is as follows:  

```cpp
...
...
// still measuring BPM (i.e: not 500 samples yet)
else if(command == "measuring") {
  sending = true;
  writeDisplay("Heart Rate: ", 0, true, false);
  writeDisplay("measuring...", 1, true, false);
}

// received BPM measured from python
// print it out on the OLED
else {
  String HR = String(command);
  writeDisplay(HR.c_str(), 2, false, true);
}
...
...
```

[Click here to see it in action!](https://youtube.com/shorts/fEHHbC-SkIc?feature=share)  

Oh btw, I just can't help to show how aesthetically pleasing my workstation is (don't maximize, it gets blurry lol, not my fault):  
<img src="https://media.giphy.com/media/QECxGVmCDc6Qd2eVzU/giphy.gif" width="600" height="400"/>  

<ins>__Challenge 3: Complete Wearable!__</ins>  

Since challenge 3 is really like __The Ultimate Challenge__ where we build a complete wearable, I will document this challenge in two parts:  

1. What I made, and what are the functionalities.  
2. The technical parts of the 'project', the codes, state machines and all that.  

<ins> What I made: </ins>  

As mentioned in challenge 3 writeup, I made a wearable that displays __time__ and __date__, __weather forecast__, measures __heart rate__ live, and a working __pedometer__.  

And the following are the other elements underlined in the Write-Up and the roles they play in the wearable.  

- [x] __Incorporating the button:__  \
If a user clicked the button, it will toggle from showing today's date to showing current weather, and vice versa.
- [x] __Adding the Buzzer to the wearable:__  \
The buzzer will beep everytime the button is pushed. 
- [x] __Showing weather forecast on OLED:__  \
The user will be able to get real-time weather forecast shown on the OLED.  

*Scroll to the bottom to click on the link which will redirect you to the demo. There are two videos.*  

</br>

<ins> The technicalities: </ins>  

- __Collecting and Processing data:__
  - There are 5 data I needed to collect and process: __timestamps__, __ppg__, acceleromter axis __ax__, __ay__, and __az__.  
  - For the __ppg__ data, I used the Machine Learning approach, using GMM model, to predict heart rate. This means, I reuse the `GMMTrain.py` module from challenge 2 previously, to call the `get_subjects()` method. Then I use the `predict()` method from our `HRMonitor.py` module, to retrieve (or train if it doesn't exists) the ML model. 
  - Similar to previous labs, I __process and predict__ every 500 samples.
  - As for the __accelerometer__ data, I use the `process()` method from our `Pedometer.py` module. And this processing happens every one second.  
  
The following is a code snippet (note: the source code itself is much cleaner):  

```python
...
### HeartRate, GMM ###
directory = "./data"
subjects = gmmt.get_subjects(directory)

### PEDOMETER ###
ped = Pedometer(num_samples, fs, [])
...
...
try:
  ...
  ...
  ...
  while(True):
    ...
    ...
    if message is not None:
      try:
        # in the order: t, ppg, ax, ay, az 
        (m1, m2, m3, m4, m5) = message.split(',')
      except ValueError:  # if corrupted data, skip the sample
        continue

      ### collecting data for PPG & Pedometer ###
      ped.add(int(m3),int(m4),int(m5))

      if (sample < num_samples):
        times.add(int(m1))
        ppg.add(int(m2))
        sample += 1

      ### PPG processing ###
      if (sample == num_samples):
        data = np.column_stack([times, ppg])
        t = data[:,0]
        t = (t - t[0])/1e3 # make time range from 0-10 in seconds
        ppgf = data[:,1]
        hr_monitor = HRMonitor(500, 50)
        hr, peaks = hr_monitor.predict(subjects, directory, ppgf, fs)
        last_hr = hr
        sample = 0 # reset sample to 0

      current_time = time()
      if (current_time - previous_time > refresh_time):
        previous_time = current_time

        # Pedometer processing
        steps, peaks, filtered = ped.process()
        ...
        ...
```

The Arduino part is one that we're very familiar with:  

```cpp
...
...
if(sending && sampleSensors()) {
  String response = String(sampleTime) + ",";
  response += String(ppg) + ","; 
  response += String(ax) + "," + String(ay) + "," + String(az);
  sendMessage(response);
}
...
...
```

</br>

- __Getting the weather data:__  
  - To retrieve the weather data, I use the `OWM` api, and initialize it like such:
  - `owm = OWM('dd25a8ed48b2b2b12d7a71c45e5ca1eb').weather_manager()`
  - Then, i get the weather status using the `weather_at_place()` method, and `.status`, and then the `.temperature()` method.  
 
The following is a code snippet (note: the source code itself is much cleaner):  
```python
### Init Weather API ###
owm = OWM('dd25a8ed48b2b2b12d7a71c45e5ca1eb').weather_manager()

try:
  ...
  ...
  # retrieving/updating weather data
  fade = owm.weather_at_place('san diego,ca,us')
  weather = fade.weather
  final_output = weather.status + ' ' + str(weather.temperature('celsius')['temp_max'])
  ...
  ...
```

</br> 

- __Receiving current Date & Time:__  
  - To receive current data & time, I use the `datetime` library.
  - Then the implementation is straightforward:  

```python
# Updating Time & Date
theTime = datetime.datetime.now().strftime("%H:%M:%S")
theDate = datetime.date.today()
outputDate = theDate.strftime("%b-%d- %Y")
```

</br> 

- __Detecting button pressed & Buzzing the buzzer:__  
  - To detect if a button is pressed, I use the new method `rec_msg()` i added in the `Communication.py` module. What it does is it reads message that the MCU prints.
  - Then if it is pressed, the buzzer will be set to `HIGH` for 0.5 seconds achieved using the `secPassed()` method.
  - On the Arduino side:
```cpp
...
...
unsigned long currentMillis = millis();

/*BUTTON STATE CHECKING*/
currentState = !digitalRead(buttonPin);
if (currentState != lastButtonState) { 
  if (oldStatus == true) {
    sendDate = false;
    buzzIt = false;
  }
  if (oldStatus == false) {
    sendDate = true;
    buzzIt = true;
  }
}
lastButtonState = currentState;

if (sendDate == true) {
  Serial.print('m');
}

if (buzzIt == true) {
  // buzz the buzzer for x second(s)
  digitalWrite(buzzerPin, HIGH);
}
if (secPassed(currentMillis, 500)) {
  digitalWrite(buzzerPin, LOW);
}
oldStatus = sendDate;
```

The `secPassed()` implementation is as follows:  
```cpp
long prevMillis = 0;
bool secPassed(unsigned long nowMillis, const long sec) {
	bool stat = false;
	if (nowMillis - prevMillis >= sec) {
		stat = true;
		prevMillis = nowMillis;
	}
	return stat;
}
```

On the python side:  

```python
anotherMsg = comms.rec_msg()
if (str(anotherMsg) == "b'm'"): # button is pressed
  if (lastState == True):
    printDate = False
  elif (lastState == False):
    printDate = True

lastState = printDate # update last state
```

</br>

- __Sending data back to the MCU:__  
  - Now, we need a way to send all those processed data, time & date, weather forecast, and etc.
  - Keep in mind that the Date is only displayed if the button is pressed, and same goes to the weather forecast. So, I put all these messages to be sent to the MCU in an `if` `else` block.
  - Then clear the `mcuInput` string for the next loop iteration, so that it can be updated again with new data to be displayed.  

```python
while(True):
  mcuInput = ""
  ...
  ...
  lastState = printDate # update last state

  if message is not None:
    try:
      ...
    except:
      ...
      ...
      ...
    current_time = time()
    if (current_time - previous_time > refresh_time):
      previous_time = current_time
      ...
      ...
      ### Sending data to MCU ###
      if (printDate):
        # button was pressed, so display date instead of weather
        mcuInput += "h"+str(round(last_hr,2)) + \
                    "x"+str(steps) + \
                    "t"+(theTime) + \
                    "q"+outputDate+"z"
      else:
        mcuInput += "h"+str(round(last_hr,2)) + \
                    "x"+str(steps) + \
                    "t"+(theTime) + \
                    "q"+final_output+"z"

      comms.send_message(mcuInput)
```

Now, on the Arduino side:
```cpp
...
...
else {
  String val = String(command);

  String hr = "";             // 'h'
  String mystep = "";         // 'x'
  String time = "";           // 't'
  String weather_date = "";   // 'q'

  int i, j, k, l;
  if (val.charAt(0) == 'h') {
    for (i = 1; val[i] != 'x'; i++) {
      hr += val[i];
    }
    for (j = i+1; val[j] != 't'; j++) {
      mystep += val[j];
    }
    for (k = j+1; val[k] != 'q'; k++) {
      time += val[k];
    }
    for (l = k+1; val[l] != 'z'; l++) {
      weather_date += val[l];
    }
  }

  String hr_out = "Heart Rate: " + hr;
  String mystep_out = "Steps Count: " + mystep;
  String time_out = "Time: " + time;
  String weather_date_out = "^_^ " + weather_date;
  writeDisplay(hr_out.c_str(), 0, false, true);
  writeDisplay(mystep_out.c_str(), 1, false, true);
  writeDisplay(time_out.c_str(), 2, false, true);
  writeDisplay(weather_date_out.c_str(), 3, false, true);
}
...
...
```

Here's a video of the wearable working! (Disclaimer: I don't walk like that, it's for the sake of "correct" pedometer reading :clown_face: ):  

- [Heartbeat, Buzzer, Button, etc.](https://youtube.com/shorts/9Yv3KwHyzlk?feature=share)
- [Pedometer, and everything alltogether.](https://youtu.be/dkgu7mZFstg)
