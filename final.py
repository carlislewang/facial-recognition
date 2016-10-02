import numpy as np
import cv2
import transparency as tp
import superimpose as si
import filename as f
import os
import read_csv as rc
import play_video as pv
import time

"""
Coded by Wang Ning at 16 Apr 2015
This project shows the second response video of myself and the initial movie at top,
and shows some avatars of other people, which are labeled with there expressions 
"""

#set_img function opens an image and resize it 
def set_img(file_path, w_scale, h_scale):
    img = cv2.imread(file_path)
    height, width = img.shape[:2]
    img = cv2.resize(img, (int(width*w_scale), int(height*h_scale)))
    return img

#appendix function return the format of frame names
#e.g. /avatar1/frames000001.jpg
def appendix(frame_num):
    prefix = "/avatar1/frames"
    num = str(frame_num)
    length = len(num)
    #print len(num)
    for i in range(0,6-length):
        num = "0" + num
    return prefix + num + ".jpg"

#get_instances function get data from a csv
def get_instances(i):
    csvfile_path = f.getcsvfile(i)
    csv_attributes = []
    csv_instances = []
    rc.parseCSV(csvfile_path, csv_attributes, csv_instances)
    return csv_instances

#get_expression_label gets the number of avatar,
#all the instances from the csvs and the frame number
#and returns the label image
def get_expression_label(i, csv_instances, frame_num):
    label_choice = getAnswer(int(frame_num), csv_instances[int(i)])
    label_name = classToIndex(label_choice)
    #generate the file path
    label_path = "./material/"+label_name+".jpg"
    if not os.path.exists(label_path):
        print label_path+" not exists"
    return cv2.imread(label_path)

#classtoIndex function return the label name according to the choice
def classToIndex(label):
    label = label.strip().lower()  # remove whitespace and lowercase
    if label == "neutral" or label == "none" or label == "g" or label == 0:
        return "neutral"
    elif label == "happy" or label == "a" or label == 1:
        return "happy"
    elif label == "sad" or label == "b" or label == 2:
        return "sad"
    elif label == "angry" or label == "c" or label == 3:
        return "angry"
    elif label == "disgusted" or label == "d" or label == 4:
        return "disgusted"
    elif label == "surprised" or label == "e" or label == 5:
        return "surprised"
    elif label == "nervous" or label == "f" or label == 6:
        return "nervous"

# getAnswe funtion do binary search through csv_instances
def getAnswer(frame_number, csv_instances):
    if frame_number > 16260:
        label = csv_instances[len(csv_instances) - 1][3]
        label = ''.join(ch for ch in label if ch.isalnum()) # strip non-alphanumeric chars
        return label
    begin = 0
    end = len(csv_instances)
    while begin < end: 
        mid = (begin+end)/2
        this_frame = csv_instances[mid][0]
        prev_frame = 0
        if mid != 0:
            prev_frame = csv_instances[mid-1][0]
        if this_frame == frame_number or (frame_number > prev_frame and frame_number <= this_frame):
            label = csv_instances[mid][3]
            label = ''.join(ch for ch in label if ch.isalnum()) # strip non-alphanumeric chars
            return label
        elif this_frame < frame_number:
           begin = mid
        else:
            end = mid

def main():
    print time.clock()
    #all the parameters of the project
    b_width_scale = 1.8
    b_height_scale = 1.3
    frame_num = 0
    response_file = "./video/movie.mp4"
    initial_file = "./material/realMovie.mp4"
    frame_width_scale = 0.7
    frame_height_scale = 0.7
    frame_row_offset = 30
    frame_col_offset = 50
    avatar_file = "./users/"
    avatar_num = 5
    avatar_width_scale = 0.5
    avatar_height_scale = 0.5
    avatar_row_offset = 510
    avatar_col_offset = 150
    avatar_col_gap = 230
    label_width_scale = 0.2
    label_height_scale = 0.2
    label_row_offset = avatar_row_offset - 65
    label_col_offset = avatar_col_offset
    label_col_gap = avatar_col_gap


    #set the background ready
    background_img = set_img("./material/background1.jpg", b_width_scale, b_height_scale)
    
    #add the response video and the initial movie
    cap_response = cv2.VideoCapture(response_file)
    cap_initial = cv2.VideoCapture(initial_file)
    
    #create a video writer
    b_height, b_width = background_img.shape[:2]
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
    movie_num = 1
    out = cv2.VideoWriter('./material/show'+str(movie_num)+'.mp4', fourcc , 30, (int(b_width),int(b_height)))
    
    #if videos can not be opened, print error and stop
    if not cap_response.isOpened():
        print "can't open response video!"
        return
    if not cap_initial.isOpened():
        print "can't open initial movie!"
        return

    #last_avatars store the last successful avatars
    last_avatars = []
    #csv_files_instances store all the instances read from csv
    csv_files_instances = []

    #set the last_avatars valid and get instances from csv
    for i in range(0,avatar_num):
        last_avatars.append("test")
        csv_files_instances.append(get_instances(i))

    #capture frames from video
    while (1):
        background_img = set_img("./material/background1.jpg", b_width_scale, b_height_scale)
        #capture every x frames from videos
        for i in range(0,1):
            ret_r, frame_r = cap_response.read()
            ret_i, frame_i = cap_initial.read()
            frame_num = frame_num + 1
        #see if meets the end of the movie
        if (not ret_r) or (not ret_i):
            print "End of the movie!"
            break
      
        #add frames into the background
        si.superimpose(background_img, frame_i, frame_width_scale, frame_height_scale, frame_row_offset, frame_col_offset)
        i_height, i_width = frame_i.shape[:2]
        #resize the response image
        frame_r = cv2.resize(frame_r, (i_width, i_height))
        si.superimpose(background_img, frame_r, frame_width_scale, frame_height_scale, frame_row_offset, frame_col_offset+(i_width*frame_width_scale)+20)

        #add avatars and expression labels into the background
        #get avatars
        for i in range(0,avatar_num):
            flag = 1
            print i
            avatar_file_name = avatar_file + f.getcurrentfilename(i) + appendix(frame_num)
            #if the frame exist
            if os.path.exists(avatar_file_name):
                avatar = tp.openFile(avatar_file_name)
                #see if the temporary avatar is usable
                #if it's too small after transparency, it is not usable
                if avatar.shape[0] < 10:
                    flag = 0
                elif avatar.shape[1] < 10:
                    flag = 0
            #if the temporary frame of avatars not exists, it is not usable
            else:
                flag = 0
            if flag == 0:
                print avatar_file_name + " not usable"
                #use the last successful avatar frame
                avatar = tp.openFile(str(last_avatars[i]))
            else:
                #store it as the last successful frame 
                last_avatars[i] = avatar_file_name

            #add avatar into the frame
            si.superimpose(background_img, avatar, avatar_width_scale, avatar_height_scale, avatar_row_offset, avatar_col_offset+(avatar_col_gap*i))
            label_img = get_expression_label(i, csv_files_instances, frame_num)
            #add labels into the frame
            si.superimpose(background_img, label_img, label_width_scale, label_height_scale, label_row_offset, label_col_offset+(label_col_gap*i))

        #write processed frames
        #re_frame = cv2.flip(background_img)
        out.write(background_img)
        print "frame" + str(frame_num)
        if frame_num % 1000 == 0:
        	movie_num = movie_num + 1
        	out = cv2.VideoWriter('./material/show'+str(movie_num)+'.mp4', fourcc , 30, (int(b_width),int(b_height)))
        #just for check
 #       cv2.imshow('Fianl_project', background_img)
    
    print time.clock()
    #release the videos capture and destroy windows 
    cap_response.release()
    cap_initial.release()
    out.release()
    cv2.destroyAllWindows()
    print "preprocessing has finished"
    pv.playVideo("./material/show", movie_num)

if __name__ == "__main__":
    main()
