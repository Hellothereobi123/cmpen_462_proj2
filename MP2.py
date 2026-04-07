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

def calc_relative_loc (num_AP, ap_list, client_loc):
    # must find the locations of each AP relative to the client to accurately calculate the angle they are at in realtion to the client 
    ap_relative_list = []
    for i in range(num_AP):
        ap_loc = ap_list[i]
        ap_relative_loc = []
        for j in range(len(ap_loc)):
            ap_relative_loc.append(ap_loc[j]-client_loc[j])
        ap_relative_list.append(ap_relative_loc)
    return ap_relative_list

def generate_unit_vector (num_AP, ap_relative_list):
    # generates the ap_locations unit vector as replacement for dopplers cos(angle)
    unit_vector_list = []
    for i in range(num_AP):
        ap_loc = np.array(ap_relative_list[i]) # convert into numpy vector 
        magnitude = np.linalg.norm(ap_loc) # Calculate magnitude
        unit_vector = ap_loc / magnitude # Compute unit vector
        unit_vector_list.append(unit_vector) # add to list of unit vectors 
    return unit_vector_list 

def doppler_const_multiplier (f0, unit_vector_list):
    c=3e8
    d_const= f0/c
    # calculates the const for doppler since the equation is dopper_shift= (f0/c)*(v*r)
    # we dont use cos(angle) becuase we are dealing with 3d so we use 3d vector r 

    return 

def approx_velocity (unit_vector_list, d_mult, ):
    pass


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

freq_array = np.fft.fftfreq(5000000, d=0.000001) # FFT frequency array based on index & converts the freq indexes to hz 
input_data = get_input_data("./input.txt")
client_location = input_data[0] #tuple with client location, number of APs, and AP locations
num_APs = input_data[1] #number of APs in the environment
AP_locations = list(input_data[2:]) #tuple with AP locations then converted to a list for ease of use 

print(client_location)
print(AP_locations)
print("\n")
AP_relative_list = calc_relative_loc(num_APs,AP_locations,client_location)
print(AP_relative_list)
print("\n")
unit_vector_list = generate_unit_vector(num_APs,AP_relative_list)
print(unit_vector_list)
print("\n")

'''
get_ap1 = get_AP_data("AP1.txt") #gets the signal data from the AP1.txt file, which contains the signal data received by the reciever from the first access point (AP)
print(get_ap1.shape)
print(get_ap1[6])
ap1_freq_data = sp.fft.fft(np.array(get_ap1).T) #performs a fast fourier transform on the signal data to convert it from the time domain to the frequency domain
ap1_mag = np.abs(ap1_freq_data) #calculates the magnitude of the frequency domain data, which is used to find the peaks in the frequency domain
ap1_peaks_maxval = np.argmax(ap1_mag) #finds the peak index in the frequency domain data. #converts the peaks to a numpy array for easier manipulation
ap1_doppler_freq = freq_array[ap1_peaks_maxval] #finds the frequency corresponding to the peak index, which is used to calculate the velocity of the reciever relative to the transmitter using the doppler shift formula
'''
#freq_list = get_peak_frequency(num_APs, freq_array)
#print(freq_list)



