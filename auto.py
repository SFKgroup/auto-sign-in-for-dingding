import time
import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
from datetime import datetime
def find():
    img = ImageGrab.grab(bbox=(0,0,2560,1600))
    img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    img = cv2.resize(img,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    template = cv2.imread('./d.png', 0)
    template_h, template_w = template.shape[:2]
    
    methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    pointl = []
    pointr = []
    bel = 10
    for meth in methods:
        # 匹配方法的真值
        method = eval(meth)
        res = cv2.matchTemplate(img, template, method)
        # 函数返回值就是矩阵的最小值，最大值，最小值的索引，最大值的索引。
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        #print(meth,min_val, max_val)
        if meth == 'cv2.TM_CCOEFF_NORMED':#越接近1信度越高
            if abs(1-max_val) > 0.1:pass
            elif abs(1-max_val) > 0.5:bel = bel - 1
            else:bel+=1
        elif meth == 'cv2.TM_CCORR_NORMED':#越接近1信度越高
            if abs(1-max_val) > 0.001:bel = bel - 1
            else:bel+=1
        elif meth ==  'cv2.TM_SQDIFF':#越小信度越高
            if min_val > 50000:bel = bel -1
            elif min_val > 20000:bel = bel -1
            if min_val <= 100:bel = bel + 2
        elif meth ==  'cv2.TM_SQDIFF_NORMED':#越接近0信度越高
            if abs(min_val) > 0.001:bel = bel - 1
            else:bel+=1
        # 如果是平方差匹配 TM_SQDIFF 或归一化平方差匹配 TM_SQDIFF_NORMED，取最小值
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + template_w, top_left[1] + template_h)

        pointl.append(top_left)
        pointr.append(bottom_right)
    print(bel)
    if bel < 10:return None,None
    midx = []
    midy = []
    for a,b in zip(pointl,pointr):
        midx.append((a[0]+b[0])//2)
        midy.append((a[1]+b[1])//2)
    midx.remove(max(midx))
    midx.remove(min(midx))
    midy.remove(max(midy))
    midy.remove(min(midy))
    return sum(midx)*2//len(midx),sum(midy)*2//len(midy)

tb = []
grand = open('./timetable.txt','r',encoding='utf-8')
while True:
    data = grand.readline().replace('\n','').replace(' ','').replace('\t','')
    if data == '':break
    elif '#' in data:pass
    else:tb.append(data.split(':'))
grand.close()
#make_check(psd,path)
t = datetime.now()
run = False
while True:
    for i in tb:
        if int(t.hour) == int(i[0]) and int(t.minute) == int(i[1]):
            run = True
            break
    if run:
        times = 25#最大寻找次数
        for i in range(times):
            x,y=find()
            if x != None:
                #pyautogui.moveTo(x, y, duration=0.25)
                pyautogui.click(x,y)
                times = i
                break
            else:pyautogui.scroll(800)#向上翻找
            time.sleep(1)
        for i in range(times+2):
            pyautogui.scroll(-800)#回滚
            time.sleep(1)
        print('Done!')
        run = False
    time.sleep(50)
    t = datetime.now()