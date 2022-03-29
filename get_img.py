import numpy as np
from PIL import ImageGrab
import cv2
import time
x = 100
y = 100
w = 100
h = 100
colour = 0
img = ImageGrab.grab(bbox=(0,0,2560,1600))
img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
img = cv2.resize(img,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA)
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
while True:
    image = img.copy()
    im = cv2.rectangle(image,(x,y),(x+w,y+h),colour)
    cv2.imshow('img',im)
    key = cv2.waitKey(0)
    if key == ord('a'):x = x - 5
    elif key == ord('d'):x = x + 5
    elif key == ord('w'):y = y - 5
    elif key == ord('s'):y = y + 5
    elif key == ord('q'):break
    elif key == ord('j'):w = w - 5
    elif key == ord('l'):w = w + 5
    elif key == ord('i'):h = h - 5
    elif key == ord('k'):h = h + 5
    elif key == ord('r'):cv2.imwrite('./d.png',img[y:y+h,x:x+w])
    elif key == ord('c'):
        if colour == 255:colour = 0
        else:colour = 255
    elif key == ord('f'):
        cv2.destroyWindow('img')
        time.sleep(0.5)
        img = ImageGrab.grab(bbox=(0,0,2560,1600))
        img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        img = cv2.resize(img,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.destroyWindow('img')