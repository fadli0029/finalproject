from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
import ECE16Lib.DSP as filt
import ECE16Lib.GMMTrain as gmmt
from sklearn.mixture import GaussianMixture as GMM
from joblib import dump, load
from os.path import exists
import numpy as np

"""
A class to enable a simple heart rate monitor
"""
class HRMonitor:
  """
  Encapsulated class attributes (with default values)
  """
  __hr = 0           # the current heart rate
  __time = None      # CircularList containing the time vector
  __ppg = None       # CircularList containing the raw signal
  __filtered = None  # CircularList containing filtered signal
  __num_samples = 0  # The length of data maintained
  __new_samples = 0  # How many new samples exist to process
  __fs = 0           # Sampling rate in Hz
  __thresh = 0.6     # Threshold from Tutorial 2

  """
  Initialize the class instance
  """
  def __init__(self, num_samples, fs, times=[], data=[]):
    self.__hr = 0
    self.__num_samples = num_samples
    self.__fs = fs
    self.__time = CircularList(data, num_samples)
    self.__ppg = CircularList(data, num_samples)
    self.__filtered = CircularList([], num_samples)

  def getPPG(self):
    ppg = self.__ppg
    return ppg

  def getTime(self):
    time = self.__time
    return time

  def getFiltered(self):
    filtered = self.__filtered
    return filtered

  """
  Add new samples to the data buffer
  Handles both integers and vectors!
  """
  def add(self, t, x):
    if isinstance(t, np.ndarray):
      t = t.tolist()
    if isinstance(x, np.ndarray):
      x = x.tolist()


    if isinstance(x, int):
      self.__new_samples += 1
    else:
      self.__new_samples += len(x)

    self.__time.add(t)
    self.__ppg.add(x)

  """
  Compute the average heart rate over the peaks
  """
  def compute_heart_rate(self, peaks):
    t = np.array(self.__time)
    return 60 / np.mean(np.diff(t[peaks]))

  """
  Process the new data to update step count
  """
  def process(self):
    # Grab only the new samples into a NumPy array
    x = np.array(self.__ppg[ -self.__new_samples: ])

    # Filter the signal (feel free to customize!)
    x = filt.detrend(x, 25)
    x = filt.moving_average(x, 5)
    x = filt.gradient(x)
    x = filt.normalize(x)

    # Store the filtered data
    self.__filtered.add(x.tolist())

    # Find the peaks in the filtered data
    _, peaks = filt.count_peaks(self.__filtered, self.__thresh, 1)

    # Update the step count and reset the new sample count
    self.__hr = self.compute_heart_rate(peaks)
    self.__new_samples = 0

    # Return the heart rate, peak locations, and filtered data
    return self.__hr, peaks, np.array(self.__filtered)

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


  def predict(self, subjects, directory, ppgData, freq):
    target_data = gmmt.process_for_gmm(ppgData) 
    if (exists("gmm_model")):
      print("Model already exists, sweet! No training needed")
      gmmModel = load("gmm_model")
      labels = gmmModel.predict(target_data.reshape(-1,1))
      hr_est, peaks = gmmt.estimate_hr(labels, len(ppgData), freq)
    else:
      self.train(subjects, directory, freq)
      # recursion technique in action hehehe
      hr_est, peaks = self.predict(subjects, directory, ppgData, freq)

    return hr_est, peaks

  """
  Clear the data buffers and step count
  """
  def reset(self):
    self.__hr = 0
    self.__time.clear()
    self.__ppg.clear()
    self.__filtered.clear()
