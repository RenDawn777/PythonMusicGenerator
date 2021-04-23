from midiutil import MIDIFile
import random
import numpy
import time
from Dictionary import *


loopingOff = True
melodyReplay = []
melodyReplayDuration = []
melodyReplayStart = 'E'  #Where does the loop start? (Inclusive)
melodyReplayStop = 'C'   #Where does the loop end? (Non-inclusive)
loopCount = 3            #How many chords are being looped?
LoopStartIndexes = [0,1,2] #What are the indexes of the first set of chords?
LoopEndIndexes = [5,6,7]       #What are the indexes of the second set of chords?

#Copyright (c) 2021 Brandon Rendon

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# create the MIDI object
mf = None  # only 1 track
melodyOctive = '4'
melodyOctiveBack = '3'
chordsOctive  = '3'
chordsToPlay = []

#BIS
#chordsSelected = ['G#m','F#','E','F#','G#m','E','F#','D#','D#','G#m','F#','E','D#','E','F#','D#','G#m','G#m','F#','E','D#','E','F#','D#','G#m']

#chordsSelected = ['F','Dm','Am','Em','Am','F','C','G','F','Dm','Am','Em']
#chordsSelected = ['G', 'C', 'G', 'D', 'Em', 'Am', 'Em', 'Bm', 'G', 'C', 'G', 'D']

#HallsOfScience
#chordsSelected = ['C','E','Am','Fm','D#','A#','F#','B']

#RWBY
#chordsSelected = ['Em','C','Am','B','Em','C','Am','B',  'Em','G', 'C', 'B', 'Em', 'C','Am','B','F#','F#','Em',     'Cm', 'G','G','Cm','G','Cm','G', 'G','Cm','G','B','Em']
#chordsSelected =['Cm', 'G','G','Cm','G','Cm','G', 'G','Cm','G','B','Em']

#Zelda
#chordsSelected = ['D', 'C', 'A#', 'F', 'D#', 'Dm', 'E', 'A', 'Am', 'Cm', 'D', 'C','A#','A#','A', 'A#','G#','A','D#','E','A','Am', 'Cm']
#chordsSelected = ['F','Dm','Am','Em']
#chordsSelected = ['E','C#m','F#m','B']

#chordsSelected = ['Fm','A#m','G#','C#',]
chordsSelected = []

#chordsSelected = ['Bm','G','Em','F#m']

#FF7 Main
#chordsSelected = ['E', 'C#m', 'E', 'C', 'D', 'E', 'C#m', 'E', 'A', 'F#m', 'B', 'B', 'E']

#YWKON
#chordsSelected = ['A#m', 'Cm', 'A#m', 'C', 'A#', 'A#m', 'Cm', 'G', 'F', 'A#m', 'Cm', 'A#m', 'C', 'A#', 'A#m', 'F','Cm', 'Gm','F','F','A#m','Cm','A#m','C','A#','A#m','Cm','G','A#','F','A#m','Cm','A#m','C','A#','A#m','Cm','G','A#','F']
#chordsSelected = ['B', 'B', 'Fm', 'Fm', 'B', 'B', 'A#m', 'A#m']

#chordsSelected = ['e_7', 'fm7', 'G_M7', 'g*7', 'A_s', 'Fs', 'F', 'G_M7', 'G#', 'fm7', 'A#m', 'e_m7', 'F7', 'A#m', 'F/A', 'D7/A', 'B/G', 'G_M7', 'G#', 'fm7', 'A#m','e_7','F7','A#m','A#']

#chordsSelected = ['Dm', 'Dm',  'Fm', 'Cm', 'Am', 'Em', 'Gm', 'Dm','F','G','G#', 'A#', 'C']
#chordsSelected = ['G','G','G','G','C','G','G','G','G']

#chordsSelected = ['F','Fm','A#','D#','A#m','D#m','G#','Gm','G']
#chordsSelected = ['A','A','A#','A','A','G#','D','D','D#','D','D','C#']
chordDurations = [1]

#Find and return the note between the two selected notes
def findMiddleNote(Key,a,b):
    index = 0
    solution = 'none'
    for note in Key:
        if note == a:
            if index+2 < len(Key) and Key[index+2] == b:
                solution = Key[index+1]
        if note == b:
            if index+2 < len(Key) and Key[index+2] == a:
                solution = Key[index+1]
        index+=1
    return solution

#Find and return the two adjacent notes
def findNextNote(Key,a):
    index = 0
    solutionA = 'none'
    solutionB = 'none'
    for note in Key:
        if note == a:
            if index+1 < len(Key) :
                solutionA = Key[index+1]
            if index-1 >= 0:
                solutionB = Key[index-1]
        index+=1
    return solutionA, solutionB


#This ensure that that song can be looped seemlessly (forces the length of the song to end on a measure)
def CreateChordLentghs(chordDurations, chordsToPlay):
    while numpy.sum(chordDurations) % 4 != 0:
        chordsToPlay = []
        chordDurations = []
        #Adds the chords to be played to a list and creates a seperate list for how long each chord is to be played
        for chord in chordsSelected:
            chordsToPlay.append(Chords[chord])
            chordDurations.append(random.randrange(2,4))
        if not loopingOff:
            loopIndex = 0
            for ChordDex in LoopEndIndexes:
                chordDurations[ChordDex] = chordDurations[LoopStartIndexes[loopIndex]]
                loopIndex+=1

    return chordDurations, chordsToPlay


#Write the chords to the midi
def WriteChords(manual = False):


    track = 0  # the first track
    time = 0  # start at the beginning

    mf.addTrackName(track, time, "Chords")
    mf.addTempo(track, time, 120)

    # add some notes
    channel = 0
    volume = 75
    index = 0
    posibleDurations = [1, 1, 1, 2, 2, 3]


    # loops through all of the chords to be played and adds them to the midi
    for durationChord in chordDurations:
        index2 = 0
        if not manual:
            while index2 < 4:
                pitch = lookup[chordsToPlay[index][index2] + chordsOctive]
                mf.addNote(track, channel, pitch, time, durationChord, volume)
                index2 += 1
            time += durationChord
            index += 1
        else:
            LoopIndex = 1
            while LoopIndex <= durationChord:
                index2 = 0
                while index2 < 4:
                    NoteDuration = random.choice(posibleDurations)
                    pitch = lookup[chordsToPlay[index][index2] + chordsOctive]
                    mf.addNote(track, channel, pitch, time, NoteDuration, volume)
                    index2 += 1


                LoopIndex +=1
                time += NoteDuration

            index += 1

def WriteBackingTrack():
    # Background Melody Track

    track = 2  # the first track

    time = 0  # start at the beginning

    mf.addTrackName(track, time, "Background Melody")
    mf.addTempo(track, time, 120)

    # add some notes
    channel = 2
    volume = 100
    chordIndex = 0

    for durationChord in chordDurations:
        chordTime = 0
        while chordTime < durationChord:
            pitch = lookup[Chords[chordsSelected[chordIndex]][random.randrange(0, 3)] + melodyOctiveBack]
            posibleDurations = [.5, 1, 2]
            melodyDuration = random.choice(posibleDurations)
            while (chordTime + melodyDuration > durationChord):
                melodyDuration -= 1
            chordTime += melodyDuration
            mf.addNote(track, channel, pitch, time, melodyDuration, volume)
            time += melodyDuration

        chordIndex += 1

def melodyRepeat(continueCount,chordIndex,track,time,channel,volume):
    continueCount += loopCount+1
    replayIndex = 0
    chordIndex += 3
    for replayNote in melodyReplay:
        pitch = lookup[replayNote + melodyOctive]
        melodyDuration = melodyReplayDuration[replayIndex]
        mf.addNote(track, channel, pitch, time, melodyDuration, volume)
        time += melodyDuration

        replayIndex += 1

    melodyReplayEnd = True
    return continueCount,chordIndex,time

def WriteMelody():
    # Melody Track

    track = 1  # the first track
    continueCount = 0
    time = 0  # start at the beginning
    melodyReplayHasStopped = False
    melodyReplayEnd = False

    mf.addTrackName(track, time, "Melody")
    mf.addTempo(track, time, 120)

    # add some notes
    channel = 1
    volume = 100
    chordIndex = 0
    MiddleNoteSelected = 'none'
    prevNote = 'none'

    # Calculates the melody for each chord
    for durationChord in chordDurations:

        chordTime = 0
        if continueCount != 0:
            continueCount -= 1
            continue

        if not loopingOff and melodyReplayStart == chordsSelected[chordIndex] and melodyReplayHasStopped and not melodyReplayEnd:
            continueCount, chordIndex, time = melodyRepeat(continueCount,chordIndex,track,time,channel,volume)
            continue
        # While the length of the melody hasn't surpassed the chord acompanying it
        while chordTime < durationChord:
            # pitch = lookup[Chords[chordsSelected[chordIndex]][random.randrange(0,3)]+melodyOctive]

            if MiddleNoteSelected == 'none':
                possibleNotes = notesIn[chordsSelected[chordIndex]]  # List of notes in the current key
                PentatonicNotes = noteChoices[chordsSelected[chordIndex]]  # List of notes in the Pentatonic scale
                ChordNotes = Chords[chordsSelected[chordIndex]]  # List of notes in the current chord
                noteStepA, noteStepB = findNextNote(PentatonicNotes, prevNote)
                # noteC = possibleNotes[random.randrange(0, 7)]
                noteC = PentatonicNotes[random.randrange(0, 5)]
                # noteC = ChordNotes[random.randrange(0, 3)]
                whatNoteIsNext = [noteStepA, noteStepA, noteStepB, noteStepB, noteStepA, noteStepA, noteStepB,
                                  noteStepB, noteC]
                selectedNote = 'none'
                while selectedNote == 'none':
                    selectedNote = random.choice(
                        whatNoteIsNext)  # Select whether the next note is a step up, down, or random

                # Ensure a 1 in 10 chance the same note will be played twice consequitively

                while prevNote == selectedNote:
                    if random.randrange(0, 10) != 7:
                        selectedNote = ChordNotes[random.randrange(0, 3)]
                    else:
                        break

                middleNote = findMiddleNote(possibleNotes, prevNote, selectedNote)

                # If a middle 'connecting' note can be used, use it, and save the current note to be played next
                if middleNote != 'none':
                    MiddleNoteSelected = selectedNote
                    selectedNote = middleNote
            else:
                selectedNote = MiddleNoteSelected
                MiddleNoteSelected = 'none'
            pitch = lookup[selectedNote + melodyOctive]
            posibleDurations = [.25, .5, .5,2]
            melodyDuration = random.choice(posibleDurations)
            while (chordTime + melodyDuration > durationChord):
                melodyDuration -= .25
            if not loopingOff:
                if melodyReplayStop != chordsSelected[chordIndex] and not melodyReplayHasStopped:
                    melodyReplay.append(selectedNote)
                    melodyReplayDuration.append(melodyDuration)
                else:
                    melodyReplayHasStopped = True

            chordTime += melodyDuration
            prevNote = selectedNote
            # if chordTime == durationChord and chordIndex == len(chordDurations)-1:
            #     pitch = lookup[chordsSelected[chordIndex] + melodyOctive]
            mf.addNote(track, channel, pitch, time, melodyDuration, volume)
            time += melodyDuration

        chordIndex += 1
if __name__ == '__main__':



    #Chords Track
    #These are the chords to be played. The length of the song is directly correlated to the number of chords inputted
    #Somber, Ballad, Creepy, Happy, Joyful
    chordsSelected = Joyful

    start_time = time.time()
    NoError = False
    attemptsFailed = 0
    while not NoError:

        try:
            mf = MIDIFile(3)
            chordDurations, chordsToPlay = CreateChordLentghs(chordDurations, chordsToPlay)
            WriteChords()
            WriteMelody()
            WriteBackingTrack()
            NoError = True
            with open("output.mid", 'wb') as outf:
                mf.writeFile(outf)
        except:
            attemptsFailed +=1
            NoError = False
    end_time = time.time()
    print("Attempts: ")
    print("\nComplete in ",end_time-start_time,"Seconds")
    print(attemptsFailed)
    # pitch = lookup['B6']  # E4
    # time = 2  # start on beat 2
    # duration = 2  # 1 beat long
    # mf.addNote(track, channel, pitch, time, duration, volume)
    #
    # pitch = lookup['A6']  # G4
    # time = 4  # start on beat 4
    # duration = 2  # 1 beat long
    # mf.addNote(track, channel, pitch, time, duration, volume)

    # write it to disk

