import sys
import subprocess
# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pretty_midi'])

import pretty_midi

# Create fields and constructor!

markov = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
NotesList = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
"""
def __init__(self, file):
  # Could always just pre-build the notes you take, exclude the rest for standardization
  fullArr = genData(file)
  allNotes = listDubInd(fullArr, 0)
  
  for i in allNotes
"""
      

def genData(midiFile):
  midi_data = pretty_midi.PrettyMidi(midiFile)
  tempo = midi_data.estimate_tempo()
  notesCol = []
  """
  General Structure:
  [Note *Name*, Note *Number*, Velocity, Duration, Instrument]
  """
  for i in midi_data.instruments:
    for j in i.notes:
      print(pretty_midi.note_number_to_name(j.pitch))
      #notesCol.append([pretty_midi.note_number_to_name(j.pitch), j.pitch, j.velocity, j.get_duration(), i.name])
  # Made to unpack the following data points into a list of lists:
  # Note, Velocity, Tempo, Time
  # return notesCol

def listDubInd(list, ind):
  arr = []
  for i in list:
    arr.append(i[ind])
  return arr

genData("bach.mid");
