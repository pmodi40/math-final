import fileConv

musicList = []
for i in range(772, 818):
    musicList.append("music/bwv" + str(i) + ".mid")

hi = fileConv.markov(musicList)[1]
print(hi)
