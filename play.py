'''
Usage:
python play.py [duration of playtime as float]
'''
# Algorithmic Classical Music Generator (Main Program)

import numpy as np
import pandas
from midiutil.MidiFile3 import MIDIFile
import pygame
import random
import argparse

class harmony:
    ''' Harmony Class
            Stores information about the (MIDI) notes in the input label 
            
            Args:
                label: Integer of the current harmonic label (ranges from 
                       0 to 143)
                roots: Dictionary of roots and corresponding MIDI numbers mod 12
                       Keys: Roots as strings; Ex: 'C_M'
                       Values: MIDI number mod 12 of root
                reverse_labels: Dictionary of MIDI numbers mod 12 and 
                                corresponding roots
                                Keys: MIDI number mod 12 
                                Values: Roots as strings; Ex: 'C_M'
    '''
    def __init__(self,label,roots,reverse_labels):
        self.reverse_labels = reverse_labels
        # Using reverse_labels, convert input integer label to 
        # corresponding string label
        self.label = list(reverse_labels[label])
        self.lenlabel = len(self.label)
        self.roots = roots
        # Extract the root from the string label 
        self.root = self.label[0]+self.label[1]
        self.root = self.roots[self.root]
        # Extract the quality from the string label 
        self.quality = self.label[2]
        # Assign values to self.third and self.fifth 
        # according to the quality 
        if self.quality == 'M':
            self.third = self.root + 4
            self.fifth = self.root + 7
        elif self.quality == 'm':
            self.third = self.root + 3
            self.fifth = self.root + 7
        else: 
            self.third = self.root + 3
            self.fifth = self.root + 6
        # If the label indicates a seventh chord, assign
        # a value to self.add for the corresponding 
        # MIDI note mod 12 
        if self.lenlabel == 4 and self.label[3] == '7':
            self.add = self.root + 10
        # For the albertibass method, assign self.add 
        # to self.fifth if not a seventh chord 
        else:
            self.add = self.fifth 
        
class composition:    
    ''' Composition Class
            Used to algorithmically generate harmonic progressions based off
            the input transition probability matrix, in addition to rhythms 
            and melodies in the classical style and play the resulting 
            compositions 
            
            Args:
                roots: Dictionary of roots and corresponding MIDI numbers mod 12
                       Keys: Roots as strings; Ex: 'C_M'
                       Values: MIDI number mod 12 of root 
                labels: Dictionary of harmonies and corresponding integer labels
                        Keys: Harmonies as strings, Ex: 'C_M'
                        Values: Corresponding (arbitrary) integer label
                        ranging from 0 to 143
                trans_mat: Transition probability matrix dictionary
                           Keys: Initial States
                           Values: Dictionaries
                                   Keys: Final States
                                   Values: Probability of transitioning from the
                                   initial states to final states 
                duration: User-input desired duration of composition as float
                          in minutes; Ex: 5.5 (5 and a half minutes)
    '''
    def __init__(self,roots,labels,trans_mat,duration):
        # Divide input duration by 2 because play method assigns each harmonic
        # label a time duration of 2.0 seconds to construct the composition 
        # (i.e. each harmony lasts for 2 seconds) 
        if isinstance(duration,float):
            self.duration = duration / 2
        else:
            raise ValueError()
        # self.time1 and self.time2 used by play method
        self.time1 = 0
        self.time2 = 0    
        self.trans_mat = trans_mat
        self.labels = labels
        self.reverse_labels = {y:x for x,y in labels.items()}
        self.roots = roots
        # Randomly choose a tonic from the available keys and from major ('M') or 
        # minor ('m')
        temp = random.choice([ii for ii in self.roots.keys()])+random.choice(['M','m'])
        # Assign the corresponding integer label to the randomly chosen string label 
        self.tonic = self.labels[temp]
        # Assign MIDI notes mod 12 to the self.scale variable (indicating the scale
        # for the composition) based on the quality 
        if temp[2] == 'M':
            self.scale = [0,2,4,5,7,9,11]
        else:
            self.scale = [0,2,3,5,7,8,10]
        # Assign a random tempo 
        self.tempo = random.randint(50,80)
        # Total number of beats in composition 
        self.totalbeats = self.tempo * self.duration
        # Holds the harmonic progressions for the entire composition 
        self.compprog = []
        # Indicates whether to continue adding progressions 
        self.boolean = True

    def progressionf(self):
        ''' Progressionf Method 
                Algorithmically generates harmonic progressions using the
                initial, randomly-assigned tonic and input transition 
                probability matrix
                
                Returns: 
                    progression: 1-D Array of integer harmonic labels for 
                                 the algorithmically-generated harmonic 
                                 progression 
                                 Shape: [n_labels]
                            
        '''
        eps = np.finfo(np.float).eps
        progression = []    
        progression.append(self.tonic)
        flag = 0
        index = 0
        # Using the tonic as the first harmonic label in the progression,
        # use the transition probability matrix and np.random.choice 
        # to select the next harmonic label in the progression 
        while flag == 0:
            p = [ii for ii in self.trans_mat[progression[index]].values()]
            # Convert values of eps in the matrix to 0.0 
            for ii in range(len(p)):
                if p[ii] <= eps:
                    p[ii] = 0.0
            progression.append(np.random.choice(144,1,p=p)[0])
            index += 1
            # End the progresion when the tonic is returned to 
            if progression[index] == self.tonic:
                flag = 1
        return progression

    def albertibass(self,harmony,octave):
        ''' Albertibass Method 
                Generates the MIDI notes to be used in the piano left hand alberti 
                bass line accompanying the current melody 
            
                Args:
                    harmony: Harmony class object
                    octave: Integer indicating the desired octave for the generated
                            MIDI notes; Ex: 5 (5th octave)
                Returns:
                    chordList: 1-D Array of MIDI note numbers as ints to be used for
                               the piano left hand part 
                               Shape: [n_notes=4]
        '''
        chordlist = []
        # The alberti bass consists of a root, fifth, third, fifth pattern
        # However, if the harmony is a seventh chord, replace the fifth with 
        # the seventh 
        chordlist.extend([harmony.root+(12*octave),
                          harmony.add+(12*octave),
                          harmony.third+(12*octave), 
                          harmony.add+(12*octave)])
        return chordlist
   
    def rhythmgen(self,progression):
        ''' Rhythmgen Method
                Generates the rhythm of the melody notes accompanying the current
                harmony
            
                Args:
                    progression: 1-D Array of integer harmonic labels 
                                     Shape: [n_labels]
                Returns:
                    rhythmList: 1-D Array of rhythm duration values as floats to
                                be used by the melody 
                                Shape: [n_notes]
        '''
        progression = progression
        # Possible rhythm duration values 
        rhythms = [2.0,1.0,0.5,0.25,1.5]
        rhythmlist = []
        rhythmsublist = []
        rhythmsum = 0.0
        # For each harmony, randomly choose values from the rhythms list
        # until the duration equals 2.0 and add these duration values to 
        # rhythmsublist. Once the duration equals 2.0, add rhythmsublist
        # to rhythmlist, initialize rhythmsublist to the empty array and
        # repeat
        for n in progression:
            while(rhythmsum < 2.0):
                index = random.randint(0,4)
                if rhythmsum + rhythms[index] <= 2.0:
                    rhythmsublist.append(rhythms[index])
                    rhythmsum += rhythms[index]
            rhythmsum = 0.0
            rhythmlist.append(rhythmsublist)
            rhythmsublist = []
        return rhythmlist

    def melodygen(self,progression,rhythmlist,scale,octave):
        ''' Melodygen Method
                Generates the notes of the melody accompanying the current 
                harmony
            
                Args:
                    progression: 1-D Array of integer harmonic labels 
                                     Shape: [n_labels]
                    rhythmList: 1-D Array of rhythm duration values as floats 
                                Shape: [n_notes]
                    scale: 1-D Array of MIDI notes mod 12 in the current tonic's
                           scale
                           Shape: [n_notes=7]
                    octave: Integer indicating the desired octave for the generated
                            MIDI notes; Ex: 5 (5th octave)
                Returns:
                    melodyList: 1-D Array of melody MIDI note numbers as ints
                                Shape: [n_notes]
        '''
        rhythmlist = rhythmlist
        progression = progression
        scale = scale
        scalelist = []
        # Create a list of possible notes to be used by the melody using the 
        # scale of the composition 
        for n in scale: 
            octaven1 = n + (12*octave)
            octaven2 = n + (12*(octave-1))
            octaven3 = n + (12*(octave+1))     
            scalelist.extend([octaven1,octaven2,octaven3])
        # List holding the melody MIDI notes of the composition 
        melodylist = []
        length = len(progression) 
        for m in range(length):
            harmonylist = []
            # For every harmony, find the corresponding notes using the 
            # harmony class and add those notes to harmonylist 
            chord = harmony(progression[m],self.roots,self.reverse_labels)
            temp = list(set([chord.root+(12*octave),chord.third+(12*octave),chord.fifth+(12*octave),chord.add+(12*octave)]))
            harmonylist.extend(temp)
            # For every duration value in rhythmlist, assign a melody MIDI note
            for p in rhythmlist[m]:
                if len(rhythmlist[m]) == 1 or len(melodylist) == 0:
                    # Randomly choose a note from harmonylist
                    melodylist.append(random.choice(harmonylist))
                else:
                    if (melodylist[len(melodylist) - 1] - 1) in harmonylist:
                        melodylist.append(melodylist[len(melodylist) - 1] - 1)
                    elif (melodylist[len(melodylist) - 1] + 1) in harmonylist: 
                        melodylist.append(melodylist[len(melodylist) - 1] + 1)
                    else: 
                        if (random.randint(0,3) == 0):
                            melodylist.append(random.choice(harmonylist))
                        elif (random.randint(0,3) == 1):
                            if (melodylist[len(melodylist) - 1] - 2) in harmonylist:
                                melodylist.append(melodylist[len(melodylist) - 1] - 2)
                            elif (melodylist[len(melodylist) - 1] + 2) in harmonylist:
                                melodylist.append(melodylist[len(melodylist) - 1] + 2)   
                            else: 
                                melodylist.append(random.choice(harmonylist))
                        else:
                            # Add notes that could be outside the scale, but encourage
                            # notes that are one or two steps away from the previous 
                            # note to encourage step-wise up and down motion 
                            testtone = melodylist[len(melodylist) - 1] 
                            ncth = testtone + 1
                            nctl = testtone - 1
                            ncthh = testtone + 2
                            nctll = testtone - 2                   
                            if ncth in scalelist:
                                melodylist.append(ncth)
                            elif nctl in scalelist:
                                melodylist.append(nctl)
                            elif ncthh in scalelist:
                                melodylist.append(ncthh)
                            elif nctll in scalelist:
                                melodylist.append(nctll)
                            else:
                                melodylist.append(testtone)
        return melodylist       

    def play(self):
        ''' Play Method
                Generates the MIDI tracks necessary to play the composition
                Plays the composition using pygame module
        '''
        # Create two MIDI tracks 
        midi = MIDIFile(2)
        # Piano right hand track 
        track = 0
        time = 0
        midi.addTrackName(track,time,"Piano Right Hand")
        midi.addTempo(track,time,self.tempo)
        track = 1
        midi.addTrackName(track,time,"Piano Left Hand")
        midi.addTempo(track,time,self.tempo)
        while(self.boolean):
            # Create new progressions as long as self.boolean is True 
            progression = self.progressionf()
            proglength = len(progression)
            flag = 0
            # If the length of the progression is greater than self.totalbeats,
            # the composition will last longer than the user-input duration 
            # Therefore, try 10 more times to generate a progression shorter
            # than self.totalbeats. 
            while self.totalbeats <= proglength: 
                progression = self.progressionf()
                proglength = len(progression)
                flag += 1
                if flag == 10:
                    break
            # If the length of the progression is suitable, add it to self.compprog
            if self.totalbeats >= proglength:
                self.compprog.extend(progression)
                # Subtract length of progression from self.totalbeats (so that 
                # self.totalbeats keeps track of number of beats left in the 
                # composition)
                self.totalbeats -= proglength
                track = 0
                channel = 0
                volume = 100
                # Create rhythmlist
                temprlist = self.rhythmgen(progression)
                rhythmlist = []
                for r in temprlist:
                    for el in r:
                        rhythmlist.append(el)    
                # Create melodylist using rhythmlist
                melodylist = self.melodygen(progression,temprlist,self.scale,5)
                rllength = len(rhythmlist)
                # Add each note to the piano right hand track 
                for n in range(rllength):
                    pitch = melodylist[n]
                    duration = rhythmlist[n]
                    midi.addNote(track,channel,pitch,self.time1,duration,volume)
                    self.time1 += rhythmlist[n]
            # If program fails to generate a progression shorter than self.totalbeats,
            # add the tonic to self.compprog and end the composition 
            else: 
                self.compprog.append(self.tonic)
                self.boolean = False
        # Piano left hand track 
        track = 1
        channel = 0
        duration = 0.25
        volume = 80
        # For every harmony in self.compprog, add the alberti bass line 
        for n in range(len(self.compprog)):
            a = self.albertibass(harmony(self.compprog[n],self.roots,self.reverse_labels),4)
            if n == len(self.compprog) - 1:
                pitch = a[0]
                duration = 0.5
                midi.addNote(track,channel,pitch,self.time2,duration,volume) 
            else:
                for iter in range(2):    
                    for tone in range(4):
                        pitch = a[tone]
                        midi.addNote(track,channel,pitch,self.time2,
                                     duration,volume)
                        self.time2 += 0.25
        # Write a midi file 
        file = "composition.mid"
        with open(file,'wb') as binfile:
            midi.writeFile(binfile)
        # Play the midi file using pygame 
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

# Argparse takes in the duration of playtime desired by user as float
parser = argparse.ArgumentParser()
parser.add_argument('duration', type = float, help = 'duration of composition')
args = parser.parse_args()
       
# Read in the roots, labels, and trans_mat dictionaries generated
# by the hmm_trans_emission.py program 
roots_df = pandas.read_csv('roots.csv')
roots = roots_df.to_dict(orient='records')
roots = roots[0]

labels_df = pandas.read_csv('labels.csv')
labels = labels_df.to_dict(orient='records')
labels = labels[0]

trans_mat_df = pandas.read_csv('trans_mat.csv')
trans_mat = trans_mat_df.to_dict()
trans_mat = {int(key):trans_mat[key] for key in trans_mat}

c = composition(roots,labels,trans_mat,args.duration)
c.play()


