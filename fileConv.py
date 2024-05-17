import sys
import subprocess
# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pretty_midi'])

import pretty_midi

def genData(midiFile):
  # Made to unpack the following data points into a list of lists:
  # Note, Velocity, Tempo, Time
  print("Stub")

  
