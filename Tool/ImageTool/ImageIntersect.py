from  PIL import Image
import os
import shutil
import time
import matplotlib.pyplot as plt
import threading
import threadpool
img =Image.open('da_search_test.png')

img2 =Image.open('da_search_test4.png')


def imageIntersect(img1,imgPath2):
    '''
        检测的图像大小必须一致
    '''

    scale = 0.05
    alphaValue = 10

    img2 = Image.open(imgPath2)
    if img1.mode != "RGBA":
        return 0,0
    if img2.mode != "RGBA":
        return 0,0
    w1,h1 = img1.size
    w2,h2 = img2.size
    if w1 != w2 or h1 != h2:
        return 0,0
    w = int(w1 * scale)
    h = int(h1 * scale)
    w = 29
    h = 55
    img1 = img1.resize((w,h))
    img2 = img2.resize((w,h))

    dataCount = 0
    intersectCount = 0
    sourceCount = 0

    sourcePer = 0.0
    dataPer = 0.0
    for x in range(w):
        for y in range(h):
            rgba = img1.getpixel((x,y))
            a = rgba[3]
            rgba2 = img2.getpixel((x,y))
            if len(rgba) < 4:
                continue
            if len(rgba2) < 4:
                continue
            a2 = rgba2[3]
            if a > alphaValue and a2 > alphaValue:
                intersectCount =intersectCount + 1
            if a2 > alphaValue :
                dataCount = dataCount + 1
            if a > alphaValue:
                sourceCount = sourceCount + 1
    if dataCount <= 0 :
        return 0,0
    if sourceCount <= 0:
        return 0,0
    dataPer =   (intersectCount*1.0)/(dataCount*1.0)
    sourcePer = (intersectCount*1.0)/(sourceCount*1.0)
    return dataPer,sourcePer





def findMatchedImage(img1,imgDir):
    if os.path.exists('./findedimages'):
        shutil.rmtree('./findedimages')
    if not os.path.exists('./findedimages'):
        os.mkdir('./findedimages')
    count = 0
    for i in os.listdir(imgDir):
        subPath = imgDir+"/"+i
        if os.path.splitext(subPath)[1] == '.png':
            value = imageIntersect(img1,subPath)
            if value[0] > 0.4 and value[1] > 0.0:
                count = count + 1
                print(i + " finded")
                shutil.copyfile(subPath,'./findedimages/'+i)


class ImageFindJob(threading.Thread):
    def __init__(self,img1,imgPath2,num=0,threadLock=None):
        threading.Thread.__init__(self)
        self.num = num
        self.threadLock = threadLock
        self.img1 = img1
        self.imgPath2 = imgPath2

    def run(self):
        if self.threadLock:self.threadLock.acquire()
        # print('thread %d runing' % self.num)
        if os.path.splitext(self.imgPath2)[1] == '.png':
            value = imageIntersect(img1=self.img1,imgPath2=self.imgPath2)
            if value[0]> 0.4 and value[1] > 0.0 :
                imgFileName = self.imgPath2.split('/')[-1]
                print("find " + imgFileName + " ")
                shutil.copyfile(self.imgPath2,'./findedimages/'+imgFileName)
        if self.threadLock:
            self.threadLock.release()

def findMatcheImageByThread(img1,imgDir):
    if os.path.exists('./findedimages'):
        shutil.rmtree('./findedimages')
    if not os.path.exists('./findedimages'):
        os.mkdir('./findedimages')
    count = 0

    threads = []
    index = 1
    threadLock = threading.Lock()
    for i in os.listdir(imgDir):
        subPath = imgDir+"/"+i
        thread1 = ImageFindJob(img1=img1,imgPath2=subPath,num=index,threadLock=threadLock)
        thread1.start()
        threads.append(thread1)
        index += 1

    for t in threads:
        t.join()
    print("线程执行完成.")




def findIfIsMatched(i):
    img1 = Image.open("da_search_test1.png")
    value = imageIntersect(img1,i)
    if value[0]> 0.4 and value[1] > 0.0 :
        imgFileName = i.split('/')[-1]
        print("find " + imgFileName + " ")
        shutil.copyfile(i,'./findedimages/'+imgFileName)


def findMatcheImageByThreadpool(img1,imgDir):
    if os.path.exists('./findedimages'):
        shutil.rmtree('./findedimages')
    if not os.path.exists('./findedimages'):
        os.mkdir('./findedimages')

    fileList = [imgDir+"/"+i for i in os.listdir(imgDir) if os.path.splitext(imgDir+"/"+i)[-1] == '.png']

    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(findIfIsMatched,fileList)
    [pool.putRequest(req) for req in requests]
    pool.wait()

    print("线程执行完成.")


class Rect():
    def __init__(self,x=-1,y=-1,width=-1,height=-1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def toDict(self):
        return {"x":self.x,
                "y":self.y,
                "width":self.width,"height":self.height}
    def isNull(self):
        return self.x == -1 and self.y == -1 and self.width == -1
    def __str__(self):
        return "{"+"x:" + str(self.x) + ",y:"+str(self.y)+",width:"+str(self.width)+",height:"+str(self.height) +"}"

def findImageRect(img):
    rect = Rect()
    arrs = []
    if img:
        w = img.size[0]
        h = img.size[1]

        w = 89
        h = 165

        minX = w
        maxX = 0

        minY = h
        maxY = 0

        img = img.resize((w,h),Image.NORMAL)
        img.save("./rl_da_test_2.png")
        for y in range(h):
            for x in range(w):
                rgba  = img.getpixel((x,y))
                if rgba[3] > 0:
                    index = (w * y + x) * 4
                    arrs.append(index)
                    if x < minX:
                        minX = x
                    if x > maxX :
                        maxX = x
                    if y < minY:
                        minY = y
                    if y > maxY:
                        maxY = y

        rect.x = minX
        rect.y = minY
        rect.width = maxX - minX
        rect.height = maxY - minY

        if rect.width < 0 or rect.height < 0:
            print("error find image edge ")
            print(rect)
            rect = Rect()


    return rect,arrs



def findImageRectForTest(img):
    rect = Rect()
    arrs = []
    if img:
        w = img.size[0]
        h = img.size[1]
        minX = w
        maxX = 0

        minY = h
        maxY = 0

        for y in range(h):
            for x in range(w):
                rgba  = img.getpixel((x,y))
                if rgba[3] > 0:
                    index = (w * y + x) * 4
                    arrs.append(index)
                    if x < minX:
                        minX = x
                    if x > maxX :
                        maxX = x
                    if y < minY:
                        minY = y
                    if y > maxY:
                        maxY = y

        rect.x = minX
        rect.y = minY
        rect.width = maxX - minX
        rect.height = maxY - minY

        if rect.width < 0 or rect.height < 0:
            print("error find image edge ")
            print(rect)
            rect = Rect()


    return rect,arrs

def displayResult():
    count = 0
    dstImg = Image.open('./DA_Karute_body_front.png')
    for i in os.listdir("./findedimages"):
        subPath = "./findedimages"+"/"+i
        if os.path.splitext(subPath)[-1] == ".png":
            newImg = Image.open(subPath)
            dstImg.paste(newImg,mask=newImg)
            count = count + 1
    print("total finded " + str(count) + " images")
    dstImg.save('./dstimg.png','PNG')
    fig = plt.figure(figsize=(4,6))
    ax = fig.add_subplot(111)
    ax.imshow(dstImg)
    plt.show()

if __name__ == '__main__':
    img1 = Image.open('da_search_test6.png')

    # start = time.clock()
    # findMatchedImage(img1,'/Volumes/HDD/2017/Assist/GUI/images')
    # end = time.clock()
    # print("time: %f s" % (end - start))
    # displayResult()

    # test = findImageRect(img1)
    # print(test[0])
    # print(test[1])

    img1 = Image.open('da_search_test6.png')
    test = findImageRect(img1)
    print(test[0])
    print(test[1])

    # start = time.clock()
    # findMatcheImageByThread(img1,'/Volumes/HDD/2017/Assist/GUI/images')
    # end = time.clock()
    # print("time: %f s" % (end - start))
    # displayResult()

    # start = time.clock()
    # findMatcheImageByThreadpool(img1,'/Volumes/HDD/2017/Assist/GUI/images')
    # end = time.clock()
    # print("time: %f s" % (end - start))
    # displayResult()