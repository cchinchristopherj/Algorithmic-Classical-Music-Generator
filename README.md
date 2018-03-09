#### Algorithmic Classical Music Generator  
#### Final Project - Programming Languages: Python  
#### Professor Lawrence Stead  
#### By: Christopher Chin (cjc2214)  

*************

##### **Motivation and Problems/Obstacles**  

I feel Python is a perfect programming language and tool for   
composing and music-making. For my final project, I wanted to use the   
programming skills I learned from the course to create an algorithmic   
classical music generator, which would endlessly generate new pieces in the  
classical style. However, the project turned into a more difficult undertaking
than I expected - although the music follows most of the rules of   
harmony/voice-leading in theory, I realized that creating distinct, coherent,  
and recognizable melodies involves more than programming in rules (perhaps   
there is a "human" element missing, or just additional programming needed   
to make the melodies more like those in the classical style). With more time,  
I would want to continue refining the program, improving upon the creation of  
melodies, and implementing more structure/form (having melodies and rhythmic  
patterns repeat occasionally througout the composition, etc.).  

*************
##### **Modules and Installation Instructions**  

**Modules used:** midiutil, pygame, argparse, fluidsynth(optional)  

*Note: The correct usage for the program (as given in the main.py file) is:

    python main.py [duration of playtime as float]  

When main.py is run, it will generate a .mid file (MIDI) and play it 
automatically using the pygame module for the duration specified by the user. 
There will most likely (hopefully) not be any issues with playing the MIDI 
file (as pygame is designed for this purpose), so the fluidsynth module is
optional and should not be necessary to download. However, if you do not hear
music after running main.py, there might be an error playing the MIDI. In that
case, you must download fluidsynth to convert the .mid file to an .mp3 (so
that you can play the file from iTunes, etc.). Instructions for downloading
fluidsynth are given below (after instructions for the other modules).*

**How to download midiutil:**
1. Download and unzip the MIDIUtil source distribution from the following link:
https://code.google.com/archive/p/midiutil/downloads

2. "cd" to the directory containing the MIDIUtil source code

3. Install in the standard way using:

        python setup.py install

**How to download pygame:** 
1. Follow the instructions given on the following webpage:
http://florian-berger.de/en/articles/installing-pygame-for-python-3-on-os-x/


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

*************
##### **How the program works**

The "midiutil" module contains methods for specifying MIDI, a format
commonly used by software to specify musical notes, and methods for creating
a .mid file.
The "pygame" module contains methods used to play .mid files.
The "random" module is used throughout the program to algorithmically
generate musical pitch, rhythm, etc.

In the "midiutil" module, numbers are correlated with pitches on a standard
piano keyboard. For example, 60 is the same as middle C. Adding 1 to a
number raises the pitch by a half step, a half step being the smallest
increment that can be added to a note (i.e. 61 is C#). Adding 2
to a number raises the pitch by 2 half steps or a whole step (i.e. 62 is D),
and so on. The same rules apply for subtracting of numbers (subtracting by
1 decreases the pitch by a half step, etc.)
In classical music theory, compositions are structured by sequences of
harmonic progressions. Every harmony in a progression has a function (ex.
"tonic," "predominant," "dominant"), which specifies how the harmony
behaves in the progression. "Tonic," for example, is the name usually 
assigned to the first harmony in a progression. The "root" of a harmony
is the fundamental note, from which other notes are determined.
In the harmony with function "I" and root "C", the other notes are "E"
(C + four half steps, or 60+4), and "G" (C + seven half steps, or 60+7).  
In the harmony with function "ii" and root "D," the other notes are "F"
(D + three half steps) and "A" (D + seven half steps).

The class "harmony" therefore takes a function and root, and uses that   
input to determine the other notes within a chord. The numbers
corresponding to these notes become class variables, which can then be
accessed later on in the program.

The "midiutil" module operates in several steps: first, a certain number of
tracks must be created. Each track essentially represents an independent
line of music within the composition. In this program, two tracks are
created (in the play() method), which represent the right and left hand
parts of the piano score. Second, a tempo must be specified for each track.
Third, MIDI notes can then be added to each of the tracks.

The __init__ method of class "composition" accepts one input - duration.
The user specifies how long they would like the algorithmically generated
piece to be from the command line, with 1.0, 0.5, and 3.74 all being valid 
inputs. If the input is not a float, an error is raised. 
The self.tempo variable is assigned to a random integer between 40 and 80
(40 beats per minute to 80 beats per minute), which allows for a range of
tempos from very slow to very fast.
The self.tempo and self.duration values are then multiplied to obtain the
value for the self.totalbeats variable (i.e. by multiplying the tempo and
duration, you can obtain the total number of beats in the composition).
This is important because the "midiutil" module adds notes on every beat 
or fraction of a beat. (If, for example, a MIDI note is specified with a time
value of 1, it is placed on the first beat of the composition. If a note
is specified with a time value of 3.5, it is placed on the 3 1/2 beat of the
composition. If a note is specified with a time value of 254.3, it is placed
on the 254 1/3 beat of the composition. The self.totalbeats variable
therefore helps keep track of where the MIDI notes are being placed.
The self.time1 and self.time2 variables are an extension of this principle.
These variables correspond with the first and second tracks, respectively.
They help keep track of what beats notes are being placed on for each of the
two tracks independently.
The self.tonic variable chooses a random "tonic" or "key" signature
for the piece from the 12 possible pitches.
The self.chords variable then creates a dictionary, where the values
correspond to the notes in that scale's key signature, and the keys 
correspond to the function of each note within the scale.
The self.compprog variable is a list, which will be eventually be appended 
with all of the harmonic progressions in the composition.
The self.boolean variable is used in the play() method to determine
when to stop adding notes and harmonies to the piece (so that the piece
lasts with the duration the user specified).

The "progressionf" method algorithmically generates harmonic progressions
that conform to rules of classical music theory. Every progression must  
follow the standard formula: tonic, tonicexp, prebridge, bridge, predominant,
dominant (in this order exactly). Different harmonies can be placed into
each category, and some of these categories are optional. The method takes
this into account, using the random module to choose between the different
options and generate a new harmonic progression every time the method is
called.

The alberti bass is one of the most common basslines used in classical
music left hand piano parts.
Given a harmony and an octave, the method creates a list containing the
alberti bassline corresponding to that harmony.
The "octave" input is used to determine where notes are on the piano. For
example, middle C is in the piano's fourth octave. If the "alberti bass"
method was given an input of 5 for the octave, it would play the C
an octave above middle C. If it was given an input of 3, it would play
the C an octave below middle C, and so on.

The "rhythmgen" method generates rhythmic sequences that will eventually 
be used to create melodies. The "rhythms" variable is a list of all the
possible rhythms that can be used in the piece (2.0 is a half note, 1.0   
is a quarter note, 0.5 is an eighth note, 0.25 is a quarter note, and
1.5 is a dotted quarter note). Given a progression, the "rhythmgen" method
will assign random combinations of rhythms to each harmony in the progression
until the sum of rhythmic values equals 2.0 for each harmony. (A sum of 2.0
is specified so that each harmony in the progression lasts for 2 beats,
giving a wider array of possible combinations of the rhythmic values).   
The variable "rhythmsum" keeps track of the running total of the rhythmic
values assigned to each harmony.
During each iteration of the for loop, a while loop chooses a random value
from the "rhythms" list. If the value, when added to rhythmsum, is greater
than 2.0, the value is rejected and the while loop chooses another random 
value. If the value, when added to rhythmsum, is less than or equal to 2.0,  
it is added to "rhythmsublist." When the total of rhythm values in
"rhythmsublist" is 2.0, the "rhythmsublist" is added to "rhythmlist."  
By adding these sublists to the larger scale "rhythmlist" returned by the
method, it is easier to determine what rhythms belong to what harmony
in the progression.

The "melodygen" method generates melodies. The two for loops allow the
program to go through every harmony in the input progression and each
corresponding rhythm sublist in the input rhythmlist. The first for loop
identifies a harmony in the progression, and uses the class "harmony" to
create a list of the notes in that harmony. These notes are considered
"consonant." In other words, if these notes are used in the melody, they
will sound pleasant to the ear because they are chord tones. The second
for loop goes through every element in the corresponding rhythm sublist and
assigns a pitch to it. For example, if a sublist within the rhythmlist was
[1.0,0.5,0.25,0.25], the "melodygen" method would assign a pitch to each
value for a total of four pitches. The pitches assigned are determined
algorithmically by a series of conditions that reflect rules in classical
music theory. For example, the first condition uses an if statement to
determine whether the rhythm sublist has one element (i.e. it is a half note,
meaning that only one melody note is heard above the harmony) or if the 
melodylist has zero elements (the melody note to be assigned will be the
very first pitch heard in the piece). In this case, the melody pitch
assigned must be consonant, and it is taken randomly from the "harmonylist"
(which contains only consonant chord tones). This ensures that the first
note heard in the piece will be consonant, and that if only one melody note
is played above a harmony, it will be consonant (both typical in classical
pieces).
The second condition (the else statement for the above if statement)
identifies what the last pitch in the melodylist is (i.e. the preceding 
note in the melody). If subtracting 1 from or adding 1 to this preceding
note (lowering or raising this note by a half step) results in a pitch
within the "harmonylist," this pitch within "harmonylist" is added to the  
melodylist. This condition is established because of the strong gravitational
pull of the half step within classical music. Half-step motion to chord tones
within a harmony is extremely prevalent in this style, as it serves to
reinforce the sound of a particular harmony.
If half-step motion does not result in a chord tone, the program proceeds
to a nested "else" statement which leads to two possible conditions.    
If the random integer between 0 and 3 is 0, the first condition assigns the
melody note to a consonant pitch within the "harmonylist."
If the random integer between 0 and 3 is 1 or 2, the second condition once 
again identifies the preceding note in the melodylist. If subtracting 2 from 
or adding 2 to this note (lowering or raising this note by a whole step)
results in a pitch within the "harmonylist," this pitch within "harmonylist"
is added to the melodylist. This condition is established because whole-step
motion to chord tones is also prevalent in classical music (not as strong
as half-step motion, but still very typical). If lowering or raising the
preceding melody note by a whole step does not result in a chord tone, the
else statement causes the program to add a consonant pitch within the
"harmonylist" instead.
If the random integer between 0 and 3 is 3, the program proceeds into the    
next "else" statement." This series of code first takes a "testtone" from the
"harmonylist" (a random pitch within this list). If adding 1 or 2, or
subtracting 1 or 2 (raising or lowering by a whole step or half step) results
in a pitch within "scalelist," this pitch within "scalelist" is added to the
melodylist.
(The scalelist variable holds a list containing all of the pitches in the
piece's scale. The pitches are taken from the self.chords dictionary 
and transposed to the octave specified in the input. (The same pitches in
the octave above and below are added to provide more possible pitch
material)).
This condition is established in order to allow for scalar ascending 
and descending motion in the melody (i.e. whole and half step motion to
notes within the key signature's scale).
After appending all of these pitches to the melodylist, the melodylist
is returned at the end of the program.

The "play" method is the "main" method of the program, which calls all of the
other methods in class "composition," creates a .mid file, and plays it
using the "pygame" module.
First, the method creates two new tracks using the "midiutil" module  
as described previously using the "addTrackName" method. Tempo is specified
using the "addTempo" method for each track.
A while loop is then exectuted, which runs as long as self.boolean is True.
During each iteration, the while loop first generates a new harmonic
progression using the "progressionf" method. It then determines the length
of this progression and evaluates to see if it is larger than the value
contained in the self.totalbeats variable (the variable keeping track of the
total number of beats in the composition). If the total number of beats is
larger than the length of the progression, the harmonic progression is
added on to the self.compprog variable (a list keeping track of all the
harmonic progressions in the composition). Then, the length of this
progression is subtracted from the self.totalbeats variable. (The
self.totalbeats variable, in this way, is used to also keep track of how
many beats are left in the composition - how many are left for pitches,   
rhythms, and harmonies to be added to).
Now the program prepares to add MIDI notes to Track 0 (the track
corresponding to the piano right hand, or the melody line of the
composition). The "rhythmgen" and "melodygen" methods are called to   
generate rhythms and melodies corresponding to the progression just
generated using "progressionf". Using the "addNote" method from the
"midiutil" module, a new MIDI note is added to Track 0 for every rhythm
and corresponding pitch from these generated rhythm and melody lists.   
The self.time1 class variable is then incremented by the value of the     
rhythm just added. (Recall that the midi.addNote() method adds notes
on beats or fractions of beats using the input "time" value. The self.time1
variable helps keep track of where to add new notes in time. For example,
if a new MIDI note was added with a rhythm of an eighth note (0.5), the
self.time1 variable would increment by 0.5 so that the next MIDI note
added would come in an eighth note (0.5 beats) later).
If, during an iteration of the while loop, the length of the generated 
progression is found to be greater than self.totalbeats, this means     
that no further progressions can be added to self.compprog without        
exceeding the duration of the composition specified by the user. Therefore,
a harmony of "I" is added to self.compprog to conclude the piece. (By adding
"I" as the final harmony, the piece ends on the tonic, a resolution that 
always occurs in classical pieces).
After exiting from the while loop, the program now prepares to enter new
MIDI notes to Track 1, which corresponds to the piano left hand part or
"bassline" of the composition. For every element in self.compprog (for every
harmony in the composition), the program calls the "albertibass" method to
generate the harmony's corresponding alberti bassline (a series of four   
sixteenth notes per harmony, with every harmony lasting two beats).
If the last element of self.compprog is reached, the program adds one
eighth note (0.5) on the tonic note to conclude the piece).
Finally, the "play" method uses binary write to create a new .mid file
called "composition.mid". Methods from pygame.mixer.music are then used 
to load and play the composition.mid file.
The additional pygame.mixer.music.get_busy() and pygame.time.Clock().tick() 
methods at the end of the method are used to ensure that the file is played
as long as pygame's "mixer" is "busy" (otherwise, the program will close  
before playing the .mid file).

The variable "c" is assigned to an instance of class "composition" with
input value of args.duration. The play() method is then called to create the
.mid file and play the music

*************
