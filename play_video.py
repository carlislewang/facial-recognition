import numpy as np
import cv2
import time

"""
OpenCV code for playing a video and getting the frame number. 

Adapted from:
http://docs.opencv.org/trunk/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
"""
def playVideo(videofile, n):
    for i in range(1,n+1):
        print "part"+str(i)
        filename = videofile + str(i) + ".mp4"
        cap = cv2.VideoCapture(filename)

        frame_number = 1
        flag = 1
        while(cap.isOpened()):
        # capture a frame from the video
            for j in range(0,2):
                ret, frame = cap.read()
                if ret == False:
                    flag = 0
                frame_number = frame_number + 1
            if flag == 0:
                break
        # Display the frame in the window "video"
        # the variable frame holds an image, just like a normal image
            cv2.imshow('application', frame)
            #print time.clock()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return
            
    # release the video capture
        cap.release()

    cv2.destroyAllWindows()

def main():
    videofile = "./material/show"
    playVideo(videofile, 17)

if __name__ == "__main__":
    main()

