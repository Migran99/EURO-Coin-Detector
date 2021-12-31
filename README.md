# EURO-Coin-Detector
This repository aims to build a fully automated Euro coin detector. It's still a WIP, so if you have any ideas or recommendations, I am opened to listening to them.

## Selecting the area

Homography is used to warp the image and get only the ROI. For that, the coins must be on a A4 paper.

The distribution of the coins does not matter (or at least it shouldn't). My algorithms detects the borders of the paper and transforms it into a cropped and stretched image of it.

### Original Image
<img src="images/torcida.jpeg" width="400"/>

### Warped Image
<img src="images/output.png" width="400"/>

### Results after detecting coins
My algorithm will output a cropped image of each coin:

<img src="images/coin0.png" height="150"/> <img src="images/coin1.png" height="150"/> <img src="images/coin2.png" height="150"/> <img src="images/coin3.png" height="150"/> <img src="images/coin4.png" height="150"/>

## Coin Detection - Dataset (WIP)

I tried a dataset from:
https://github.com/Pitrified/coin-dataset

But still some preprocessing is needed to isolate the coins the same way my algorithm do and not have a green background for example.

With this data and the raw input of the dataset, the ANN doesn't perform very well with the coins obtained by my algorithm.


## References
I used some software already developed or I was inspired by:
- https://docs.opencv.org/3.4/d3/db4/tutorial_py_watershed.html
- https://learnopencv.com/homography-examples-using-opencv-python-c/
- https://github.com/SuperDiodo/euro-coin-dataset/
