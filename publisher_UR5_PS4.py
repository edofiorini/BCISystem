#!/usr/bin/env python


import select
import sys
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Vector3


# This python script reads from joy node some input command
# and with ROS node sends a Vector3 to the simulator


#Structure of command
drive = {
    'right': 0,
    'left': 0,
    'forward': 0,
    'backward': 0,
    'open': 0,
    'close': 0,
    'up': 0,
    'down': 0
}


#Function that sends the message to the simulator step by step with the possibility to stop it
def send(msg_pos,pub):
    count = 0

    while count < 10:
        rospy.loginfo(msg_pos)
        pub.publish(msg_pos)
        rospy.sleep(0.1)

        i,o,e = select.select([sys.stdin],[],[],0.0001)
        if i == [sys.stdin]:
            print("CAUTION!")
            break
        '''
        if sys.stdin.isatty():
             print "not sys.stdin.isatty"
        '''
        count += 1




#Function that controls the input from the structure of command and fills the buffer
def control(msg_pos):
    if drive['right'] == 1:
        msg_pos.x = +0.05
    elif drive['left'] == 1:
        msg_pos.x = -0.05
    elif drive['forward'] == 1:
        msg_pos.y = +0.05
    elif drive['backward'] == 1:
        msg_pos.y = -0.05
    elif drive['close'] == 1:
        msg_pos.x = 10
    elif drive['open'] == 1:
        msg_pos.x = 20
    elif drive['up']== 1:
        msg_pos.z = 0.05
    elif drive['down'] == 1:
        msg_pos.z = -0.05

#Function that talks with the simulator
def talker():
    #Buffer initialization composed of x,y,z
    msg_pos = Vector3()
    #ROS node and publisher initialization
    pub = rospy.Publisher('sim_ros_interface/chatter', Vector3, queue_size=10)

    control(msg_pos)
    send(msg_pos,pub)


#Function that listens from the joy_node and create the ROS node
def listener():
    print("Welcome to the ROS node!")
    rospy.sleep(0.5)
    rospy.init_node('listener', anonymous=True)
    #ROS publisher initialization
    sub = rospy.Subscriber('joy', Joy, callback, queue_size=1)
    rospy.spin()


#Callback function calls by the subscriber. It fills the structure of command
def callback(data):
    rospy.loginfo(data.buttons)
    drive['right'] = data.buttons[0]            #cross button
    drive['left'] = data.buttons[1]             #circle button
    drive['forward'] = data.buttons[2]          #triangle button
    drive['backward'] = data.buttons[3]         #rectangle button
    drive['open'] = data.buttons[8]             #share button
    drive['close'] = data.buttons[9]            #option button
    drive['up'] = data.axes[7]                  #arrow up
    drive['down'] = data.axes[6]                #arrow left
    talker()



if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
