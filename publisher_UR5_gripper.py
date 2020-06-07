#!/usr/bin/env python


import select
import sys
import rospy
from geometry_msgs.msg import Vector3


# This python script reads from file some input command
# and with ROS node sends a Vector3 to the simulator

#Function that sends the message to the simulator
def send(msg_pos,pub):
    rospy.sleep(1)
    if msg_pos.x == 10 or msg_pos.x == 20:
        rospy.loginfo(msg_pos)
        pub.publish(msg_pos)
    else:
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


#Function that cleans the buffer msg_pos
def setUp(msg_pos):
    msg_pos.x = 0
    msg_pos.y = 0
    msg_pos.z = 0


#Function that controls the input command and fills the buffer
def control(line,msg_pos):
    if line == 'right':
        msg_pos.x = +0.05
    elif line == 'left':
        msg_pos.x = -0.05
    elif line == 'forward':
        msg_pos.y = +0.05
    elif line == 'backward':
        msg_pos.y = -0.05
    elif line == 'up':
        msg_pos.z = 0.05
    elif line == 'down':
        msg_pos.z = -0.05
    elif line == 'open':
        msg_pos.x = 20
    elif line == 'close':
        msg_pos.x = 10


def talker():
    print("Welcome to the ROS node!")
    #Path of the file
    filename = sys.argv[-1]

    #Buffer initialization composed of x,y,z
    msg_pos = Vector3()

    #ROS node and publisher initialization
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('sim_ros_interface/chatter', Vector3, queue_size=10)

    f = open(filename, "r")
    line = (f.readline())

    #Read the file
    while line:
        line = line.strip()
        control(line,msg_pos)
        send(msg_pos,pub)
        rospy.sleep(2)
        setUp(msg_pos)
        line = f.readline()
    f.close()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
