import sys
#sys.append.append('/usr/local/lib')
# First import library
import pyrealsense2 as rs
#this is an altered version of this file: https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/read_bag_example.py

# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path

'''
NOTE from aaron! 
-- rectangle could be a good counterbalance to all the variance that happens in the video

given a snapshot of depth data at a given instance
calculate an approximate volume of contents of the box
 
inputs
-- dimensions of cropped matrix: x, y 
-- dimensions of box: box_x, box_y
-- depths (distance from camera to ___): floor, box_top

high level: of our known cropped matrix + known dimensioned box
we are splitting it into many many small triangular prisms
with a pyramid top

tri_base = (box_x * box_y) / (x*y*2) < - the area of the triangular base

ITERATING THROUGH THE MATRIX
--- load a matrix
--- determine smallest = lowest_pt 
--- determine largest = highest_pt
-- prism = tri_base * lowest_pt
-- pyramid = 1 /3 * tri_base * highest_pt 
        V = 1/3(Ah)
            A = tri_base
            h = highest_pt
-- slice = prism + pyramid
-- total_converse += slice

true_volume = (box_x * box_y * floor) - (total_converse)
'''

#TODO subprocess that fills in 0 values
def normalizer(x,y):
    

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 90)
pipeline.start(config)
frames = pipeline.wait_for_frames()
depth_frame = frames.get_depth_frame()
depth_frame = frames.get_depth_frame().as_depth_frame()
depth_image = np.asanyarray(depth_frame.get_data())
# '''/*
#scale_factor = .03921 #this is an inches scaling (inch x .0254 = meter)
scale_factor = .09959 #centimeter scaling (meter scaling is an approximation)
depth8 = (depth_image*scale_factor).astype(np.uint8) #ndarray


'''
print("ITERATIVE PRINTING OF DEPTH")
for i in depth8:
    print(i)
'''

print("ITERATIVE PRINTING OF DEPTH LENGTH")
for i in depth8:
    print(len(i))

print("FULL DEPTH8 PRINT")
print(depth8)


#x = 640
#y = 460

#TODO cropping image manually -- check the approximate coordinates and then create a submatrix
#of depth8
#TODO different height inputs (should be dynamic) NOTE compensating for error

min_x = 200
min_y = 48
max_x = 400
max_y = 248

#TODO preprocessing should yield an approximate square
#NOTE camera should be directly overhead as much as possible such that its directly overhead the edge
x = max_x-min_x
y = max_y-min_y

cropped_depth8 = depth8[min_y: max_y +1, min_x: max_x+1] #rows are first -- column minor format

cv2.imwrite("cropsnap.png", cropped_depth8)
img = cv2.imread('cropsnap.png', 1)
#cv2.imshow('image',img)

origin_val = 0
right = 0
down = 0
diagonal = 0


#TODO average neighor if 0 (error)
for x in (0,200): #traverse 0 --> 199
    for y in (0,200):
        #seed and filter: input (x,y)
        origin_val = cropped_depth8[y][x]
        if origin_val == 0:
            normalizer(x,y)
        right = cropped_depth8[y][x+1]
        if right == 0:
            normalizer(x+1,y)
        down = cropped_depth8[y-1][x]
        if down == 0:
            normalizer(x,y-1)
        diagonal = cropped_depth8[y-1][x+1]
        if diagonal == 0: 
            normalizer(x+1,y-1)
        group = [origin_val, down, right, diagonal]

        #find largest
        largest = origin_val
        smallest = origin_val
        for i in group:
            if i > largest:
                largest = i
            if i < smallest:
                smallest = i

        #calculations
            
        



        #group actions - normalize w averages of neightbors when 0,
                    #  - find largest for calculations




box_x = .5
box_y = .5

box_top = 1
floor = 1.25

tri_base = (box_x * box_y) / (x*y*2)
rec_base = (box_x * box_y) / (x*y)


#print(img)






