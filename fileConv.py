import sys
import subprocess
import contextlib
# implement pip as a subprocess:
with contextlib.redirect_stdout(None):
  subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pretty_midi'])

import pretty_midi
import numpy as np
# Create fields and constructor!

NotesList = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
probVectorNot = np.zeros((12, 1))
probVectorOct = np.zeros((8, 1))

def markov(files):
  # Could always just pre-build the notes you take, exclude the rest for standardization
  markovNot = np.zeros((12,12))
  markovOct = np.zeros((8,8))
  allData = []
  for i in files:
    allData.append(genData(i))
  allNotes = listTripInd(allData, 0)
  allOctaves = listTripInd(allData, 1)
  firstNote = allNotes[0]
  for i in allNotes[1:]:
    markovNot[firstNote][i] += 1
    firstNote = i
  firstOct = allOctaves[0]
  for i in allOctaves[1:]:
    # print([firstOct, i])
    markovOct[firstOct][i] += 1
    firstOct = i
  markovNot = freqToMarkov(markovNot)
  markovChord = freqToMarkov(chordMarkov(allNotes))
  markovOct = freqToMarkov(markovOct)
  return [markovNot, markovChord, markovOct]  

def genData(midiFile):
  midi_data = pretty_midi.PrettyMIDI(midiFile)
  tempo = midi_data.estimate_tempo()
  notesCol = []
  for i in midi_data.instruments:
    for j in i.notes:
      note = pretty_midi.note_number_to_name(j.pitch)
      octave = note[-1]
      note = note[0:len(note) - 1]
      if note[-1] == "!" or note[-1] == "b":
        note = note[0]
      notesCol.append([find(note, NotesList), int(octave)])
  return notesCol
      
def listTripInd(list, ind):
  arr = []
  for i in list:
      for j in i:
        arr.append(j[ind])
  return arr

def find(desid, within):
  for i in range(0, len(within)):
    if within[i] == desid:
      return i
  return None

def freqToMarkov(freq):
  rowPos = 0
  while rowPos < len(freq):
    sum = 0
    for i in freq[rowPos]:
      sum += i
    for i in range(0, len(freq[rowPos])):
      if sum != 0:
        freq[rowPos][i] = freq[rowPos][i] / sum
      else:
        freq[rowPos][i] = 0
    rowPos += 1
  return freq

def chordMarkov(notes):
  chordMatr = np.zeros((144, 12))
  for i in range(2, len(notes)):
    minusTwoNote = notes[i-2]
    minusOneNote = notes[i-1]
    note = notes[i]
    chordMatr[minusOneNote + 12 * minusTwoNote][note] += 1
  return chordMatr

def findLargestInd(vector):
  largestCur = -1
  largestInd = -1
  for i in range(0. len(vector):
    curEntry = vector[i][0]
    if (curEntry > largestCur):
      largestCur = curEntry
      largestInd = i
  return largestInd

def createMusNorm(startNote, startOct, markovNot, markovOct):
  probVectorNot[startNote] = 1
  probVectorOct[startOct] = 1
  noteList = [[startNote, startOct]]
  for i in range(199):
    noteList.append(nextNorm(probVectorNot, probVectorOct, markovNot, markovOct))
  return noteList
  
def nextNorm(vectNot, vectOct, markovNot, markovOct):
  # List composition ([note, velocity])
  nextVectNot = np.matmul(markovNot, vectNot)
  nextVectOct = np.matmul(markovOct, vectOct)
  newNote = findLargestInd(nextVectNot)
  newOct = findLargestInd(nextVectOct)
  probVectorNot = nextVectNot
  probVectorOct = nextVectOct
  return [newNote, newOct]

def createMusChord(startNote1, startNote2):

def nextChord():
    
