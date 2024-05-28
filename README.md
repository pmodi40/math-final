# Using Markov Chains to Generate Bach Music
**Note that the pretty_midi and numpy libraries are *required* to run this program. These libraries can be installed with the terminal commands `pip install pretty_midi` and `pip install numpy`, respectively.**

To clone this repository, use the command `git clone "git@github.com:pmodi40/math-final.git"` in your directory of choice; be sure to properly initialize git on your machine first, using the guides at https://docs.github.com/en/get-started/getting-started-with-git/set-up-git and https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent.

**Alternatively, just navigate to the "Code" dropdown on the main page of the repository and click on the "Download ZIP" option to receive all of the repository's contents without any setup.**

---

To create music of your own with a first-order Markov Chain, run the command:
`python3 Driver.py F fileName firstNoteOctaveCombo`

As an example, the command `python3 Driver.py F output C4` would produce a midi file named `output.mid` with a starting note of `C` and a starting octave of `4`.

---

To create music of your own with a second-order Markov Chain (*generally* more cohesive), run the command:
`python3 Driver.py S fileName firstNoteOctaveCombo secondNoteOctaveCombo`

As an example, the command `python3 Driver.py S output C3 D#3` would create a midi file named `output.mid` with starting notes of `C` and `D#` and starting octaves of `3` and `3`, using the second-order stochastic matrices.

**Leave out the extension when choosing a fileName**, and note that the Note-Octave combos must be formatted like this: `C5`, `D#2`, etc. Octaves go from one to eight, and valid notes can be found in this list `[C, C#, D, D#, E, F, F#, G, G#, A, A#, B]`.
