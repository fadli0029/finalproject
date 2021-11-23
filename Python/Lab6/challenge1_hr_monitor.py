import ECE16Lib.HRMonitor as hrm
import matplotlib.pyplot as plt
import ECE16Lib.DSP as filt
import scipy.signal as sig
from scipy import stats
import numpy as np
import os


"""
  function to filter ppg:
    detrend->moving_average->gradient->normalize

    then find count and peaks with:
      count, peaks = filt.count_peaks()

    return: count, peaks
"""
def process(x):
  x = filt.detrend(x, 25)
  x = filt.moving_average(x, 5)
  x = filt.gradient(x)
  x = filt.normalize(x)

  thresh = 0.6
  count, peaks = filt.count_peaks(x, thresh, 1)

  return count, peaks


"""
  function to evaluate accuracy of hr monitor:
    compares estimates and ground truth, analyze
    using Bland-Altman Plot
"""
def eval_hr_monitor(grnd_list, est_list):

    grnd = np.array(grnd_list)
    est = np.array(est_list)

    [R,p] = stats.pearsonr(grnd, est) # correlation coefficient

    plt.figure(1)
    plt.clf()

    # Correlation Plot
    plt.subplot(211)
    plt.plot(est, est)
    plt.scatter(grnd, est)

    plt.ylabel("Estimated HR (BPM)")
    plt.xlabel("Reference HR (BPM)")
    plt.title("Correlation Plot: Coefficient (R) = {:.2f}".format(R))

    # Bland-Altman Plot
    avg = [(a+b)/2 for a, b in zip(grnd, est)]
    # take the average between each element of the ground_truth and
    # estimates arrays and you should end up with another array

    dif = grnd - est
    # take the difference between ground_truth and estimates

    std = np.std(dif)
    # get the standard deviation of the difference (using np.std)

    bias = np.mean(dif)
    # get the mean value of the difference

    upper_std = bias + 1.96*std
    # the bias plus 1.96 times the std

    lower_std = bias - 1.96*std
    # the bias minus 1.96 times the std

    plt.subplot(212)
    plt.scatter(avg, dif)

    plt.plot(avg, len(avg)*[bias])
    plt.plot(avg, len(avg)*[upper_std])
    plt.plot(avg, len(avg)*[lower_std])

    plt.legend(["Mean Value: {:.2f}".format(bias),
      "Upper bound (+1.96*STD): {:.2f}".format(upper_std),
      "Lower bound (-1.96*STD): {:.2f}".format(lower_std)
    ])

    plt.ylabel("Difference between estimates and ground_truth (BPM)")
    plt.xlabel("Average of estimates and ground_truth (BPM)")
    plt.title("Bland-Altman Plot")
    plt.show()


# MAIN CODE:
if __name__ == "__main__":

  # get/list all csv files in the path
  path = './data/a16468481/'
  files = os.listdir(path)
  thefiles = []
  for f in files:
    thefiles.append(f)
    # append all the file names inside thefiles list.

  thefiles.sort()
  # sort it alphabetically
  # because my peaks_count list is sorted
  # alphabetically


  estimates = []
  peaks_count = [12,14,11,16,18,14,15,15,15,15,18,14,16,16,16] # for ground truth
  ground_truth = []
  for item in peaks_count:
    ground_truth.append((item/10)*60)
    # bpm for ground truth

  for f in thefiles:
    data = np.genfromtxt(path+f, delimiter=",")
    t = data[:,0]
    t = (t - t[0])/1e3
    ppg = data[:,1]
    count, peaks = process(ppg)
    avg_beat_time = np.mean(np.diff(t[peaks]))
    bpm = 60/avg_beat_time
    estimates.append(bpm)

  eval_hr_monitor(ground_truth, estimates)
