#!/usr/bin/python3
#もしくは　#!/usr/bin/env python など環境に合わせて

#from _typeshed import IdentityFunction
from re import I
import rospy
from sensor_msgs.msg import JointState

import socket
from contextlib import closing
import struct
import math

import signal


UDP_RESV_IP="192.168.xxx.xxx" #このPCのIPアドレス
UDP_RESV_PORT=22222 #受信ポート

UDP_SEND_IP="192.168.xxx.xxx" #送信先のIPアドレス
UDP_SEND_PORT=22224 #送信ポート

MSG_SIZE = 92
MSG_BUFF = MSG_SIZE * 2

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#UDP用のsocket設定
sock.bind((UDP_RESV_IP,UDP_RESV_PORT))

data2 = []
loop_count = 0
error_count = 0

global i


while not rospy.is_shutdown():
    with closing(sock):
        while True:
            loop_count += 1
            r_bin_data,addr = sock.recvfrom(1472)
            sock.sendto(r_bin_data,(UDP_SEND_IP,UDP_SEND_PORT))
            r_short_data=struct.unpack('92h',r_bin_data)
            
            # checksum culc
            checksum = 0
            for i in  range(MSG_SIZE-2):
                checksum += r_short_data[i]
            checksum = ~checksum & 0xffff
            
            if checksum == r_short_data[MSG_SIZE-1]:
                print("Reseived OK. ",loop_count )

                joint_pub = rospy.Publisher('joint_states', JointState, queue_size=10)
                rospy.init_node('joint_state_publisher_meridim')
                rate = rospy.Rate(500) # 500hz
                js_meridim = JointState()
                js_meridim.header.stamp = rospy.Time.now()
                js_meridim.name =     ['c_chest_yaw',                      'l_shoulder_pitch',                'l_shoulder_roll',                  'l_elbow_yaw',                      'l_elbow_pitch',                    'l_hipjoint_yaw',                   'l_hipjoint_roll',                  'l_hipjoint_pitch',                 'l_knee_pitch',                     'l_ankle_pitch',                    'l_ankle_roll',                     'c_head_yaw',                       'r_shoulder_pitch',                  'r_shoulder_roll',                   'r_elbow_yaw',                      'r_elbow_pitch',                     'r_hipjoint_yaw',                    'r_hipjoint_roll',                  'r_hipjoint_pitch',                 'r_knee_pitch',                      'r_ankle_pitch',                     'r_ankle_roll']
                js_meridim.position = [math.radians(r_short_data[21]/100), math.radians(r_short_data[23]/100), math.radians(r_short_data[25]/100), math.radians(r_short_data[27]/100), math.radians(r_short_data[29]/100), math.radians(r_short_data[31]/100), math.radians(r_short_data[33]/100), math.radians(r_short_data[35]/100), math.radians(r_short_data[37]/100), math.radians(r_short_data[39]/100), math.radians(r_short_data[41]/100), math.radians(r_short_data[51]/100), math.radians(r_short_data[53]/100), -math.radians(r_short_data[55]/100), -math.radians(r_short_data[57]/100), math.radians(r_short_data[59]/100), -math.radians(r_short_data[61]/100), -math.radians(r_short_data[63]/100), math.radians(r_short_data[65]/100), math.radians(r_short_data[67]/100),  math.radians(r_short_data[69]/100), -math.radians(r_short_data[71]/100)]
                js_meridim.velocity = []
                #js_meridim.velocity = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                js_meridim.effort = []        
                joint_pub.publish(js_meridim)
                rate.sleep() 

            else:
                print("DATA ERROR")
                error_count += 1
                print("COUNT:",loop_count," ERROR:",error_count," ErrorRatio:",error_count/loop_count)

            signal.signal(signal.SIGINT, signal.SIG_DFL)
        
    

#if __name__ == '__main__':
    #main()
    #try:
    #    joint_publisher_func()
    #except rospy.ROSInterruptException:
    #    pass


