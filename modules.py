'''Written by Nicki Lentz
All functions used for P7 project for group 7201 1.Semester sports tech AAU
will be saved in this module.
'''
import numpy as np
import pandas as pd
from scipy import signal as sig


def find_peaks(data, contraction=None):
        """Finding peaks, and using "contraction" to determine the movement

        Args:
            data ([vector]): [vector with positional data]
            contraction ([integer], optional): [0 == concentric (positive work)
                                                1 == Eccentric (negative work)]. Defaults to None.

        Returns:
            [2D array]: [first vector includex idx, second includes the value]
        """
        position = data['Position']
        if contraction == 0:
            thres = np.max(position) - (1.5 * np.std(position))
            max_peaks = sig.find_peaks(position, height=thres, distance=400)
        elif contraction == 1:
            inv_data = position * (-1)
            thres = np.max(inv_data) - (1.5 * np.std(inv_data))
            max_peaks = sig.find_peaks(inv_data, height=thres, distance=400)

        drop_values_under = np.arange(0, max_peaks[0][0], 1)
        drop_values_above = np.arange(max_peaks[0][-1]+1, data.index[-1]+1, 1)
        data.drop(drop_values_under, inplace=True)
        data.drop(drop_values_above, inplace=True)
                
        return [max_peaks, data]


def label_reps(data, peaks):
    """labeling which datas belong to which repetition, 
    based on peak values from sig.find_peaks

    Args:
        data ([Ints / Floats]): [Pandas DataFrame]
        peaks ([Ints / Floats]): [array with peak indecies from dataframe]

    Returns:
        [int]: [array of labels based on indecies given]
    """
    reps = []
    count = 1
    for j in range(len(peaks[0])-1):
        for i in data.index:
            if i == peaks[0][count]:
                break
            elif (i >= peaks[0][count-1]) & (i < peaks[0][count]):
                reps.append(count)
            
        count += 1
    
    reps = np.insert(reps, -1, max(reps))
    data['reps'] = reps
    
    return data

def fleksion_ekstension(speed):
        """finding positive and negative speed values,
        to define fleksion and ekstension in a movement, and their index numbers.
        Flexion is expected to be positive speed
        Extensions is expected to be negative speed

        Args:
            y ([float]): [array]

        Returns:
            [DataFrame]: [2 datafames, with speed and given index number, for fleksion and ekstension]
        """
         
        fleksion_value = []
        fleksion_idx = []
        ekstension_value = []
        ekstension_idx = []
        for idx, value in enumerate(speed):
            if value >= 0:
                fleksion_value.append(value)
                fleksion_idx.append(idx)
            else:
                ekstension_value.append(value)
                ekstension_idx .append(idx)
                
        flex = np.array([fleksion_idx, fleksion_value])
        fleksion = pd.DataFrame(flex).T
        fleksion.columns = ['idx', 'speed']
        flex_int = fleksion['idx'].astype(int)
        fleksion['idx'] = flex_int         

        eks = np.array([ekstension_idx, ekstension_value])
        ekstension = pd.DataFrame(eks).T
        ekstension.columns = ['idx', 'speed']
        eks_int = ekstension['idx'].astype(int)
        ekstension['idx'] = eks_int
        
        #Unit test to secure correct values in extenssion and flexion
        if value >= 0:
            if sum( n > 0 for n in fleksion['speed']):
                return [ekstension, fleksion]
            else: 
                print("ERROR: There have been found negative values when none should be there")
        elif value <= 0:
            if sum( n < 0 for n in ekstension['speed']):
                return [ekstension, fleksion]
            else: 
                print("ERROR: There have been found positive values when none should be there")
            
    
def duration_of_rep(data):
    data['idx'] = data.index
    eks_idx_max = data.groupby(data['Reps'])['idx'].max()
    eks_idx_min = data.groupby(data['Reps'])['idx'].min()
    eks_idx_diff = np.mean((eks_idx_max - eks_idx_min) / 500)

    return eks_idx_diff

def gravitycorrect(radianer, torque, maxget):
    '''insert gravity correction based on knee flexion
    '''
    gravitycorrect = []
    for idx, pos in enumerate(radianer):
        gravitymoment = torque.iloc[idx] + maxget*np.cos(pos)
        gravitycorrect.append(gravitymoment)

    return gravitycorrect

def torque_mean(position, RP, max_peaks):
    """Calculates mean of array based on positional data.
        Required a double groupby Series

    Args:
        position ([Pandas Series]): [Positional data]
        RP ([Pandas Series]): [double groupby on dataframe]

    Returns:
        [Series]: [mean data per position from series]
    """
    min_range = position.min()
    max_range = position.max()
    total_range = pd.Series(range(min_range, max_range+1))
    line_mean = []
    for i in range(min_range, max_range+1, 1):
        m = np.sum(RP[:,i]) / (len(max_peaks[0]) - 1)
        line_mean.append(m)
    line_mean_pd = pd.Series(line_mean)

    return [line_mean_pd, total_range]


#Making time axis as seconds in vyn data
def strtime_to_seconds(data):
    """Takes array of time as string, and returns it to seconds as integer.

    Args:
        data ([str]): [time format as Minuted:Seconds]

    Returns:
        [list]: [time as seconds]
    """
    seconds = []
    for time in data:
        sec = sum(x * int(t) for x, t in zip([60, 1], time.split(":")))
        seconds.append(sec)

    return seconds


def metabolic_energy(o2, co2, diff_time):
    """Calculates metabolic energy based on o2 and co2 values based on 
    wiers formal: kcal = (3.9 * LO2 + 1.1 * CO2) / (1 + 0.082 * p)
    where p is assumed to be 0.125 based on Wier (1949)
    Brockway 1987: J = 16.58 * VO2 + 4.51 * VCO2 / (1 + 0.06 * p)
    Peronnet 1991: J = 16.89 * VO2 + 4.84 VCO2
    
    (1 + 0.06 * p) is a modified version from weird, that is only used as a test. This is NOT legitimate.
    

    Args:
    o2 ([array of float / int]): Oxygen value given in liters
    co2 ([array of floats / int]): Carbon dioxide given in liters
    diff_time ([Array]): differential time in seconds

    Returns:
    [float]: sum of total metabolic energy in kJ
    """
    diff_o2 = []
    diff_co2 = []
    for i, j, k in zip(o2, co2, diff_time):
        o = (i / 60) * k
        co = (j / 60) * k
        diff_o2.append(o)
        diff_co2.append(co)
    
    brockway = (16.58 * np.sum(diff_o2) + 4.51 * np.sum(diff_co2)) / 1 + (0.06 * 0.125)
    wier = ((3.941 * np.sum(diff_o2) + 1.106 * np.sum(diff_co2)) / 1 + (0.082 * 0.125)) * 4.184 #cal to j
    peronnet = (16.89 * np.sum(diff_o2) + 4.84 * np.sum(diff_co2))
    
    return [brockway, wier, peronnet]