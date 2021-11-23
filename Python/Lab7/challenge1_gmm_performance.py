# Import for searching a directory
import glob

# for fancy spinning wheel hehe ^_^
from halo import Halo

# The usual suspects
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt

# The GMM Import
from sklearn.mixture import GaussianMixture as GMM
from sklearn.metrics import mean_squared_error

# Import for Gaussian PDF
from scipy.stats import norm


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

# plot BIC and AIC
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


# Retrieve a list of the names of the subjects
def get_subjects(directory):
  filepaths = glob.glob(directory + "/*")
  return [filepath.split("/")[-1] for filepath in filepaths]

# Retrieve a data file, verifying its FS is reasonable
def get_data(directory, subject, trial, fs):
  search_key = "%s/%s/%s_%02d_*.csv" % (directory, subject, subject, trial)
  filepath = glob.glob(search_key)[0]
  t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
  t = (t-t[0])/1e3
  hr = get_hr(filepath, len(ppg), fs)

  fs_est = estimate_fs(t)
  if(fs_est < fs-1 or fs_est > fs):
    print("Bad data! FS=%.2f. Consider discarding: %s" % (fs_est,filepath))

  return t, ppg, hr, fs_est

# Estimate the heart rate from the user-reported peak count
def get_hr(filepath, num_samples, fs):
  count = int(filepath.split("_")[-1].split(".")[0])
  seconds = num_samples / fs
  return count / seconds * 60 # 60s in a minute

# Estimate the sampling rate from the time vector
def estimate_fs(times):
  return 1 / np.mean(np.diff(times))

# Filter the signal (as in the prior lab)
def process(x):
  x = filt.detrend(x, 25)
  x = filt.moving_average(x, 5)
  x = filt.gradient(x)
  return filt.normalize(x)

# Plot each component of the GMM as a separate Gaussian
def plot_gaussian(weight, mu, var):
  weight = float(weight)
  mu = float(mu)
  var = float(var)

  x = np.linspace(0, 1)
  y = weight * norm.pdf(x, mu, np.sqrt(var))
  plt.plot(x, y)

# Estimate the heart rate given GMM output labels
def estimate_hr(labels, num_samples, fs):
  peaks = np.diff(labels, prepend=0) == 1
  count = sum(peaks)
  seconds = num_samples / fs
  hr = count / seconds * 60 # 60s in a minute
  return hr, peaks

# Run the GMM with Leave-One-Subject-Out-Validation
if __name__ == "__main__":
  fs = 50
  directory = "./data"
  subjects = get_subjects(directory)

  bic = []
  aic = []
  hr_val = []
  hrEst_val = []

  spinner = Halo(text='Training...', spinner='monkey')
  spinner.start()

  for exclude in subjects:
    train_data = np.array([])
    for subject in subjects:
      for trial in range(1,11):
        t, ppg, hr, fs_est = get_data(directory, subject, trial, fs)

        if subject != exclude:
          train_data = np.append(train_data, process(ppg))

    # Train the GMM
    train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
    gmm = GMM(n_components=2).fit(train_data)
    bic.append(abs(gmm.bic(train_data)))
    aic.append(abs(gmm.aic(train_data)))

    # Test the GMM on excluded subject
    for trial in range(1,11):
      t, ppg, hr, fs_est = get_data(directory, exclude, trial, fs)
      test_data = process(ppg)

      labels = gmm.predict(test_data.reshape(-1,1))
      hr_est, peaks = estimate_hr(labels, len(ppg), fs)

      hr_val.append(round(hr, 2))
      hrEst_val.append(round(hr_est,2))

  spinner.stop()

  n = 11
  k = 0
  for i in range (1, 26):
    plotRMSE(hr_val, hrEst_val, n, k, i)
    i+=1
    n+=10
    k+=10

  plotBarBIC_AIC(bic, aic)

