#!/usr/bin/env python

import rospy

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

rospy.init_node('movebase_client_py')
client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
client.wait_for_server()
goal = MoveBaseGoal()
goal.target_pose.header.frame_id = "map"
goal.target_pose.header.stamp = rospy.Time.now()
goal.target_pose.pose.position.x = 1
goal.target_pose.pose.position.y = 1
goal.target_pose.pose.orientation.z = -0.028
goal.target_pose.pose.orientation.w = 0.999
client.send_goal(goal)
wait = client.wait_for_result()
