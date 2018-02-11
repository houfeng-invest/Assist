import  os
from PIL import  Image,ImageFilter
# import matplotlib.pyplot as plt
# currentPath = os.path.abspath('.')
# img = Image.open('addd.png')
# img = img.filter(ImageFilter.CONTOUR)
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.imshow(img)
# plt.show()


class ChangeImageColor(object):
    @classmethod
    def startHandle(self,rgb):
        path = os.getcwd()
        npath = os.getcwd() + '/newiamges/'
        if not os.path.exists(npath):
            os.makedirs(npath)
        else:
            for root,dirs ,files in os.walk(npath):
                for file_name in files:
                    os.remove(npath + file_name)
        nr,ng,nb = rgb
        print("new color r:" + str(nr) + "g:" +str(ng) + "b:" +str(nb))
        br,bg,bb,ba = 0, 0,0,0
        for root,dirs,files in os.walk(path):
            print('root:',root)
            print('dirs: ',dirs)
            print('files:',files)
            for file_name in files:
                file_path = root + '/' + file_name
                if os.path.splitext(file_path)[1] == '.png':
                    image = Image.open(file_path)
                    if image is not None:
                        print('修改 ' + file_name + "的颜色")
                        image_width ,image_height =image.size
                        for i in range(image_width):
                            for j in range(image_height):
                                xy =(i,j)
                                color = image.getpixel(xy)
                                color_num = len(color)
                                if color_num == 4:
                                   r,g,b,a = color
                                   if i == 0 and j == 0:
                                       br,bg,bb,ba = color
                                   if br != r or bg != g or bb != b:
                                     image.putpixel(xy,(nr,ng,nb,a))
                                elif color_num == 3:
                                    print('rgb')
                                    r,g,b = color
                                    if i== 0 and j == 0:
                                        br,bg,bb = color
                                    if br != r or bg != g or bb != b:
                                        image.putpixel(xy,(nr,ng,nb))
                        image.save(npath+file_name)
    @classmethod
    def hex2rgb(self,hexcolor):
        rgb = ((hexcolor >> 16) & 0xff,(hexcolor >> 8) & 0xff,(hexcolor & 0xff))
        return rgb


# reSize = (100,100)
def filter(path,newSize = (-1,-1),scale = 0.5):
    for i in os.listdir(path):
        subPath = path+"/"+i
        if os.path.isdir(subPath):
            filter(subPath)
        elif os.path.splitext(subPath)[1] == '.png':
            img = Image.open(subPath)
            w,h = img.size
            if newSize[0] != -1  and newSize[1] != -1 :
                w,h = newSize
            nw , nh = int(w * scale),int(h * scale)
            if nw < 296 or nh < 550 :
                return
            print(i," 从 ",(w,h),"转换为 ",(nw,nh))
            newImg = img.resize((nw , nh))
            newImg.save(subPath)

#filter(currentPath)
hexColor = ChangeImageColor.hex2rgb(int('0x1A96D5',16))
ChangeImageColor.startHandle(hexColor)