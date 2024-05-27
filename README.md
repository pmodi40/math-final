# Using Markov Chains to Generate Bach Music
**Note that the pretty_midi and numpy libraries are *required* to run this program. These libraries can be installed with the terminal commands `pip install pretty_midi` and `pip install numpy`, respectively.**
To create music of your own with a first-order Markov Chain, run the command:
`python3 Driver.py F fileName firstNoteOctaveCombo`
To create music of your own with a second-order Markov Chain, run the command:
`python3 Driver.py S fileName firstNoteOctaveCombo secondNoteOctaveCombo`
Leave out the extension when choosing a fileName, and note that the Note-Octave combos must be formatted like this: `C5`, `D#2`, etc. Octaves go from one to eight, and valid notes can be found in this list `[C, C#, D, D#, E, F, F#, G, G#, A, A#, B]`.
