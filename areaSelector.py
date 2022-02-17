########################
#
#      --- - Area Selector for the EURO Coin Detector - ---
#   
#
#                   Miguel Granero Ramos 2021
####

import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.npyio import load

def loadImage(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.title('Original')
    #plt.show()
    return image

def filterImage(im):
    grayIm = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((5,5), np.float32) / 15
    filteredImage = cv2.filter2D(grayIm,-1, kernel)
    plt.imshow(cv2.cvtColor(filteredImage,cv2.COLOR_BGR2RGB))
    plt.title('Filtered image')
    #plt.show()
    return filteredImage

def thersholdImage(im, sensitivity = 140):
    hsv = cv2.cvtColor(im,cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
    lower_white = np.array([0,0,255-sensitivity])
    upper_white = np.array([255,sensitivity,255])
    ret, thresImage = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
    thresImage = cv2.inRange(hsv,lower_white,upper_white)
    
    plt.imshow(cv2.cvtColor(thresImage, cv2.COLOR_BGR2RGB))
    plt.title('Threshold Image')
    #plt.show()
    return thresImage

def sortCorners(corners):
    # Sort corners TL - TR - BL - BR
    top_corners = corners
    top_corners.sort(key=lambda y:y[1])
    top_corners = top_corners[0:2] 
    top_corners.sort() # Top corners by order of X coord

    bot_corners = corners
    bot_corners.sort(key=lambda y:y[1])
    bot_corners = bot_corners[2:4] 
    bot_corners.sort() # Bot corners by order of Y coord

    print('Top corners: ', top_corners)
    print('Bottom corners: ', bot_corners)

    ordered_corners = top_corners + bot_corners
    print('Ordered corners: ', ordered_corners)
    
    return ordered_corners

def detectCorners(im, original):
    contours, hier = cv2.findContours(im, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    canvas = original.copy()
    cv2.drawContours(canvas, cnt, -1, (0, 255, 255), 3)
    plt.title('Largest Contour')
    plt.imshow(canvas)
    #plt.show()
    
    epsilon = 0.02 * cv2.arcLength(cnt, True)
    approx_corners = cv2.approxPolyDP(cnt, epsilon, True)
    cv2.drawContours(canvas, approx_corners, -1, (255, 255, 0), 10)
    approx_corners = sorted(np.concatenate(approx_corners).tolist())

    approx_corners = [approx_corners[i] for i in [1, 0, 3, 2]] 
    #[1, 0, 3, 2]
    #[1, 2, 0, 3]
    print(approx_corners)
    

    ordered_corners = sortCorners(approx_corners)

    print('\nThe corner points are ...\n')
    for index, c in enumerate(ordered_corners):
        character = chr(65 + index)
        print(character, ':', c)
        cv2.putText(canvas, character, tuple(c), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    plt.imshow(canvas)
    plt.title('Corner Points')
    #plt.show()

    return np.float32(ordered_corners)

def destPoints(scale):
    # Get the dst points keeping the A4 aspect ratio
    w = int(21 * scale)
    h = int(29.7 * scale)

    destination_corners = np.float32([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])

    return destination_corners, h, w

def unwarpImage(img, src, dst, wr, hr):
    H, _ = cv2.findHomography(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    print('\nThe homography matrix is: \n', H)
    un_warped = cv2.warpPerspective(img, H, (wr, hr), flags=cv2.INTER_LINEAR)

    # plot

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    # f.subplots_adjust(hspace=.2, wspace=.05)
    ax1.imshow(img)
    ax1.set_title('Original Image')

    x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
    y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]

    ax2.imshow(img)
    ax2.plot(x, y, color='yellow', linewidth=3)
    #ax2.set_ylim([h, 0])
    #ax2.set_xlim([0, w])
    ax2.set_title('Target Area')

    #plt.show()
    return un_warped

def getCoinArea(filePath, sensitivity = 140):
    orImage = loadImage(filePath)
    #filImage = filterImage(orImage)
    thresImage = thersholdImage(orImage, sensitivity)
    src_corners = detectCorners(thresImage, orImage)

    dst_corners, h, w = destPoints(300)

    resImage = unwarpImage(orImage,src_corners,dst_corners,w,h)   
    plt.imshow(resImage)
    plt.title('Warped')
    #plt.show()
    resImage = cv2.cvtColor(resImage, cv2.COLOR_RGB2BGR)
    cv2.imwrite("images/output.png",resImage)
    return resImage

if(__name__ == "__main__"):
    getCoinArea("images/juntas.jpeg", 140) # Change sensitivity of the threshold