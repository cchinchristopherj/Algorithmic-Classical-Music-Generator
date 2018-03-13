'''
Usage:
python test_hmm.py [number of chorale to test as int]
'''
# Program to test HMM

import numpy as np
import pandas
import argparse

def viterbiL(obs, states, start_p, trans_p, emit_p):
    ''' Viterbi Algorithm in Log-Space
            Prints HMM predicted labels for the input observations 
            
            Args:
                obs: 2-D numpy array of observations, where observations are
                     the presence/absence of notes (for each of the 12 notes
                     in the chromatic scale, with 1 indicating presence and 
                     0 indicating absence)
                     Shape: [n_features=12,n_examples]  
                states: 1-D numpy array of all the possible labels 
                        Shape: [n_labels]
                start_p: Start probability matrix dictionary, where the initial
                         probability distribution is uniform
                         Keys: Labels
                         Values: Probabilities 
                trans_p: Transition probability matrix dictionary
                         Keys: Initial States
                         Values: Dictionaries
                                 Keys: Final States
                                 Values: Probability of transitioning from the
                                 initial states to final states 
                emit_p: Emission probability matrix dictionary
                        Keys: Current States
                        Values: Dictionaries
                                Keys: Observations 
                                Values: Probability of observing each observation
                                given the current state. Note that each 
                                observation's probability, given the current state,
                                is evaluated independently of the others (i.e. the 
                                sum of all the values does not equal 1)
    '''
    V = [{}]
    for st in states:
        V[0][st] = {"prob": np.log2(start_p[st]) + np.log2(obs_to_prob(obs[:,0],st,emit_p)), "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, obs.shape[1]):
        V.append({})
        for st in states:
            max_tr_prob = max((V[t-1][prev_st]["prob"]+np.log2(trans_p[prev_st][st])) for prev_st in states)
            for prev_st in states:
                if (V[t-1][prev_st]["prob"] + np.log2(trans_p[prev_st][st])) == max_tr_prob:
                    max_prob = max_tr_prob + np.log2(obs_to_prob(obs[:,t],st,emit_p))
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]
    print('The predicted states are: ')
    print(np.array(opt))
        
def obs_to_prob(obs,st,emission_mat):
    ''' Helper function for viterbiL
            Converts input observation into an emission probability (probability
            of observing the observation given the current assumed state) 
            This is performed by raising the probability of each individual 
            event in the observation to a power, where the power is the number
            of times that event occurred in the observation 
            All of the resulting products are then multiplied to find the 
            probability of observing all the events in the observation together
            at the same time 
            
            Args:
                obs: 2-D numpy array of observations, where observations are
                     the presence/absence of notes (for each of the 12 notes
                     in the chromatic scale, with 1 indicating presence and 
                     0 indicating absence)
                     Shape: [n_features=12,n_examples]  
                st: Integer of the assumed current state with values ranging
                    from 0 to 143
                emit_mat: Emission probability matrix dictionary
                        Keys: Current States
                        Values: Dictionaries
                                Keys: Observations 
                                Values: Probability of observing each observation
                                given the current state. Note that each 
                                observation's probability, given the current state,
                                is evaluated independently of the others (i.e. the 
                                sum of all the values does not equal 1)
            Returns:
                prob: Float indicating the emission probability of the input 
                      observation 
    '''
    p = np.array(list(emission_mat[st].values()))
    p_pow = np.power(p,obs)
    p_pow = np.prod(p_pow) 
    prob = p_pow
    return prob

# Argparse takes in the number of the chorale to test as input 
# Number for chorales ranges from 1 to 50
parser = argparse.ArgumentParser(description='Test HMM')
parser.add_argument('chorale_num', type = int, help = 'Number of Chorale to Test')
args = parser.parse_args()

# Load in the df_y data generated by the hmm_trans_emission.py program
df_y = np.genfromtxt('df_y.csv',delimiter=',')
df_y = [int(x) for x in df_y]

# Load in the event_list data generated by the hmm_trans_emission.py program
event_list = np.genfromtxt('event_list.csv',delimiter=',')

# Load in the lengths_list data generated by the hmm_trans_emission.py program
# Also, add the first index (0) of event_list and final index (4703) of event_list
# to lengths_list
lengths_list = np.array([0])
temp = np.genfromtxt('lengths_list.csv',delimiter=',')
temp = temp.astype(int)
lengths_list = np.append(lengths_list,temp)
lengths_list = np.append(lengths_list,event_list.shape[1])
# Create a dictionary of indexes corresponding to each piece in the dataset 
# for easy look-up with the chorale_num from argparse 
event_dict = {}
index = 1
while index < len(lengths_list):
    value = [lengths_list[index-1],lengths_list[index]-1]
    event_dict[index] = value
    index += 1

# Load in the trans_mat and emission_mat generated by the hmm_trans_emission.py
# program 
trans_mat_df = pandas.read_csv('trans_mat.csv')
trans_mat = trans_mat_df.to_dict()
trans_mat = {int(key):trans_mat[key] for key in trans_mat}

emission_mat_df = pandas.read_csv('emission_mat.csv')
emission_mat = emission_mat_df.to_dict()
emission_mat = {int(key):emission_mat[key] for key in emission_mat}

# Lookup the indexes in event_list of the chorale_num input by argparse 
chorale_num = args.chorale_num
obs = event_list[:,event_dict[chorale_num][0]:event_dict[chorale_num][1]]
# Generate numpy array of possible states (0-143)
states = np.arange(144)
# Generate start probability matrix dictionary where the initial probability
# distribution is uniform 
start_p = {}
for ii in range(144):
    start_p[ii] = 1/144
trans_p = trans_mat
emit_p = emission_mat
# Print the predicted labels using viterbiL and the correct labels from df_y
viterbiL(obs,states,start_p,trans_p,emit_p)
print('The correct states are: ')
print(np.squeeze(df_y)[event_dict[chorale_num][0]:event_dict[chorale_num][1]])

