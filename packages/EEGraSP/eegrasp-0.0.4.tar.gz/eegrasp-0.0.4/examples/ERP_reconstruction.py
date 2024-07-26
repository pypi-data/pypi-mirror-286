""""
Example on how to interpolate missing channels.
"""

# %% Import libraries
import numpy as np
import matplotlib.pyplot as plt
import mne
from eegrasp import EEGrasp

# %% Load Electrode montage and dataset
subjects = np.arange(1, 10)
runs = [4, 8, 12]

# Download eegbci dataset through MNE
# Comment the following line if already downloaded

raw_fnames = [mne.datasets.eegbci.load_data(
    s, runs, path='datasets') for s in subjects]
raw_fnames = np.reshape(raw_fnames, -1)
raws = [mne.io.read_raw_edf(f, preload=True) for f in raw_fnames]
raw = mne.concatenate_raws(raws)
mne.datasets.eegbci.standardize(raw)
raw.annotations.rename(dict(T1="left", T2="right"))


montage = mne.channels.make_standard_montage('standard_1005')
raw.set_montage(montage)
eeg_pos = np.array(
    [pos for _, pos in raw.get_montage().get_positions()['ch_pos'].items()])
ch_names = montage.ch_names

# %% Filter data and extract events
L_FREQ = 1  # Hz
H_FREQ = 30  # Hz
raw.filter(L_FREQ, H_FREQ, fir_design='firwin', skip_by_annotation='edge')
raw, ref_data = mne.set_eeg_reference(raw)

events, events_id = mne.events_from_annotations(raw)

# %% Epoch data
# Exclude bad channels
TMIN, TMAX = -1.0, 3.0
picks = mne.pick_types(raw.info, meg=False, eeg=True,
                       stim=False, eog=False, exclude="bads")
epochs = mne.Epochs(raw, events, events_id,
                    picks=picks, tmin=TMIN,
                    tmax=TMAX, baseline=(-1, 0),
                    detrend=1)

# %%
left = epochs['left']
erp_left = left.average()

right = epochs['right']
erp_right = right.average()

# Use only data on the Left condition to find
# the best distance (epsilon) value
data = erp_left.get_data()

# %% Fit to data

# 1. Define index of the missing channel
MISSING_IDX = 5
# 2. Initialize instance of EEGrasp
eegsp = EEGrasp(data, eeg_pos, ch_names)
# 3. Compute the electrode distance matrix
dist_mat = eegsp.compute_distance(normalize=True)
# 4. Find the best parameter for the channel
results = eegsp.fit_sigma(missing_idx=MISSING_IDX, epsilon=0.5,
                          min_sigma=0.01, max_sigma=0.5, step=0.01)

# %% Plot error graph and results of the interpolation

error = results['error']
best_idx = np.argmin(error[~np.isnan(error)])
reconstructed_signal = results['signal'][MISSING_IDX, :]
best_sigma = results['best_sigma']
vdistances = results['sigma']

plt.subplot(211)
plt.plot(vdistances, error, color='black')
plt.scatter(vdistances, error, color='teal', marker='x',
            alpha=0.5)
plt.scatter(best_sigma,
            error[vdistances == best_sigma],
            color='red')
plt.xlabel(r'$\sigma$')
plt.ylabel(r'RMSE')
plt.title('Error')

plt.subplot(212)
plt.title('Best Reconstruction')
plt.plot(reconstructed_signal, label='Reconstructed Data')
plt.plot(data[MISSING_IDX, :], label='Original Data')
plt.xlabel('samples')
plt.ylabel('Voltage')
plt.legend()

plt.tight_layout()
plt.show()

# %% Interpolate right ERP based on the left channel
new_data = erp_right.get_data()
# Delete information from the missing channel
new_data[MISSING_IDX, :] = np.nan

# Interpolate channel
interpolated = eegsp.interpolate_channel(data=new_data,
                                         missing_idx=MISSING_IDX)

# %% Plot Interpolated Channel
original = erp_right.get_data()
plt.plot(interpolated[MISSING_IDX, :],
         label='Interpolated Data', color='purple')
plt.plot(original[MISSING_IDX, :], label='Original Data', color='teal')
plt.xlabel('Samples')
plt.ylabel('Voltage')
plt.legend()
plt.show()
