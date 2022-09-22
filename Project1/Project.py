import cv2
import numpy as np
import time

source = cv2.VideoCapture("samplefile.mp4")
source.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
source.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
source.set(cv2.CAP_PROP_FPS, 30)

isLINE = False
isGrey = False
imgCount = 0
record = False
isPaused = False
isROI = False
isRECT = False
isCIRCLE = False
evt=0
pnt1 = None
pnt2 = None
points=[]
count = 0
x1 = 0
y1 = 0
x2 = 0
y2 = 0

roiwidth=0
roiheight=0

radius=0

key = cv2.waitKey(1)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter('output.avi',fourcc,20.0, (640,480))
cv2.namedWindow("frame")

def mouseClick(event , xPos , yPos , flag , param):
   global pnt1
   global pnt2
   global evt
   global x1, y1
   global x2, y2
   global count , radius,points,pointsnp
   global roiwidth , roiheight
   if isRECT or isROI or isCIRCLE or isLINE:
      if event == cv2.EVENT_LBUTTONDOWN:
          evt = event
          if evt==1:
             count = count + 1
          print(count, "down")
          if count==1:
              x1=xPos
              y1=yPos
              pnt1 = (xPos, yPos)
              points.append(pnt1)
          elif count==2:
              pnt2=(xPos,yPos)
              x2 = xPos
              y2 = yPos
              roiwidth = int(x2 - x1)
              roiheight = int(y2 - y1)
              radius=int((((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5)
              points.append(pnt2)
      elif event == cv2.EVENT_LBUTTONUP:
          if count == 2:
            evt = event
            count = 0
      pointsnp = np.array(points, dtype=int)

cv2.setMouseCallback("frame", mouseClick)


while source.isOpened():
   print(points)
   print(roiwidth, roiheight)
   key = cv2.waitKey(1)
   if not isPaused:
      ret, vid = source.read()
      if isLINE:
          isCIRCLE=False
          isRECT=False
          if evt==4 or evt==1:
              if len(points) >= 2:
                  cv2.polylines(vid, [pointsnp], False, (255, 0, 0), 3)
      if isROI:
          if evt == 4:
            cv2.rectangle(vid, pnt1, pnt2, (0, 255, 0), 2)
            ROI=vid[pnt1[1]:pnt2[1], pnt1[0]:pnt2[0]]
            ROIres = cv2.resize(ROI, (roiwidth, roiheight))
            vid[0:roiheight, 0:roiwidth] = ROIres
            isRECT = False
            isCIRCLE = False
            isLINE=False

      elif isRECT:
         if evt == 4:
            cv2.rectangle(vid, pnt1, pnt2, (0, 255, 0), 2)
            isROI = False
            isLINE=False
            isCIRCLE=FALSE
      elif isCIRCLE:
          if evt==4:
            cv2.circle(vid, (x1, y1), radius, (0,255, 150), 2)
            isLINE = False
            isROI = False
            isRECT = False
      gray = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)


      if key== ord("i"):
          isROI = True
      if key== ord("c"):
          isCIRCLE = True
      elif key== ord("t"):
         isRECT = True
      elif key == ord("g"):
         isGrey = True
         cv2.destroyWindow("frame")
      elif key == ord("l"):
          isLINE = True
      elif key == ord("n"):
         isGrey = False
         cv2.destroyWindow("Grayscale")
      elif key==ord("s"):
         img_name = "opencv_{}.png".format(imgCount)
         cv2.imwrite(img_name, vid)
         imgCount =imgCount+ 1
      elif key == ord("v"):
          record=True
      elif key == ord("b"):
          record = False
      elif key == ord("p"):
          isPaused = True
      elif key == ord("r"):
          isROI=False
          isRECT=False
          isCIRCLE=False
          isLINE=False
          points=[]
          pointsnp.fill(0)
      if key == 43:
          roiwidth = roiwidth+10
          roiheight = roiheight+10
      elif key == 45:
         if roiwidth >= 0 & roiheight >= 0:
            roiwidth = roiwidth - 5
            roiheight = roiheight - 5

      if isGrey:
          cv2.imshow("Grayscale", gray)
          cv2.moveWindow("Grayscale", 200, 100)
      else:
          cv2.imshow("frame", vid)
          cv2.moveWindow("frame", 200, 100)
      if record:
          out.write(vid)
   elif key == ord("o"):
     isPaused = False
   if (key == ord("q")) or (key == 27):
       cv2.destroyAllWindows()
       break
source.release()
cv2.destroyAllWindows()
