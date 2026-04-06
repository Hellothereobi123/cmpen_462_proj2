import scipy as sp
from scipy import fft
import numpy as np
def get_AP_data(filename):
    # read data from file
    new_file = open(filename, "r")
    data = new_file.read().split("\n")
    new_data = []
    for i in range(len(data)):
        if(data[i] != ""):
            new_data.append(complex(data[i].replace("i", "j")))
        #print(i)
    #print(data[1])
    return np.array(new_data)
def doppler_velocity(frequency, f0=5.8e9, direction_vect):
    c=3e8
    # calculate velocity using doppler shift formula
    return (frequency * c) / (2 * f0)
### (Step 1 AP 1) ###

freq_array = np.fft.fftfreq(5000000, d=0.000001) # FFT frequency array based on index

get_ap1 = get_AP_data("AP1.txt") #gets the signal data from the AP1.txt file, which contains the signal data received by the reciever from the first access point (AP)
print(get_ap1.shape)
print(get_ap1[6])
ap1_freq_data = sp.fft.fft(np.array(get_ap1).T) #performs a fast fourier transform on the signal data to convert it from the time domain to the frequency domain
ap1_mag = np.abs(ap1_freq_data) #calculates the magnitude of the frequency domain data, which is used to find the peaks in the frequency domain
ap1_peaks_maxval = np.argmax(ap1_mag) #finds the peak index in the frequency domain data. #converts the peaks to a numpy array for easier manipulation
ap1_doppler_freq = freq_array[ap1_peaks_maxval] #finds the frequency corresponding to the peak index, which is used to calculate the velocity of the reciever relative to the transmitter using the doppler shift formula



# steps per AP (step 1)
    # read data
    # perform fft to convert to frequency domain
    # find peaks in frequency domain, and determine the frequency of the peaks
    # plug into doppler shift formula to find velocity of the reciever relative to the transmitter
# repeat for all APs
# use least squares to find the relative position of the reciever


