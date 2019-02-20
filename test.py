import numpy as np
import cv2

cap = cv2.VideoCapture("walking.mp4")
fgbg = cv2.createBackgroundSubtractorMOG2()
while(True):
    ret, frame = cap.read()
    ROIimg = frame[100:200, 100:200]
    fgmask = fgbg.apply(ROIimg)
    kernel = np.ones((3, 3), np.uint8)
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 2)
    th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
    dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
    contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) > 1000:  # 1600
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x+100, y+100), (x+100+w, y+100+h), (255, 255, 0), 2)  # here you add back the offset that you crop
            cv2.imshow('frame', frame)
            cv2.imshow('mask', fgmask)
    if cv2.waitKey(1) & 0xff == ord('q'):

        break
cap.release()
cv2.destroyALLWindow()
