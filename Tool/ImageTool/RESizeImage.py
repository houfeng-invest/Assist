
import  os
from PIL import  Image

currentPath = os.path.abspath('.')
# reSize = (100,100)
def resize(path,newSize = (-1,-1),scale = 0.5):
    for i in os.listdir(path):
        subPath = path+"/"+i
        if os.path.isdir(subPath):
            resize(subPath)
        elif os.path.splitext(subPath)[1] == '.png':
            img = Image.open(subPath)
            w,h = img.size
            if newSize[0] != -1  and newSize[1] != -1 :
                w,h = newSize
            nw , nh = int(w * scale),int(h * scale)
            if nw < 592 or nh < 1100 :
                continue
            print(i," 从 ",(w,h),"转换为 ",(nw,nh))
            newImg = img.resize((nw , nh))
            newImg.save(subPath)

resize(currentPath,scale=0.4)



