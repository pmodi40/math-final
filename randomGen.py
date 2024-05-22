import fileConv
from os import walk

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



hi = fileConv.markov(musicList)[0]
print(hi)
