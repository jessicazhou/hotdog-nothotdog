#####################################################
##               stream bag + display results of post processing accordingly                         ##
#####################################################

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


# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read live stream (formerly recorded bag scheme) and display depth stream in jet colormap.\
                                Remember to change the stream resolution, fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-i", "--input", type=str, help="Path to the bag file")
# Parse the command line arguments to an object
args = parser.parse_args()
# Safety if no parameter have been given
'''
 if not args.input:
    print("No input paramater have been given.")
    print("For help type --help")
    exit()
'''
# Check if the given file have bag extension
'''
if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()
'''
try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config objec#this is an altered version of this file: live stream (formerly recorded bag scheme)
    config = rs.config() #https://intelrealsense.github.io/librealsense/doxygen/classrs2_1_1config.html
    
    # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
    #rs.config.enable_device_from_file(config, args.input)

#this is an altered version of this file: live stream (formerly recorded bag schemehttps://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/read_bag_example.py)
    # Configure the pipeline to stream the depth stream
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 90)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in, there's more cv2 down VVV
    cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    
    # Create colorizer object
    colorizer = rs.colorizer()
    '''
    ;
    '''

    # Streaming loop
    while True:#this is an altered version of this file: live stream (formerly recorded bag)
        # Get frameset of depth 
        frames = pipeline.wait_for_frames() 

        # Get depth frame
        depth_frame = frames.get_depth_frame()
        depth_frame = frames.get_depth_frame().as_depth_frame()
        #print(depth_frame)

        #commented out so now it is greyscale - Colorize depth frame to jet colormap
       # depth_color_frame = colorizer.colorize(depth_frame)

       
        # Convert depth_frame to ***numpy array*** to render image in opencv
        depth_image = np.asanyarray(depth_frame.get_data()) #type numpy.ndarray
        #***aaron: good for ML and visualization

        #convert 16 bit to 8 bit unsigned -- this is a matrix
        scale_factor = .0256
        depth8 = (depth_image*scale_factor).astype(np.uint8)
        depth8_v = np.vectorize(depth8)
        print(depth8)






        #attempt from: link betweem cv.imread and something from realsense
        #https://docs.opencv.org/3.4/da/d0c/tutorial_bounding_rects_circles.html
       
        gray_test = cv2.cvtColor(depth8_v, depth8_v, cv2.COLOR_BGR2GRAY)

        '''
        DOCUMENTATION
        cv.CvtColor(src, dst, code)
        src – input image: 8-bit unsigned, 
        16-bit unsigned ( CV_16UC... ), or single-precision floating-point.
        '''

      #  gray_test = cv2.blur(gray_test, (3,3))

        '''
        # OPENCV: Render image in opencv window
        '''
        cv2.imshow("Depth Stream", gray_test) 
        

      #  cv2.imshow("Depth Stream", gray_test) 
        #TODO note- this is the current link between cv2 and the rs pipeline

        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
        
            break

finally:
    pass