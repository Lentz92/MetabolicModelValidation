""" 
Following script loops through all the participants at the given study for metabolic model validation.
The script calculates the metabolic energy consumed doing a concentric and eccentric knee flexion, 
while also calculating the needed torgue inputs used for a muscuskeletal modelling software. 

"""


#%%
import pandas as pd
import numpy as np
import modules as mod


#FP1 = AD
#FP2 = MB
#FP3 = MM
#FP4 = MS
#FP5 = NL

namelist = ['FP1_con_20','FP1_con_40','FP1_con_60','FP1_con_80',
              'FP2_con_20','FP2_con_40','FP2_con_60','FP2_con_80',
              'FP3_con_20','FP3_con_40','FP3_con_60','FP3_con_80',
              'FP4_con_20','FP4_con_40','FP4_con_60','FP4_con_80',
              'FP5_con_20','FP5_con_40','FP5_con_60','FP5_con_80',
              'FP1_exc_20','FP1_exc_40','FP1_exc_60','FP1_exc_80',
              'FP2_exc_20','FP2_exc_40','FP2_exc_60','FP2_exc_80',
              'FP3_exc_20','FP3_exc_40','FP3_exc_60','FP3_exc_80',
              'FP4_exc_20', 'FP4_exc_40','FP4_exc_60','FP4_exc_80', 
              'FP5_exc_20','FP5_exc_40','FP5_exc_60','FP5_exc_80']

count = 1
for f in namelist:
    print(f"Model {count} / 40")
    count += 1
        #maxget, shank, crank, bw, height, start_con, start_exc
    if  ('FP1' in f) and ('20' in f):
        id_info = [34.08, 0.44, 0.43, 90.5, 1.93, 635, 610]
    elif ('FP1' in f) and ('40' in f):
        id_info = [34.08, 0.44, 0.43, 90.5, 1.93, 679, 610]
    elif ('FP1' in f) and ('60' in f):
        id_info = [34.08, 0.44, 0.43, 90.5, 1.93, 636, 613]
    elif ('FP1' in f) and ('80' in f):
        id_info = [34.08, 0.44, 0.43, 90.5, 1.93, 627, 625]
        
        #maxget, shank, crank, bw, height, start_con, start_exc
    elif ('FP2' in f) and ('20' in f):
        id_info = [28.24, 0.39, 0.35, 78.6, 1.75, 605, 617]
    elif ('FP2' in f) and ('40' in f):
        id_info = [28.24, 0.39, 0.35, 78.6, 1.75, 678, 338]
    elif ('FP2' in f) and ('60' in f):
        id_info = [28.24, 0.39, 0.35, 78.6, 1.75, 610, 610]
    elif ('FP2' in f) and ('80' in f):
        id_info = [28.24, 0.39, 0.35, 78.6, 1.75, 637, 610]
        
        #maxget, shank, crank, bw, height, start_con, start_exc
    elif ('FP3' in f) and ('20' in f):
        id_info = [32.16, 0.39, 0.35, 90.8, 1.77, 620, 611]
    elif ('FP3' in f) and ('40' in f):
        id_info = [32.16, 0.39, 0.35, 90.8, 1.77, 669, 610]
    elif ('FP3' in f) and ('60' in f):
        id_info = [32.16, 0.39, 0.35, 90.8, 1.77, 750, 657]
    elif ('FP3' in f) and ('80' in f):
        id_info = [32.16, 0.39, 0.35, 90.8, 1.77, 633, 315]
        
        #maxget, shank, crank, bw, height, start_con, start_exc
    elif ('FP4' in f) and ('20' in f):
        id_info = [39.71, 0.42, 0.41, 99.9, 1.89, 618, 614]
    elif ('FP4' in f) and ('40' in f):
        id_info = [39.71, 0.42, 0.41, 99.9, 1.89, 753, 600]
    elif ('FP4' in f) and ('60' in f):
        id_info = [39.71, 0.42, 0.41, 99.9, 1.89, 624, 627]
    elif ('FP4' in f) and ('80' in f):
        id_info = [39.71, 0.42, 0.41, 99.9, 1.89, 640, 625]
        
        #maxget, shank, crank, bw, height, start_con, start_exc
    elif ('FP5' in f) and ('20' in f):
        id_info = [27.8, 0.39, 0.38, 92.7, 1.72, 617, 620]
    elif ('FP5' in f) and ('40' in f):
        id_info = [27.8, 0.39, 0.38, 92.7, 1.72, 320, 609]
    elif ('FP5' in f) and ('60' in f):
        id_info = [27.8, 0.39, 0.38, 92.7, 1.72, 432, 624]
    elif ('FP5' in f) and ('80' in f):
        id_info = [27.8, 0.39, 0.38, 92.7, 1.72, 570, 644]

    else: 
        print("Wrong input, try again loser")
        break
    
    
    DYN_DATA = f"7201_{f}_dyn.CSV"
    MAXGET = id_info[0]

    if 'con' in f:
        CONTRACTION = 0
        STARTTIME = id_info[5]
    elif 'exc' in f:
        CONTRACTION = 1
        STARTTIME = id_info[6]

    DATA_FILE = "../data/rawData/dyn/" + DYN_DATA
    dyn = pd.read_csv(DATA_FILE, sep = ",", low_memory=False).dropna(axis=1)
    column_names = ['Status','Time','Position','Torque','Speed']
    
    try:
        dyn.columns = column_names
    except:
        dyn.drop(dyn.columns[5], axis=1, inplace=True)
        dyn.columns = column_names



    [max_peaks, dynPeaks] = mod.find_peaks(dyn, contraction = 0)
    dynData = mod.label_reps(dynPeaks, max_peaks)
    [eks, fleks] = mod.fleksion_ekstension(dynData['Speed'])    


    #creating eks and fleks dataframes with correct columns
    eks['Torque'] = dynData['Torque'].iloc[eks['idx']].values
    fleks['Torque'] = dynData['Torque'].iloc[fleks['idx']].values
    eks['Position'] = dynData['Position'].iloc[eks['idx']].values
    fleks['Position'] = dynData['Position'].iloc[fleks['idx']].values
    eks['Reps'] = dynData['reps'].iloc[eks['idx']].values
    fleks['Reps'] = dynData['reps'].iloc[fleks['idx']].values
    eks['idx'] = eks.index
    fleks['idx'] = fleks.index

    #Rounding all positions to whole numbers / integers
    eks['Pos_int'] = round(eks['Position']).astype(int)
    fleks['Pos_int'] = round(fleks['Position']).astype(int)

    #Starting by correcting the torque, so it is gravity corrected
    eks['pos_rad'] = (eks['Pos_int'] * np.pi) / 180
    fleks['pos_rad'] = (fleks['Pos_int'] * np.pi) / 180

    eks['gravitycorrection'] = mod.gravitycorrect(eks['pos_rad'], eks['Torque'], MAXGET)
    fleks['gravitycorrection'] = mod.gravitycorrect(fleks['pos_rad'], fleks['Torque'], MAXGET)


    RP_eks = eks.groupby(['Reps', 'Pos_int'])['gravitycorrection'].mean()
    RP_fleks = fleks.groupby(['Reps', 'Pos_int'])['gravitycorrection'].mean()


    try:
        mean_eks, total_range_eks = mod.torque_mean(eks['Pos_int'], RP_eks, max_peaks)
        mean_fleks, total_range_fleks = mod.torque_mean(fleks['Pos_int'], RP_fleks, max_peaks)
    except KeyError:
        pass


    #These are used for creating timeline with linspace in anybody function
    eks_duration_rep = mod.duration_of_rep(eks)
    fleks_duration_rep = mod.duration_of_rep(fleks)

    eks_path = "../data/dynProcessedData/" + f + "_dyn_eks.csv"
    fleks_path = "../data/dynProcessedData/" + f + "_dyn_fleks.csv"
    
    eks.to_csv(eks_path, header=False, index=False)
    fleks.to_csv(fleks_path, header=False, index=False)

    #Now working with the vyn data set
    
    VYN_DATA = f"7201_{f}_vyn.csv"
    DATA_FILE = "../data/rawData/vyn/" + VYN_DATA
    vyn = pd.read_csv(DATA_FILE, sep = ";", low_memory=False)
    #checking if data correctly imported by a ; seperator, if not reimport with ,
    if len(vyn.columns) == 1:
        vyn = pd.read_csv(DATA_FILE, sep = ",", low_memory=False)
        
        
    if CONTRACTION == 0:
        degrees = np.arange(min(total_range_eks), max(total_range_eks)+1, 1)
        T = np.array(mean_eks)
        d = (degrees * np.pi) / 180
        diff = np.diff(d)
        work_sum = np.sum(T*diff[0])

        watt = work_sum / (eks_duration_rep + fleks_duration_rep)
        watt_work_performed = watt / eks_duration_rep

    if CONTRACTION == 1:
        degrees = np.arange(min(total_range_fleks), max(total_range_fleks)+1, 1)
        T = np.array(mean_fleks)
        d = (degrees * np.pi) / 180
        diff = np.diff(d)
        work_sum = np.sum(T*diff[0])

        watt = work_sum / (eks_duration_rep + fleks_duration_rep)
        watt_work_performed = watt / fleks_duration_rep

    #This if statement is made, because one data input, has another setup.             
    if len(vyn.columns) == 9: 
        vyn.drop([0], inplace=True)
        vyn.drop(["Load", "HR", "BR FEV%"], axis=1, inplace=True)
        vyn.columns = ['Time', 'VE', 'VO2','VCO2','RER','VO2/kg']
        vyn.dropna(inplace=True)
        vyn = vyn.astype({'VE': int, 'VO2': int, 'VCO2': int, 
                            'RER': float, 'VO2/kg': float})

        Time = mod.strtime_to_seconds(vyn['Time'])
        vyn['Time'] = Time
        #Fixing periods in vyn data
        #removing the first 30s of the data
        vyn = vyn[vyn['Time'] > 30]
        ### defining resting period ###
        resting_vyn = vyn[vyn['Time'] <= STARTTIME]
        ### defining work period ###
        work = vyn[vyn['Time'] >= resting_vyn['Time'].max()]
        
    elif len(vyn.columns) == 10:
        vyn.drop(['Unnamed: 0'], axis=1, inplace=True)
        vyn.drop(["Load", "HR", "BR FEV%"], axis=1, inplace=True)
        vyn.columns = ['Time', 'VE', 'VO2','VCO2','RER','VO2/kg']
        vyn.dropna(inplace=True)
        vyn = vyn.astype({'VE': int, 'VO2': int, 'VCO2': int, 
                            'RER': float, 'VO2/kg': float})
        
        vyn = vyn[vyn['Time'] > 30]
        resting_vyn = vyn[vyn['Time'] <= 750]
        work = vyn[vyn['Time'] >= resting_vyn['Time'].max()]
        
    work_timediff = np.diff(work['Time'])
    rest_timediff = np.diff(resting_vyn['Time'])

    [brock_work_energy, wier_work_energy, peronnet_work_energy] = mod.metabolic_energy(o2 = work['VO2'], co2 = work['VCO2'], diff_time = work_timediff)
    [brock_rest_energy, wier_rest_energy, peronnet_rest_energy] = mod.metabolic_energy(o2 = resting_vyn['VO2'], co2 = resting_vyn['VCO2'], diff_time = rest_timediff)

    rest_time = (resting_vyn['Time'].iloc[-1] - resting_vyn['Time'].iloc[0]) / 60
    work_time = (work['Time'].iloc[-1] - work['Time'].iloc[0]) / 60


    brock_work_met_vyn = brock_work_energy - ((brock_rest_energy / rest_time ) * work_time)
    brock_work_met_per_rep = brock_work_met_vyn / 150 #number of leg extensions / flexions
    
    wier_work_met_vyn = wier_work_energy - ((wier_rest_energy / rest_time ) * work_time)
    wier_work_met_per_rep = wier_work_met_vyn / 150 #number of leg extensions / flexions
    
    peronnet_work_met_vyn = peronnet_work_energy - ((peronnet_rest_energy / rest_time ) * work_time)
    peronnet_work_met_per_rep = peronnet_work_met_vyn / 150 #number of leg extensions / flexions
    
    
    subject = f.split("_")[0]
    contraction_type = f.split("_")[1]
    load = f.split("_")[2]
    
    dict = {'MetabolicCalculation':["brockway", "wier", "peronnet"],
        'TotalMetabolicWork': [brock_work_met_vyn, wier_work_met_vyn, peronnet_work_met_vyn],
        'MetabolicWorkPerRep':[brock_work_met_per_rep, wier_work_met_per_rep, peronnet_work_met_per_rep],
        'TotalMetabolicRest': [brock_rest_energy, wier_rest_energy, peronnet_rest_energy],
        'resttime': [rest_time, rest_time, rest_time],
        'subject' : [subject,subject,subject],
        'contraction' : [contraction_type,contraction_type,contraction_type],
        'load' : [load,load,load],
        'ekstension_time': [eks_duration_rep, eks_duration_rep, eks_duration_rep],
        'flexion_time': [fleks_duration_rep, fleks_duration_rep, fleks_duration_rep],
        'Work': [work_sum, work_sum, work_sum],
        'watt': [watt, watt, watt],
        'bw': [id_info[3], id_info[3], id_info[3]]}
 
    metabolicDf = pd.DataFrame(dict)
    
    if CONTRACTION == 0:
        metabolicDf_path = "../data/vynProcessedData/" + f + "_vyn_eks.csv"
    elif CONTRACTION == 1:
        metabolicDf_path = "../data/vynProcessedData/" + f + "_vyn_fleks.csv"
    else: 
        print("You have made a mistake, dumbass!")
    metabolicDf.to_csv(metabolicDf_path, index=False)
    


# %%
