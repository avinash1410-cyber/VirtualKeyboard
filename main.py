from time import sleep
from turtle import rt
import cv2
import cvzone
import numpy as np
from pynput.keyboard import Controller
from cvzone.HandTrackingModule import HandDetector

cap=cv2.VideoCapture(0)
cap.set(3,600)
cap.set(4,400)

detector=HandDetector(detectionCon=0.8)
keys=[["Q","W","E","R","T"],
      ["Y","U","I","O","P"],
      ["A","S","D","F","G"],
      ["H","J","K","L"],
      ["Z","X","C","V","B"],
      ["N","M","/"]]

finalText="."
keyboard=Controller()
# def drawAll(img,buttonList):
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#         cv2.rectangle(img, button.pos, (x + w, y + h), (255, 255, 0), cv2.FILLED)
#         cv2.putText(img, button.text, (button.pos[0] + 25, button.pos[1] + 60), cv2.FONT_ITALIC, 2, (255, 0, 0), 5)
#
#     return img


#for trancperenecy background
def drawAll(img,buttonList):
    imgNew=np.zeros_like(img,np.uint8)
    for button in buttonList:
        x, y = button.pos
        # w, h = button.size
        cvzone.cornerRect(imgNew,(button.pos[0],button.pos[1],button.size[0],button.size[1]),20,rt=0)
        cv2.rectangle(imgNew,button.pos,(x+button.size[0],y+button.size[1]),(22,111,94),cv2.FILLED)
        cv2.putText(imgNew,button.text,(x+40,y+60),cv2.FONT_ITALIC,2,(21,27,150),3)

    out=img.copy()
    alpha=0.5
    mask=imgNew.astype(bool)
    print(mask.shape)
    out[mask]=cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]
    return out





class Button():
    def __init__(self, pos, text, size=[70,70]):
        if size is None:
            size = [100, 100]
        self.pos=pos
        self.text=text
        self.size=size


buttonList=[]
for i in range(3):
    for x, key in enumerate(keys[i]):
        buttonList.append(Button([80 * x + 30, 50 * 2 * i + 50], key))


while True:
    sucess,img=cap.read()
    img=detector.findHands(img)
    lmlist,bboxInfo=detector.findPosition(img)
    img=drawAll(img,buttonList)

    if lmlist:
        for button in buttonList:
            x,y=button.pos
            w,h=button.size

            if x<lmlist[8][0]<x+w and y<lmlist[8][1]<y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (0,0, 0), cv2.FILLED)
                cv2.putText(img, button.text, (button.pos[0] + 25, button.pos[1] + 60), cv2.FONT_ITALIC, 2, (255, 0, 0),
                            5)
                l, _, _=detector.findDistance(8,12,img,draw=False)
                print(l)

                if l<15:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, button.text, (button.pos[0] + 25, button.pos[1] + 60), cv2.FONT_ITALIC, 2,
                                (255, 0, 0),
                                5)
                    finalText += button.text
                    sleep(0.15)

    cv2.rectangle(img, (50,350), (700,450), (255, 255, 0), cv2.FILLED)
    cv2.putText(img, finalText, (100,400), cv2.FONT_ITALIC, 2, (255, 255, 255), 5)


    cv2.imshow("Image",img)
    cv2.waitKey(1)