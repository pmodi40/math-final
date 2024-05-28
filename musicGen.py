# Pranjal Modi: musicGen Class
# Includes all the methods used to generate new "Bach-inspired" pieces of music

# Import Statements: These load in all of the modules that'll be critical to the functioning of this class later on.
import os # Used to parse through the music directory for midi files.
import pretty_midi # Used to convert the midi files into program-parsable code.
import random # Used to take advantage of probability vectors in the Markov Chain.
import numpy as np # Used to load in and manipulate matrices.

# Initialization for several key global variables: the supported notes list, and all probability vectors.
NotesList = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
probVectorNot = np.zeros((12, 1))
probVectorOct = np.zeros((8, 1))
probVectorChordNot = np.zeros((144, 1))
probVectorChordOct = np.zeros((64, 1))

"""
Legacy Code: Files have already been loaded in to generate the premade stochastic matrices.

# Converts double lists of the format [[directory, file], ...] into lists of the format ["filePath/fileName", ...]
def collapse(dubList):
    music = []
    for i in dubList:
        adder = i[0]
        for j in range(1, len(i)):
            music.append(adder + "/" + i[j])
    return music

# Goes through the music directory and creates a double list of the format [[directory, file], ...]
musicList = []
for (dir, dir_name, file) in os.walk("music"):
    musicList.append([dir] + file)

# Converts this double list into a list of relevant file paths.
musicList = collapse(musicList)
"""

def createNormMusic(fileName, startNoteOct):
  # Given a file name and starting note-octave combo (of the form "NoteNameOctaveName", such as "C#5"), creates a music piece of 300 total notes, solely using a note-by-note Markov Chain.
  startOct = int(startNoteOct[-1])
  startNot = find(startNoteOct[0:len(startNoteOct) - 1], NotesList)
  allMarkovs = markov(musicList)
  markovNot = allMarkovs[0]
  markovOct = allMarkovs[2]
  allNotes = createMusNorm(startNot, startOct, markovNot, markovOct)
  noteListToMidi(fileName + ".mid", allNotes)

def createChordMusic(fileName, startNoteOct1, startNoteOct2):
  # Given a file name and a starting two note-octave combos (i.e. "C#4" and "D5"), creates a music piece of 301 total notes, using a two-note chord-based Markov Chain.
  startOct1 = int(startNoteOct1[-1])
  startNot1 = find(startNoteOct1[0:len(startNoteOct1) - 1], NotesList)
  startOct2 = int(startNoteOct2[-1])
  startNot2 = find(startNoteOct2[0:len(startNoteOct2) - 1], NotesList)
  allMarkovs = markov(musicList)
  markovChordNot = allMarkovs[1]
  markovChordOct = allMarkovs[3]
  allNotes = createMusChord(startNot1, startNot2, startOct1, startOct2, markovChordNot, markovChordOct)
  noteListToMidi(fileName + ".mid", allNotes)

def markov(files):
  # Returns markov chains associated with the corpus
  """
  # Legacy Code: Built to handle a list of files, rather than premade text-based matrices

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
    markovOct[firstOct][i] += 1
    firstOct = i
  markovNot = freqToMarkov(markovNot)
  np.save("stochastics/markovNot.npy", markovNot)
  markovChord = freqToMarkov(chordMarkov(allNotes))
  np.save("stochastics/markovChord.npy", markovChord)
  markovChordOctave = freqToMarkov(chordOctaveMarkov(allOctaves))
  np.save("stochastics/markovChordOctave.npy", markovChordOctave)
  markovOct = freqToMarkov(markovOct)
  np.save("stochastics/markovOct.npy", markovOct)
  return [markovNot, markovChord, markovOct, markovChordOctave]
  """
  return [np.load("stochastics/markovNot.npy"), np.load("stochastics/markovChord.npy"), np.load("stochastics/markovOct.npy"), np.load("stochastics/markovChordOctave.npy")]

def genData(midiFile):
  # Returns a double list of notes and octaves of the format [[note, octave], ...] given a midi file
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
  # Loops within a triple-nested list to find every item with a particular index in the most nested component
  arr = []
  for i in list:
      for j in i:
        arr.append(j[ind])
  return arr

def find(desid, within):
  # Returns the index of "within" inside the collection "desid"
  for i in range(0, len(within)):
    if within[i] == desid:
      return i
  return None


def freqToMarkov(freq):
  # Converts a frequency matrix into a column-stochastic matrix
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
  # Creates the second-order column-stochastic matrix for octaves
  octMatr = np.zeros((64, 8))
  for i in range(2, len(octaves)):
    minusTwoOct = octaves[i - 2]
    minusOneOct = octaves[i - 1]
    octave = octaves[i]
    octMatr[minusOneOct + 8 * minusTwoOct][octave] += 1
  return octMatr

def chordMarkov(notes):
  # Creates the second-order column-stochastic matrix for notes
  chordMatr = np.zeros((144,12))
  for i in range(2, len(notes)):
    minusTwoNote = notes[i-2]
    minusOneNote = notes[i-1]
    note = notes[i]
    chordMatr[minusOneNote + 12 * minusTwoNote][note] += 1
  return chordMatr

def createMusNorm(startNote, startOct, markovNot, markovOct):
  # Creates a nested list of the form [[note, octave], ...] that represents the entire generated music piece with the first-order Markov chains
  probVectorNot[startNote] = 1
  probVectorOct[startOct] = 1
  noteList = [[startNote, startOct]]
  for i in range(199):
    noteList.append(nextNorm(probVectorNot, probVectorOct, markovNot, markovOct))
    print(probVectorNot)
    print(probVectorOct)
  return noteList

def randomPickVector(vector):
  # Given a stochastic vector, return a probability-weighted index (i.e. "randomly" chosen with the weights). If the stochastic vector is insufficient, return a random valid index.
  randomNum = random.random()
  for i in range(len(vector)):
    randomNum -= vector[i][0]
    if (randomNum <= 0):
      return i
  return random.randint(0, len(vector) - 1)

def nextNorm(vectNot, vectOct, markovNot, markovOct):
  # Determines the next note-octave combo using the first-order Markov chain
  nextVectNot = np.matmul(markovNot, vectNot)
  nextVectOct = np.matmul(markovOct, vectOct)
  newNote = randomPickVector(nextVectNot)
  newOct = randomPickVector(nextVectOct)
  global probVectorNot
  probVectorNot = nextVectNot
  global probVectorOct
  probVectorOct = nextVectOct
  return [newNote, newOct]

def noteListToMidi(midiFileName, notes):
  # Converts a nested list of the form [[note, octave], ...] into a midi file called midiFileName, which is produce in the directory.
  newMidi = pretty_midi.PrettyMIDI()
  harpsichordProgram = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
  harpsichord = pretty_midi.Instrument(program=harpsichordProgram)
  curTime = 0
  for i in range(0, len(notes)):
    accNote = str(NotesList[notes[i][0]]) + str(notes[i][1])
    pitchNum = pretty_midi.note_name_to_number(accNote)
    dur = random.random() / 9 + 0.1
    note = pretty_midi.Note(velocity=100, pitch = pitchNum, start = curTime, end = curTime + dur - 0.15)
    curTime += dur
    harpsichord.notes.append(note)
  newMidi.instruments.append(harpsichord)
  newMidi.write(midiFileName)

def createMusChord(startNote1, startNote2, startOct1, startOct2, chordNotMarkov, chordOctMarkov):
  # Creates a nested list of the form [[note, octave], ...] that represents the entire generated music piece with the second-order Markov chains
  noteList = [[startNote1, startOct1], [startNote2, startOct2]]
  probVectorChordNot[startNote1 * 12 + startNote2][0] = 1
  probVectorChordOct[startOct1 * 8 + startOct2][0] = 1
  for i in range(299):
    noteList.append(nextChord(probVectorChordNot, probVectorChordOct, chordNotMarkov, chordOctMarkov, noteList[1 + i][0], noteList[1 + i][1]))
  return noteList

def nextChord(vectChordNot, vectChordOct, markovChordNot, markovChordOct, lastNot, lastOct):
  # Determines the next note-octave combo using the second-order Markov chain for chords
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

