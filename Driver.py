import musicGen, sys

mode = sys.argv[1]
fileName = sys.argv[2]

if mode == "F":
    musicGen.createNormMusic(fileName, sys.argv[3])
elif mode == "S":
    musicGen.createChordMusic(fileName, sys.argv[3], sys.argv[4])
