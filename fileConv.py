import sys
import subprocess
import contextlib
from os import walk

with contextlib.redirect_stdout(None):
  # implement pip as a subprocess:
  subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pretty_midi'])

import pretty_midi
import random
import numpy as np

NotesList = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
probVectorNot = np.zeros((12, 1))
probVectorOct = np.zeros((8, 1))
probVectorChordNot = np.zeros((144, 1))
probVectorChordOct = np.zeros((64, 1))

def collapse(dubList):
    music = []
    for i in dubList:
        adder = i[0]
        for j in range(1, len(i)):
            music.append(adder + "/" + i[j])
    return music

musicList = []
for (dir, dir_name, file) in walk("music"):
    musicList.append([dir] + file)
musicList = collapse(musicList)

def createNormMusic(fileName, startNoteOct):
  startOct = int(startNoteOct[-1])
  startNot = find(startNoteOct[0:len(startNoteOct) - 1], NotesList)
  allMarkovs = markov(musicList)
  markovNot = allMarkovs[0]
  markovOct = allMarkovs[2]
  allNotes = createMusNorm(startNot, startOct, markovNot, markovOct)
  # print(allNotes)
  noteListToMidi(fileName, allNotes)

def createChordMusic(fileName, startNoteOct1, startNoteOct2):
  startOct1 = int(startNoteOct1[-1])
  startNot1 = find(startNoteOct1[0:len(startNoteOct1) - 1], NotesList)
  startOct2 = int(startNoteOct2[-1])
  startNot2 = find(startNoteOct2[0:len(startNoteOct2) - 1], NotesList)
  allMarkovs = markov(musicList)
  markovChordNot = allMarkovs[1]
  markovChordOct = allMarkovs[3]
  allNotes = createMusChord(startNot1, startNot2, startOct1, startOct2, markovChordNot, markovChordOct)
  noteListToMidi(fileName, allNotes)

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
  markovChordOctave = freqToMarkov(chordOctaveMarkov(allOctaves))
  markovOct = freqToMarkov(markovOct)
  return [markovNot, markovChord, markovOct, markovChordOctave]  

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
  return np.transpose(freq)

def chordOctaveMarkov(octaves):
  octMatr = np.zeros((64, 8))
  for i in range(2, len(octaves)):
    minusTwoOct = octaves[i - 2]
    minusOneOct = octaves[i - 1]
    octave = octaves[i]
    octMatr[minusOneOct + 8 * minusTwoOct][octave] += 1
  return octMatr


def chordMarkov(notes):
  chordMatr = np.zeros((144,12))
  for i in range(2, len(notes)):
    minusTwoNote = notes[i-2]
    minusOneNote = notes[i-1]
    note = notes[i]
    chordMatr[minusOneNote + 12 * minusTwoNote][note] += 1
  return chordMatr

'''
LEGACY CODE
def findLargestInd(vector):
  largestCur = -1
  largestInd = -1
  for i in range(0, len(vector)):
    curEntry = vector[i][0]
    if (curEntry > largestCur):
      largestCur = curEntry
      largestInd = i
  return largestInd
'''

def createMusNorm(startNote, startOct, markovNot, markovOct):
  probVectorNot[startNote] = 1
  probVectorOct[startOct] = 1
  noteList = [[startNote, startOct]]
  for i in range(199):
    # print(probVectorNot)
    noteList.append(nextNorm(probVectorNot, probVectorOct, markovNot, markovOct))
  return noteList

def randomPickVector(vector):
  randomNum = random.random()
  for i in range(len(vector)):
    randomNum -= vector[i][0]
    if (randomNum <= 0):
      return i
  return random.randint(0, len(vector) - 1)

def nextNorm(vectNot, vectOct, markovNot, markovOct):
  # List composition ([note, velocity])
  nextVectNot = np.matmul(markovNot, vectNot)
  # print(nextVectNot)
  nextVectOct = np.matmul(markovOct, vectOct)
  # print(nextVectOct)
  newNote = randomPickVector(nextVectNot)
  newOct = randomPickVector(nextVectOct)
  global probVectorNot
  probVectorNot = nextVectNot
  global probVectorOct
  probVectorOct = nextVectOct
  return [newNote, newOct]

def noteListToMidi(midiFileName, notes):
  newMidi = pretty_midi.PrettyMIDI()
  harpsichordProgram = pretty_midi.instrument_name_to_program("Harpsichord")
  harpsichord = pretty_midi.Instrument(program=harpsichordProgram)
  for i in range(0, len(notes)):
    accNote = str(NotesList[notes[i][0]]) + str(notes[i][1])
    pitchNum = pretty_midi.note_name_to_number(accNote)
    note = pretty_midi.Note(velocity=100, pitch = pitchNum, start = 0.5 * i, end = 0.5 * (i + 1))
    harpsichord.notes.append(note)
  newMidi.instruments.append(harpsichord)
  newMidi.write(midiFileName)

def createMusChord(startNote1, startNote2, startOct1, startOct2, chordNotMarkov, chordOctMarkov):
  noteList = [[startNote1, startOct1], [startNote2, startOct2]]
  probVectorChordNot[startNote1 * 12 + startNote2][0] = 1
  probVectorChordOct[startOct1 * 8 + startOct2][0] = 1
  for i in range(199):
    # print(noteList[i + 1][1])
    noteList.append(nextChord(probVectorChordNot, probVectorChordOct, chordNotMarkov, chordOctMarkov, noteList[1 + i][0], noteList[1 + i][1]))
  return noteList

def nextChord(vectChordNot, vectChordOct, markovChordNot, markovChordOct, lastNot, lastOct):
  nextVectNot = np.matmul(markovChordNot, vectChordNot)
  nextVectOct = np.matmul(markovChordOct, vectChordOct)
  newNote = randomPickVector(nextVectNot)
  newOct = randomPickVector(nextVectOct)
  global probVectorChordNot
  probVectorChordNot = np.zeros((144, 1))
  for i in range(len(nextVectNot)):
    noteProb = nextVectNot[i][0]
    probVectorChordNot[lastNot * 12 + i][0] = noteProb
  global probVectorChordOct
  probVectorChordOct = np.zeros((64, 1))
  for i in range(len(nextVectOct)):
    octProb = nextVectNot[i][0] 
    probVectorChordOct[lastOct * 8 + i][0] = octProb
  return [newNote, newOct]
