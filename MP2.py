import scipy as sp
from scipy import fft
import numpy as np


# Helper functions 
#######################################################################################################################################
# extracts and parses the input.txt file 
def get_input_data(filename):
    new_file = open(filename, "r")
    client_location = new_file.readline().split(" ") # obtain the clients location
    for i in range(len(client_location)):
        client_location[i] = float(client_location[i]) # splits the coords and put into a list 

    num_APs = int(new_file.readline()) #obtain the number of APs
    ret_tuple = (client_location, num_APs)

    for i in range(num_APs):
        AP_location = new_file.readline().split(" ") # obtain the AP location and split 
        for j in range(len(AP_location)):
            AP_location[j] = float(AP_location[j]) #put values into list as floats 
        ret_tuple += (AP_location,)

    return ret_tuple # return tuple (client_location, number of ap, [ap_location])

# extracts AP data as list of data 
def get_AP_data(filename):
    new_file = open(filename, "r") 
    data = new_file.read().split("\n")
    new_data = []
    for i in range(len(data)):
        if(data[i] != ""):
            new_data.append(complex(data[i].replace("i", "j"))) # puts data in list as complex numbers 
    return np.array(new_data)

#find the peak freqency since peak frequency is equal to the doppler shift 
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

# must find the locations of each AP relative to the client to accurately calculate the angle they are at in realtion to the client
def calc_relative_loc (num_AP, ap_list, client_loc): 
    ap_relative_list = []
    for i in range(num_AP):
        ap_loc = ap_list[i]
        ap_relative_loc = []

        for j in range(len(ap_loc)):
            ap_relative_loc.append(ap_loc[j]-client_loc[j]) # subtracts the difference in location to get relative location to client 
        ap_relative_list.append(ap_relative_loc)
    return ap_relative_list


# generates the ap_locations unit vector as replacement for dopplers cos(angle)
def generate_unit_vector (num_AP, ap_relative_list):
    unit_vector_list = []
    for i in range(num_AP):
        ap_loc = np.array(ap_relative_list[i]) # convert into numpy vector 
        magnitude = np.linalg.norm(ap_loc) # Calculate magnitude
        unit_vector = ap_loc / magnitude # Compute unit vector
        
        unit_vector_list.append(unit_vector) # add to list of unit vectors 
    return unit_vector_list 

# multiply the constant into the matrix of unit vetcors 
def doppler_const_multiplier (f0, num_AP, unit_vector_list):
    c=3e8
    d_const= f0/c
    # calculates the const for doppler since the equation is dopper_shift= (f0/c)*(v*r)
    # we dont use cos(angle) becuase we are dealing with 3d so we use 3d vector r
    new_ap_list = []
    for i in range (num_AP):
        new_ap_list.append(d_const * unit_vector_list[i]) # multiply each value by d_const 
    return new_ap_list

# using the vetcor of doppler shift and the matrix of AP locations and least square to approximate the velocity 
def approx_velocity (coef_list, freq_list):
    new_coef_list = np.array(coef_list)
    new_freq_list = np.array(freq_list)
    solution, residuals, rank, singular_values = np.linalg.lstsq(new_coef_list, new_freq_list, rcond=None) # least sqaure function from numpy 

    return solution


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

# variables
carrier_freq=5.8e9
sampling_freq = 1000000
time = 5

freq_array = np.fft.fftfreq(sampling_freq*time, d=(1/sampling_freq)) # FFT frequency array based on index & converts the freq indexes to hz 
input_data = get_input_data("./input.txt")
client_location = input_data[0] #tuple with client location, number of APs, and AP locations
num_APs = input_data[1] #number of APs in the environment
AP_locations = list(input_data[2:]) #tuple with AP locations then converted to a list for ease of use 

freq_list = get_peak_frequency(num_APs, freq_array) # using the obtained freqency list find the peak which is the doppler shift 

AP_relative_list = calc_relative_loc(num_APs,AP_locations,client_location) # calculate each APs relative location
unit_vector_list = generate_unit_vector(num_APs,AP_relative_list) # use the relative locations to determine the unit vector 
coef_list = doppler_const_multiplier(carrier_freq, num_APs,unit_vector_list) # multiply other variables in the doppler equation

output = approx_velocity(coef_list, freq_list) # aclculate the velocity 
magnitude = np.linalg.norm(output) # Calculate magnitude

print( f"The 3d velocity is {output} and the speed is {magnitude}")



