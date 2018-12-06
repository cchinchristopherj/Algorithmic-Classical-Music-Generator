Algorithmic Classical Music Generator
=========================

Uses machine learning/hidden markov models to recognize classical harmonic progressions and algorithmically generate pieces of classical music

Uses the dataset and labels constructed for [BREVE- An HMPerceptron-Based Chord Recognition System](https://link.springer.com/chapter/10.1007/978-3-642-11674-2_7)
and is loosely based off of the guidelines provided in that paper as well as
[Music Chord Recognition Using Artificial Neural Networks](https://www.researchgate.net/publication/256374891_Music_Chord_Recognition_Using_Artificial_Neural_Networks)

The labels file for the [BREVE- An HMPerceptron-Based Chord Recognition System](https://link.springer.com/chapter/10.1007/978-3-642-11674-2_7) dataset is provided to you in the file "jsbach_chorals_harmony.csv" but, if desired, the original source can be accessed [here](https://archive.ics.uci.edu/ml/datasets/Bach+Choral+Harmony)

Click on the highlighted "Data Folder" on the page and download the "jsbach_chorals_harmony.zip" file 
- The downloaded file will have a .data file and a .names file
- Change the extension of the .data file to .txt 
- You can convert the .txt file to .csv in Excel

The dataset has been provided to you in the folder "JSB_Chorales," but, if desired, the original source for the MIDI files is located [here](https://github.com/jamesrobertlloyd/infinite-bach/tree/master/data/chorales/midi)

The MIDI files were converted into .csv files using John Walker's [midicsv](http://www.fourmilab.ch/webtools/midicsv/)

A Hidden Markov Model (HMM) is used to model the dataset. As an HMM is determined solely by its transition, emission, and start probability matrices, these are constructed independently in the hmm_trans_emission.py program by training on the provided dataset: 
- The dataset is first converted from the raw MIDI information in the .csv files into "events" which mark times when either a new note is played or a previously playing note is released. 
- For each event, (in HMM terminology) the "observation" is the notes that are present or absent. A 12-dimensional feature vector is constructed for each of these events (with the 12 features corresponding to the 12 chromatic notes of the piano keyboard). A 1 indicates the note being present and a 0 indicates the note being absent. 
- These "observations" indicate hidden "states" which are the underlying harmonic labels for each event (ground truth provided in the labels file "jsbach_chorals_harmony.csv"
- The transition and emission probability matrices are created by analyzing every event in each of the Bach chorale pieces in the dataset. The start probability matrix is assumed to have a uniform probability distribution over the 144 different harmonic labels possible. 
- With the transition and emission probability matrices, if the HMM is given a new piece to analyze, it will repeat the procedure above to predict the harmonic labels, i.e. it will conver the piece from raw MIDI information to events to observations. The Viterbi algorithm is used to determine the corresponding hidden states. The Viterbi algorithm used in the hmm_trans_emission.py program is based off of the one provided [here](https://en.wikipedia.org/wiki/Viterbi_algorithm), but is modified for calculations in log space and the particular configuration of the emission probability vectors in this problem. 
- In theory, given a new classical piece, the HMM should be able to predict the harmonic labels for each event. A piece from a different genre of music would be more difficult to analyze as the training set only consisted of Bach chorales. 
Note: The performance of the current model is not optimal, as the HMM often predicts a similar class instead of the ground truth class. (For example, while the ground truth label for an event is 'C_M' the HMM will often predict 'C_M4,' as the emission probability for this label sometimes has a greater probability than that for 'C_M'. These errors will be corrected in an updated model. 
- Now, using this information, you can generate your own algorithmically-generated pieces, with harmonic progressions constructed using the transition probability matrix. A representative example can be found [here](https://github.com/cchinchristopherj/Algorithmic-Classical-Music-Generator/blob/master/output.mp3). 
Note: While the harmonic progressions follow the patterns learned by the HMM, the melody and rhythm are not optimized to "sound" like a Bach piece. An updated model will improve these issues. 

Modules and Installation Instructions
=========================

**"Standard" Modules Used (Included in Anaconda Distribution):** numpy, pandas, glob, random, csv, argparse

If necessary, these modules can also be installed via PyPI. For example, for the "pandas" module: 

        pip install pandas

**Additional Modules used:** midiutil, pygame, argparse, fluidsynth(optional)  

**How to download midiutil:**
1. Download and unzip the MIDIUtil source distribution from the following link:
https://code.google.com/archive/p/midiutil/downloads

2. "cd" to the directory containing the MIDIUtil source code

3. Install in the standard way using:

        python setup.py install

**How to download pygame:** 
1. Follow the instructions given on the following webpage:
https://www.pygame.org/wiki/GettingStarted


**How to download FluidSynth (optional as described above):** 
1. Go to the following link, go to the bottom of the page in the "Download"
section, and click on "FluidSynth version 1.44." This will download the 
SoundFont needed for FluidSynth to operate: 

    http://www.schristiancollins.com/generaluser.php

2. After unzipping the file, go inside the new folder (should be titled 
"General User GS 1.44 FluidSynth"). There should be a file in this folder 
called "GeneralUser GS FluidSynth v1.44.sf2". This is the SoundFont file. 
Rename the file "soundfont.sf2". Now, copy and paste it into the same folder
on your computer where my final project's  main.py file is located. 

3. Follow the instructions given on the following webpage for downloading
"FluidSynth." (The page contains instructions for downloading FluidSynth
and Timidity++ - just follow the instructions for FluidSynth). Ignore the 
last instruction that begins with "With fluidsynth working, the conversion 
is simple." (This instruction tells you how to use FluidSynth to convert
MIDI to mp3). See the next step (step 4) for how to do so.

    http://pedrokroger.net/converting-midi-files-mp3-mac-os/

4. After running my final project's main.py program, a "composition.mid" file 
should appear in the same folder where the main.py file is located. This is 
the MIDI file. In order to convert it to an mp3, run the following from the 
command line:                                                               

        fluidsynth -F output.wav soundfont.sf2 composition.mid  
        lame output.wav  

    These two commands, from the command line, will create a new file called
    "output.mp3" in the same folder as main.py. (The first command creates a
    .wav file, and the second converts that to an .mp3 file). Now you can play 
    the .mp3 file (from iTunes, etc.). 

Correct Usage
=========================

Download the JSB_Chorales folder (of .csv files) and jsbach_chorals_harmony.csv file
to the desired directory on your computer.
Then run:

    python hmm_trans_emission.py 
    
This creates a Hidden Markov Model for the dataset, specifically a transition and emission probability matrix. The states are the harmonic labels for each event in the dataset and the observations are the notes present/absent during each event. This generates the following .csv files for use by other programs: 
- 'roots.csv'
- 'labels.csv'
- 'df_y.csv'
- 'event_list.csv'
- 'lengths_list.csv'
- 'trans_mat.csv'
- 'emission_mat.csv'

Now there are two uses for the information generated by these .csv files:
First, using the generated transition and emission probability matrices, you can test the accuracy of the Hidden
Markov Model. Out of the 50 training examples (Bach chorale pieces) in the dataset, you can run the following and choose a number from 1-50 for the command line argument to test the HMM on that training example:

    python test_hmm.py [number of chorale to test as int]
    
The program will generate the HMM's predicted labels and the correct labels for comparison. 

Second, using the generated transition probability matrix, you can algorithmically generate compositions with harmonic progressions in the classical style. 
Run the following:

    python play.py [duration of playtime (in minutes) as float]
    
Note: When play.py is run, it will generate a .mid file (MIDI) and play it 
automatically using the pygame module for the duration specified by the user. 
There will most likely not be any issues with playing the MIDI 
file (as pygame is designed for this purpose). However, if you do not hear
music after running play.py, there might be an error playing the MIDI. In that
case, you must download the fluidsynth module to convert the .mid file to an .mp3 (so
that you can play the file from iTunes, etc.). 
