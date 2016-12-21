#!/usr/bin/env python

##### The joints order is [0, 1, 20, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
        # 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24]

import rospy
import math
import json
import tf
import rosbag
from cv_bridge import CvBridge #, CvBridgeError
import os
from k2_client.msg import BodyArray, Body

#  from std_msg.msg import String






class SkeletonWriter():

    def __init__(self):
        self.inputpath='/home/ccoppola/Social_Activity_Detection_Data/'
        self.outputpath='/home/ccoppola/Social_Activity_Detection_Data/Output'
        self.joint = ['BaseSpine', 'MiddleSpine', 'Neck', 'Head', 'LShoulder',
                 'LElbow', 'LWrist', 'LHand', 'RShoulder', 'RElbow', 'RWrist',
                 'RHand', 'LHip', 'LKnee', 'LAnkle', 'LFoot', 'RHip', 'RKnee',
                 'RAnkle', 'RFoot', 'Spine Shoulder', 'TipLHand', 'LThumb',
                 'TipRHand', 'RThumb']




    def process_files(self):

        if not os.path.exists("%s" %(self.outputpath)):
            os.makedirs(self.outputpath)
        for root,path,files in os.walk(self.inputpath):
         # for files in os.listdir(self.inputpath):
            #  print files
            for name in files:
                if name.endswith('.bag'):
                    rosbagurl=os.path.join(root,name)
                    print rosbagurl

                    if not os.path.exists("%s/%s" %(self.outputpath,name.split(".")[0])):
                        os.makedirs("%s/%s" %(self.outputpath,name.split(".")[0]))
                        os.makedirs("%s/%s/color" %(self.outputpath,name.split(".")[0]))
                        os.makedirs("%s/%s/depth" %(self.outputpath,name.split(".")[0]))
                
                    self.process_bag(root,name)



    def process_bag(self,root,name):
        skel_index = 0
        color_index = 0
        depth_index = 0
        skeletons=dict()
        #  f_user1 = open("%s/%s/user1" %(self.outputpath,name.split(".")[0]),'w')
        #  f_user2 = open("%s/%s/user2" %(self.outputpath,name.split(".")[0]),'w')
        for topic, msg, t in rosbag.Bag(os.path.join(root,name)).read_messages():
            
            if topic == "/head/kinect2/k2_bodies/bodies":
                #  print type(msg)
                #  array = BodyArray()
                #  bb=Body()
                #  bb
                #  array.bodies[0].jointPositions
                #  array.bodies[0].jointOrientations
                for ind_body, body in enumerate(msg.bodies):
                    accumulated_string = ""
                    if not skeletons.has_key(body.trackingId):
                        skeletons[body.trackingId]=[]
                    for position, orientation in zip(body.jointPositions,body.jointOrientations):
                        accumulated_string += "%s %s %s %s %s %s %s %s" % (position.position.x,position.position.y,position.position.z,orientation.orientation.x,orientation.orientation.y,orientation.orientation.z,orientation.orientation.w,body.header.stamp)
                    #      accumulated_string =+ str(position.position.x) + " "
                    #      accumulated_string =+ str(position.position.y) + " "
                    #      accumulated_string =+ str(position.position.z) + " "
                    #      accumulated_string =+ str(position.orientation.x) + " "
                    #      accumulated_string =+ str(position.orientation.y) + " "
                    #      accumulated_string =+ str(position.orientation.z) + " "
                    #  accumulated_string =+ body.header.stamp
                    #  print body.trackingId
                    skeletons[body.trackingId].append(accumulated_string)
                print skeletons.keys()

                skel_index =+ 1
            elif topic == "/head/kinect2/k2_rgb/image/compressed":
                color_index =+ 1
            elif topic == "/head/kinect2/k2_depth/image":
                depth_index =+ 1

    def process_bodies(self,body_msg):
        numbodies=len(body_msg)
        for ind_body, body in enumerate(body_msg):
            for ind_joint, joint in enumerate(body.jointPositions):
                pass










def main():
    sk=SkeletonWriter()
    sk.process_files()


if __name__ == '__main__':
    main()
