import sys
import subprocess
# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pretty_midi'])

import pretty_midi

# Create fields and constructor!

noteList = []

def __init__(self, file):
  # Could always just pre-build the notes you take, exclude the rest for standardization
  fullArr = genData(file)
  allNotes = listDubInd(fullArr, 0)
  for j in allNotes:
    if j in listDubInd(allNotes, 0):
      
    else:
        

def genData(midiFile):
  midi_data = pretty_midi.PrettyMidi(midiFile)
  tempo = midi_data.estimate_tempo()
  notesCol = []
  """
  General Structure:
  [Note *Name*, Note *Number*, Velocity, Duration, ]
  """
  for i in midi_data.instruments:
    for j in i.notes:
      notesCol.append([pretty_midi.note_number_to_name(j.pitch), j.pitch, j.velocity, j.get_duration(), i.name])
  # Made to unpack the following data points into a list of lists:
  # Note, Velocity, Tempo, Time
  return notesCol

def listDubInd(list, ind):
  arr = []
  for i in list:
    arr.append(i[ind])
  return arr
  
