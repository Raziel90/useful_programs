#!/usr/bin/env python
import tf
import rospy
import rosbag
from cv_bridge import CvBridge #, CvBridgeError
#import cv2
#from sensor_msgs.msg import Image
import os


                        
def handle_tf(transform,string_to_write,consensus_to_write,last_received,t,f):
#    print transform.child_frame_id
    y,p,r=tf.transformations.euler_from_quaternion([transform.transform.rotation.x,transform.transform.rotation.y,transform.transform.rotation.z,transform.transform.rotation.w])
    coordinate_str="%s %s %s %s %s %s" %(transform.transform.translation.x,transform.transform.translation.y,transform.transform.translation.z,r,p,y)
    
    if "head" in transform.child_frame_id:
        decision=0
    elif "neck" in transform.child_frame_id:
        decision=1
    elif "torso" in transform.child_frame_id:
        decision=2
    elif "left_shoulder" in transform.child_frame_id:
        decision=3
    elif "left_elbow" in transform.child_frame_id:
        decision=4
    elif "right_shoulder" in transform.child_frame_id:
        decision=5
    elif "right_elbow" in transform.child_frame_id:
        decision=6
    elif "left_hip" in transform.child_frame_id:
        decision=7
    elif "left_knee" in transform.child_frame_id:
        decision=8
    elif "right_hip" in transform.child_frame_id:
        decision=9
    elif "right_knee" in transform.child_frame_id:
        decision=10
    elif "left_hand" in transform.child_frame_id:
        decision=11
    elif "right_hand" in transform.child_frame_id:
        decision=12
    elif "left_foot" in transform.child_frame_id:
        decision=13
    elif "right_foot" in transform.child_frame_id:
        decision=14
    
#    if consensus_to_write[decision] & (last_received[decision]<t):
#        print "overwriting a previous joint"
    if (consensus_to_write[decision]==False) | (last_received[decision]<t):
        """I take the most recent sample"""
        consensus_to_write[decision]=True
        string_to_write[decision]=coordinate_str
        last_received[decision]=t
    dec=True
    for decs in consensus_to_write:
        dec=dec&decs
#    dec=dec&(last_received[decision]<t)
    if dec:
        final_string="%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n"%(string_to_write[0],string_to_write[1],string_to_write[2],string_to_write[3],string_to_write[4],string_to_write[5],string_to_write[6],string_to_write[7],string_to_write[8],string_to_write[9],string_to_write[10],string_to_write[11],string_to_write[12],string_to_write[13],string_to_write[14])     
        f.write(final_string)
        f.flush()
#        print "finally written!"
        string_to_write= ["" for x in range(15)]
        consensus_to_write= [ False for x in range(15)]
        return 1,string_to_write,consensus_to_write
    else:
        return 0,string_to_write,consensus_to_write
        

                        

distance = float(-1)
t_stamp = dict()
bridge = CvBridge()

#outputpath="/home/claudio/LCAS/Social-behaviour/isr_social_behaviour_dataset_images"
outputpath="/media/claudio/INTENSO/Social-behaviour/isr_social_behaviour_dataset_images"
#cv2.namedWindow("test")

for root, action_dirs, files in os.walk("/media/claudio/INTENSO/Social-behaviour/isr_social_behaviour_dataset/"):
    for name in files:
        if name.endswith(".bag"):
            rosbagurl = os.path.join(root, name)
            colorindex=0
            depthindex=0
            user1index=0
            user2index=0

            if not os.path.exists("%s/%s/%s/%s_color" % (outputpath,rosbagurl.split("/")[7],rosbagurl.split("/")[6],name.split(".")[0])):
                    os.makedirs("%s/%s/%s/%s_color" % (outputpath,rosbagurl.split("/")[7],rosbagurl.split("/")[6],name.split(".")[0]))
                    os.makedirs("%s/%s/%s/%s_gray8" % (outputpath,rosbagurl.split("/")[7],rosbagurl.split("/")[6],name.split(".")[0]))
                    os.makedirs("%s/%s/%s/%s_gray16" % (outputpath,rosbagurl.split("/")[7],rosbagurl.split("/")[6],name.split(".")[0]))
#            if "_t0" in name:
            print name
            f1 = open("%s/%s/%s/%s_%s.txt" % (outputpath,rosbagurl.split("/")[7],rosbagurl.split("/")[6],name.split(".")[0]    ,"user1"),'w')
            f2 = open("%s/%s/%s/%s_%s.txt" % (outputpath,rosbagurl.split("/")[7],rosbagurl.split("/")[6],name.split(".")[0]    ,"user2"),'w')
            string_to_write1= ["" for x in range(15)]
            consensus_to_write1= [ False for x in range(15)]
            last_received1=[rospy.rostime.Time(0) for x in range(15)]
            string_to_write2= ["" for x in range(15)]
            consensus_to_write2= [ False for x in range(15)]
            last_received2=[rospy.rostime.Time(0) for x in range(15)]
            for topic, msg, t in rosbag.Bag(rosbagurl).read_messages():


                
                if topic ==  "camera/rgb/image_color":
#                            print "writing in   "+"%s/%s/%s/%s_color/%05d_%s.png" % (outputpath,rosbagurl.split("/")[6],rosbagurl.split("/")[5],name.split(".")[0],colorindex,"color")
#                    cv2.imwrite("%s/%s/%s/%s_color/%05d_%s.png" % (outputpath,rosbagurl.split("/")[6],rosbagurl.split("/")[5],name.split(".")[0]    ,colorindex,"color"), bridge.imgmsg_to_cv2(msg, "bgr8")) 
                    colorindex=colorindex+1
                elif topic == "camera/depth/image":
#                    cv2.imwrite("%s/%s/%s/%s_gray8/%05d_%s.png" % (outputpath,rosbagurl.split("/")[6],rosbagurl.split("/")[5],name.split(".")[0],depthindex,"depth8"), bridge.imgmsg_to_cv2(msg, "8UC1"))
#                    cv2.imwrite("%s/%s/%s/%s_gray16/%05d_%s.png" % (outputpath,rosbagurl.split("/")[6],rosbagurl.split("/")[5],name.split(".")[0],depthindex,"depth16"), bridge.imgmsg_to_cv2(msg, "16UC1"))
                    depthindex=depthindex+1
                elif topic=="tf":# & msg.frame_id=="openni_depth_frame":
                    for transform in msg.transforms:
#                        print transform.header.frame_id
                        if transform.header.frame_id=="openni_depth_frame":
                            if transform.child_frame_id.endswith("1")&(user1index<depthindex):
                                increment,string_to_write1,consensus_to_write1=handle_tf(transform,string_to_write1,consensus_to_write1,last_received1,t,f1)                                
                                user1index+=increment
                            if transform.child_frame_id.endswith("2")&(user2index<depthindex):
                                increment,string_to_write2,consensus_to_write2=handle_tf(transform,string_to_write2,consensus_to_write2,last_received2,t,f2)                                
                                user2index+=increment
            f1.close()
            f2.close()
                            
                            
                            
                            
                        
                        
                        
                        
                        
