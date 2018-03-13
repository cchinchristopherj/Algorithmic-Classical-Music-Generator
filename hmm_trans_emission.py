'''
Usage:
python hmm_trans_emission.py 
'''
# Program to generate transition and emission probabilitiy matrices 

import numpy as np
import pandas
import glob
import random
import csv

def update_event_list(df,event_list,event_num,ii):
    ''' Update_event_list Method
            Updates the input event_list, adding 1 to the corresponding 
            MIDI note mod 12 if it is present in the current event, and
            subtracting 1 from the corresponding MIDI note mod 12 if it
            is absent from the current event. 
            A MIDI note is present if its velocity is greater than 0.0
            and a MIDI note is absent if its velocity is 0.0
            
            Args:
                df: Pandas DataFrame of MIDI information 
                    Columns: Features; Ex: 'Velocity'
                    Rows: Examples 
                event_list: 2-D Array of event information (i.e. 12 features
                            each corresponding to the MIDI notes mod 12, with
                            1 indicating note is present and 0 indicating note
                            is absent)
                            Shape: [n_features=12,n_examples)
                event_num: Integer indicating the number of the current event
                ii: Integer indicating the current row under analysis in the
                    Pandas DataFrame
            Returns:
                event_list: 2-D Array of event information (updated)
        '''
    if df.iloc[ii,5] > 0.0:
        event_list[event_num,df.iloc[ii,4]%12] += 1
    else:
        event_list[event_num,df.iloc[ii,4]%12] -= 1
    return event_list

def trans_prob(df_y,lengths_list,labels):
    ''' Trans_prob Method
            Generates the transition probability matrix 
            
            Args:
                df_y: 2-D Numpy Array of harmonic labels for each event 
                      Shape: [1,n_examples]
                lengths_list: 1-D Array of indexes for the dataset as ints
                              (i.e. indicates the indexes into the event_list
                              array of where each piece in the dataset begins 
                              and ends)
                              Shape: [n_pieces]
                labels: Dictionary of harmonies and corresponding integer labels
                        Keys: Harmonies as strings, Ex: 'C_M'
                        Values: Corresponding (arbitrary) integer label
                        ranging from 0 to 143
            Returns:
                trans_mat: Transition probability matrix dictionary
                           Keys: Initial States
                           Values: Dictionaries
                                   Keys: Final States
                                   Values: Probability of transitioning from the
                                   initial states to final states 
        '''
    df_y = np.squeeze(df_y)
    trans_mat = {}
    # Initialize trans_mat dictionary with zeros 
    for ii in labels.values():
        trans_mat[ii] = {}
        for jj in labels.values():
            trans_mat[ii][jj] = 0
    # Since the event_list traverses through all the pieces in the dataset 
    # sequentially, ignore harmonic transitions from the end of one piece to the
    # beginning of the next (as these are arbitrary). These transitions are 
    # indicated by the indexes in lengths_list 
    for ii in range(1,len(df_y)):
        if ii in lengths_list:
            pass
        # Add 1 if a transition from one harmony to another occurs 
        else:
            trans_mat[df_y[ii-1]][df_y[ii]] += 1
    for ii in trans_mat.keys():
        values_sum = sum(trans_mat[ii].values())
        # If the sum of all values for a label is 0, convert zeros to eps 
        # This ensures, when using the viterbi algorithm, that the probability
        # of an event with zero frequency does not become 0 (instead, it becomes
        # very low through multiplication by eps) 
        for jj in trans_mat[ii].keys():
            if values_sum == 0:
                trans_mat[ii][jj] = eps
            # Otherwise, divide each value for a label by the sum of all values 
            # corresponding to the label so that all probabilities sum to 1 
            else:
                trans_mat[ii][jj] = trans_mat[ii][jj]/values_sum
                if trans_mat[ii][jj] == 0:
                    trans_mat[ii][jj] = eps
    return trans_mat

def emission_prob(df_y,event_list,labels):
    ''' Emission_prob Method
            Generates the emission probability matrix 
            
            Args:
                df_y: 2-D Numpy Array of harmonic labels for each event 
                      Shape: [1,n_examples]
                event_list: 2-D Array of event information (i.e. 12 features
                            each corresponding to the MIDI notes mod 12, with
                            1 indicating note is present and 0 indicating note
                            is absent)
                            Shape: [n_features=12,n_examples)
                labels: Dictionary of harmonies and corresponding integer labels
                        Keys: Harmonies as strings, Ex: 'C_M'
                        Values: Corresponding (arbitrary) integer label
                        ranging from 0 to 143
            Returns:
                emission_mat: Emission probability matrix dictionary
                              Keys: Current States
                              Values: Dictionaries
                                    Keys: Observations 
                                    Values: Probability of observing each observation
                                    given the current state. Note that each 
                                    observation's probability, given the current state,
                                    is evaluated independently of the others (i.e. the 
                                    sum of all the values does not equal 1)
        '''
    df_y = np.squeeze(df_y)
    # Find all unique harmonic labels and the number of times they occur 
    unique_labels,counts = np.unique(df_y,return_counts=True)
    unique_dict = {}
    # Create a dictionary of unique labels and corresponding counts 
    for ii,jj in enumerate(unique_labels):
        unique_dict[jj] = counts[ii] 
    emission_mat = {}
    # Initialize trans_mat dictionary with zeros 
    for ii in labels.values():
        emission_mat[ii] = {}
        for jj in np.arange(event_list.shape[0]):
            emission_mat[ii][jj] = 0
    # Add data from event_list to the corresponding key and value
    # Ex: If an event in event_list occurs for state 1, add the data
    # from event_list to the key corresponding to state 1 
    for ii in range(len(df_y)):
        for jj,kk in enumerate(event_list[:,ii]):
            emission_mat[df_y[ii]][jj] += kk
    for ii in emission_mat.keys():
        for jj in emission_mat[ii].keys():
            # Divide every event's value by the total number of times the state 
            # occurred to obtain the probability that that event occurs
            # Ex: If state 1 occurred 3 times, divide every value corresponding
            # to state 1 by 3. 
            # In addition, replace values of 0 by eps to ensure that the probability
            # of an event with zero frequency does not become 0 (instead, it becomes
            # very low through multiplication by eps) 
            if ii in unique_dict.keys():
                emission_mat[ii][jj] = emission_mat[ii][jj]/unique_dict[ii]
            if emission_mat[ii][jj] == 0:
                emission_mat[ii][jj] = eps; 
    return emission_mat

# Read the harmonic labels csv file into a Pandas DataFrame 
filename = 'jsbach_chorals_harmony.csv'
df_y = pandas.read_csv(filename,usecols=[16],header=None,skipinitialspace=True)
# Reduce the number of harmonic labels by using enharmonic spellings
df_y = df_y.replace(to_replace='C#',value='Db',regex=True)
df_y = df_y.replace(to_replace='D#',value='Eb',regex=True)
df_y = df_y.replace(to_replace='F#',value='Gb',regex=True)
df_y = df_y.replace(to_replace='G#',value='Ab',regex=True)
df_y = df_y.replace(to_replace='A#',value='Bb',regex=True)
# Dictionary of string labels and corresponding MIDI notes mod 12 
roots = {'C_':0,'Db':1,'D_':2,'Eb':3,'E_':4,'F_':5,'Gb':6,          'G_':7,'Ab':8,'A_':9,'Bb':10,'B_':11}
# Dictionary of quality labels and corresponding relationship
# between the root, third, and fifth. Ex: For 'M', [4,7] indicates
# that the third is 4 MIDI notes above the root and that the 
# fifth is 7 MIDI notes above the root
quality = {'M':[4,7],'m':[3,7],'d':[3,6]}
# Dictionary of added notes and corresponding relationship between
# the root and added note. Ex: For '4': 5 indicates that the 
# added note is 5 MIDI notes above the root
added_notes = {'4':5,'6':9,'7':10,'':0}
labels = {}
chords = {}
counter = 0
# Using the roots, quality, and added_notes dictionaries, create 
# a dictionary of all the possible labels (called "labels"), where 
# the keys are the string labels and the values are the corresponding
# integer labels
# Create another dictionary (called "chords"), where the keys are the 
# string labels and the values are the MIDI notes mod 12 corresponding 
# to the string label 
for ii in roots.keys():
    for jj in quality.keys():
        for kk in added_notes.keys():
            labels[ii+jj+kk] = counter
            counter += 1
            temp = [roots[ii]]
            for ll in quality[jj]:
                temp.append((roots[ii]+ll)%12)
            if added_notes[kk] == 0:
                pass
            else:
                temp.append((roots[ii]+added_notes[kk])%12)
            chords[ii+jj+kk] = temp
# Convert all the harmonic labels in df_y into the integer labels indicated
# by the labels dictionary 
for ii in range(len(df_y)):
    df_y.iloc[ii,0] = labels[df_y.iloc[ii,0]]
# Convert df_y into a numpy matrix 
df_y = df_y.as_matrix().T

# Load in the CSV files with the MIDI information for each piece in the dataset 
path = 'JSB_Chorales'
names = ['Track','Time','Action','Channel','Note','Velocity']
filenames = sorted(glob.glob(path+'/*.csv'))
all_data = pandas.DataFrame()
for filename in filenames:
    df_temp = pandas.read_csv(filename,names=names,skipinitialspace=True)
    df_temp = df_temp.drop([0,1,2,3,4,5])
    df_temp = df_temp.reset_index(drop=True)
    df_temp = df_temp.dropna()
    df_temp = df_temp.reset_index(drop=True)
    df_temp = df_temp[~df_temp['Action'].str.contains('Unknown_meta_event')]
    df_temp = df_temp.reset_index(drop=True)
    df_temp = df_temp[~df_temp['Action'].str.contains('Control_c')]
    df_temp = df_temp.reset_index(drop=True)
    df_temp.iloc[:,0:1] = df_temp.iloc[:,0:1].apply(pandas.to_numeric)
    df_temp.iloc[:,3:5] = df_temp.iloc[:,3:5].apply(pandas.to_numeric)
    df_temp = df_temp.sort_values(by=['Time'])
    df_temp = df_temp.reset_index(drop=True)
    all_data = all_data.append(df_temp,ignore_index=True)

# Use the time informaton from the all_data Pandas DataFrame to create a numpy
# array "event_list" which contains the relevant information for each individual
# event 
# Also, create an array "lengths_list" which indicates the indexes in event_list
# corresponding to each piece in the dataset 
event_list = np.zeros((len(all_data),12))
event_num = 0
lengths_list = []
for ii in range(len(all_data)):
    # If the time for the current row is the same as that of the previous, 
    # don't increment to a new event 
    if ii == 0 or all_data.iloc[ii,1] == all_data.iloc[ii-1,1]:
        pass
    # If the time for the current row is less than the time for the previous, this
    # means a new piece is occuring. Increment event_num by 1 
    elif all_data.iloc[ii,1] < all_data.iloc[ii-1,1]:
        lengths_list.append(event_num-1)
        event_num += 1
    # If the time for the current row is greater than the time for the previous, this
    # means a new event is occuring. Increment event_num by 1 and copy the data
    # from the previous event to update it. 
    else:
        event_num += 1
        event_list[event_num] = np.copy(event_list[event_num-1])
    event_list = update_event_list(all_data,event_list,event_num,ii)
# Remove all rows with all zeros 
event_list = event_list[~np.all(event_list==0,axis=1)]
event_list = event_list.T
# Convert event_list to 1 (indicating presence of note) and 0 (indicating absence
# of note)
event_list[event_list>0] = 1

eps = np.finfo(np.float).eps

# Generate the transition and emission probability matrices using the event_list
# (observations) and df_y (states) 
trans_mat = trans_prob(df_y,lengths_list,labels)
emission_mat = emission_prob(df_y,event_list,labels)

# Convert the roots and labels dictionaries into csv files for use by other programs
with open('roots.csv','w') as csv_file: 
    file_writer = csv.writer(csv_file)
    file_writer.writerow(roots.keys())
    file_writer.writerow(roots.values())

with open('labels.csv','w') as csv_file:
    file_writer = csv.writer(csv_file)
    file_writer.writerow(labels.keys())
    file_writer.writerow(labels.values())

# Convert the df_y, event_list, and lengths_list arrays into csv files for use 
# by other programs
np.savetxt('df_y.csv',np.squeeze(df_y),delimiter=',')

np.savetxt('event_list.csv',event_list,delimiter=',')

np.savetxt('lengths_list.csv',lengths_list,delimiter=',')

# Convert the trans_mat and emission_mat dictionaries into csv files for use 
# by other programs
trans_mat_df = pandas.DataFrame.from_dict(trans_mat)
trans_mat_df.to_csv('trans_mat.csv',index=None)

emission_mat_df = pandas.DataFrame.from_dict(emission_mat)
emission_mat_df.to_csv('emission_mat.csv',index=None)

