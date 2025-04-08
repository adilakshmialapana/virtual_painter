fingers=[]
if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
    fingers.append(1)
else:
    fingers.append(0)
for id in range(1,5):
    if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
        fingers.append(1)

    else:
        fingers.append(0)