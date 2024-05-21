import sys
import subprocess
# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pretty_midi'])

import pretty_midi
import numpy as np
# Create fields and constructor!

NotesList = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
markovNot = np.random.randint(0, size=(12,12))
markovOct = np.random.randint(0, size=(7,7))
lastNote = None

def __init__(self, files):
  # Could always just pre-build the notes you take, exclude the rest for standardization
  allData = []
  for i in files:
    allData.append(genData(i))
  allNotes = listTripInd(allData, 0)
  allOctaves = listTripInd(allData, 1)
  firstNote = allNotes[0]
  for i in allNotes[1:]:
    
    
  

      

def genData(midiFile):
  midi_data = pretty_midi.PrettyMIDI(midiFile)
  tempo = midi_data.estimate_tempo()
  notesCol = []
  """
  General Structure:
  [Note *Name*, Note *Number*, Velocity, Duration, Instrument]
  """
  for i in midi_data.instruments:
    for j in i.notes:
      note = pretty_midi.note_number_to_name(j.pitch)
      octave = note[-1]
      note = note[0:len(note) - 1]
      if note[-1] == "!" or note[-1] == "b":
        note = note[0]
      notesCol.append([find(note, NotesList), octave])
  return notesCol
      


def listTripInd(list, ind):
  arr = []
  for i in list:
      for j in I:
        arr.append(j[ind])
  return arr

def find(desid, within):
  for i in range(0, len(within)):
    if within[i] == desid:
      return i
  return None


genData("bach.mid");
