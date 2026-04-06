import scipy as sp
from scipy import fft
import numpy as np


# Helper functions 
#######################################################################################################################################
def get_input_data(filename):
    new_file = open(filename, "r")
    client_location = new_file.readline().split(" ")
    for i in range(len(client_location)):
        client_location[i] = float(client_location[i])
    num_APs = int(new_file.readline())
    ret_tuple = (client_location, num_APs)
    for i in range(num_APs):
        AP_location = new_file.readline().split(" ")
        for j in range(len(AP_location)):
            AP_location[j] = float(AP_location[j])
        ret_tuple += (AP_location,)
    return ret_tuple 

def get_AP_data(filename):
    # read data from file
    new_file = open(filename, "r")
    data = new_file.read().split("\n")
    new_data = []
    for i in range(len(data)):
        if(data[i] != ""):
            new_data.append(complex(data[i].replace("i", "j")))
    return np.array(new_data)

def doppler_velocity(frequency, f0=5.8e9):#, unit_vector):
    c=3e8
    # calculate velocity using doppler shift formula
    return (frequency * c) / (2 * f0)

def get_peak_frequency(num_APs, freq_array):
    freq_list = []
    for i in range(num_APs):
        get_ap1 = get_AP_data(f"AP{i+1}.txt") #gets the signal data from the A{i+1}.txt file, which contains the signal data received by the reciever from the {i+1}th access point (AP)
        ap1_freq_data = sp.fft.fft(np.array(get_ap1).T) #performs a fast fourier transform on the signal data to convert it from the time domain to the frequency domain
        ap1_mag = np.abs(ap1_freq_data) #calculates the magnitude of the frequency domain data, which is used to find the peaks in the frequency domain
        ap1_peaks_maxval = np.argmax(ap1_mag) #finds the peak index in the frequency domain data. #converts the peaks to a numpy array for easier manipulation
        ap1_doppler_freq = freq_array[ap1_peaks_maxval] #finds the frequency corresponding to the peak index, which is used to calculate the velocity of the reciever relative to the transmitter using the doppler shift formula
        freq_list.append(ap1_doppler_freq)
    return freq_list





# test 
################################################################################################################################################################################3
### (Step 1 AP 1) ###


# workflow
#   parse input.txt
#   load in each AP
#   FFT AP signals (already downsampled and downconverted)
#   find peak amp and convert into hz
#   compute unit vector of each AP
#   build system of equations 
#   use least square regression to estimate the velocity 
#   output the results

freq_array = np.fft.fftfreq(5000000, d=0.000001) # FFT frequency array based on index
input_data = get_input_data("./input.txt")
client_location = input_data[0] #tuple with client location, number of APs, and AP locations
num_APs = input_data[1] #number of APs in the environment
AP_locations = input_data[2:] #tuple with AP locations
'''
get_ap1 = get_AP_data("AP1.txt") #gets the signal data from the AP1.txt file, which contains the signal data received by the reciever from the first access point (AP)
print(get_ap1.shape)
print(get_ap1[6])
ap1_freq_data = sp.fft.fft(np.array(get_ap1).T) #performs a fast fourier transform on the signal data to convert it from the time domain to the frequency domain
ap1_mag = np.abs(ap1_freq_data) #calculates the magnitude of the frequency domain data, which is used to find the peaks in the frequency domain
ap1_peaks_maxval = np.argmax(ap1_mag) #finds the peak index in the frequency domain data. #converts the peaks to a numpy array for easier manipulation
ap1_doppler_freq = freq_array[ap1_peaks_maxval] #finds the frequency corresponding to the peak index, which is used to calculate the velocity of the reciever relative to the transmitter using the doppler shift formula
'''
freq_list = get_peak_frequency(num_APs, freq_array)
print(freq_list)



