import musicGen, sys

mode = sys.argv[0]
fileName = sys.argv[1]

if mode == "F":
    musicGen.createNormMusic(fileName, sys.argv[2])
elif mode == "S":
    musicGen.createChordMusic(fileName, sys.argv[2], sys.argv[3])