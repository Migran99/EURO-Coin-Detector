
import cv2
import numpy as np
import matplotlib.pyplot as plt



def getCoins(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(imgHSV,(0,0,0),(255,120,255))
    mask = cv2.bitwise_not(mask)
    plt.imshow(mask,cmap='gray')
    #plt.show()

    # Treat the mask to cover all the coins
    kernel = np.ones((5,5), np.uint8)
    morf = cv2.erode(mask, kernel, iterations=5)
    morf = cv2.dilate(mask, kernel, iterations=15)
    opening = cv2.morphologyEx(morf,cv2.MORPH_OPEN,kernel, iterations = 3)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,0)
    ret, sure_fg = cv2.threshold(dist_transform,0.6*dist_transform.max(),255,0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    plt.imshow(sure_fg,cmap='gray')
    #plt.show()

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0

    markers = cv2.watershed(img,markers)
    plt.imshow(markers)
    #plt.show()

    # Show the results of the segmentation + watershed
    print(markers.shape)
    result = img.copy()
    result[markers < 2] = [0,0,0]
    result[markers >= 2] = [255,255,255]
    plt.imshow(result, cmap='gray')
    #plt.show()

    # Blob detection of coins - get mask one by one
    nCoins = np.max(markers) - 1
    coins = []

    for i in range(nCoins):
        c = (markers==i+2)
        #c = cv2.cvtColor(c, cv2.COLOR_RGB2GRAY)
        coins.append(np.uint8(c))

    return coins

def processCoins(img, coins):
    # Recognition of coins  
    # yellow -> 180º
    nCoins = len(coins)

    # Process one by one, NOT FINISHED. At the moment it only saves it
    for i in range(nCoins):
        coinImg = cv2.bitwise_and(img, img, mask=coins[i])
        count, hier = cv2.findContours(coins[i], 1,2)
        x,y,w,h = cv2.boundingRect(count[0])
        coinImg = coinImg[y:y+h,x:x+w]
        cv2.imwrite("images/coin" + str(i) + ".png",coinImg)

        # Histogram analysis
        coinImg = cv2.cvtColor(coinImg, cv2.COLOR_RGB2HSV)
        h,s,v = cv2.split(coinImg)
        histH = cv2.calcHist(h, [0], None, [255], [0, 255])
        histS = cv2.calcHist(s, [0], None, [255], [0, 255])
        histV = cv2.calcHist(v, [0], None, [255], [0, 255])
        plt.figure()
        plt.plot(histH)
        plt.plot(histS)
        plt.plot(histV)


        plt.figure()
        plt.imshow(v, vmin=0, vmax=255)
        plt.colorbar()

if __name__ == "__main__":
    img = cv2.imread("images/output.png")
    coins = getCoins(img)
    processCoins(img,coins)