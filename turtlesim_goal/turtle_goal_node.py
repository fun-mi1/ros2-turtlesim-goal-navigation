import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


class TurtleGoalNode(Node):
    def __init__(self):
        self.pose = None
        self.target_x = 9.0
        self.target_y = 5.0
        self.k_linear = 1.0
        self.k_angular = 4.0

        super().__init__("turtle_goal_node")
        self.cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        """
        Twist: The type of message we are speaking, /turtle1/cmd_vel: The topic we are broadcasting on
        10: The queue size which is basically how many messages to buffer if the connection is slow.
        Its also the QoS depth, similar to best effort where it throws out the remaining when the buffer exceeds 10
        """

        """
        Normally we would use print() in python but in ROS2 we use loggers... 
        Why?
        Imagine we have 50 nodes and we want to print from all of them, the terminal window would be too crowded
        and .get_logger() is better because it labels the message, it shows [turtle_goal_node]: The message.
        So we'll know exactly what script is talking
        """

        self.pose_sub = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)

        self.get_logger().info("Turtle Goal Node has been started.")
        
        """
        Normally we would use print() in python but in ROS2 we use loggers... 
        Why?
        Imagine we have 50 nodes and we want to print from all of them, the terminal window would be too crowded
        and .get_logger() is better because it labels the message, it shows [turtle_goal_node]: The message.
        So we'll know exactly what script is talking
        """

        self.control_timer = self.create_timer(0.1, self.control_loop)

        """
        Okay so this is basically Controls in action
        So we want to continuously check how close the error is to zero 
        and how close the robot is to the goal so we need to always subscribe from the topic and compare 
        then run the controller function and we do this after a period of time
        10 times per second: we want to run the controller 10times per second, that's frequency
        ROS2 asks for period, the time interval between calls, T = 1/f, 1/10 = 0.1
        """
        
    
    def pose_callback(self, msg:Pose):
        self.pose = msg
        self. get_logger().info(f"The turtle is currently at x = {self.pose.x}, y = {self.pose.y}")

    
    def control_loop(self):
        if self.pose is None: 
            return  #Do nothing if we haven't recieved our first pose
        

        dist_x = self.target_x - self.pose.x 
        dist_y = self.target_y - self.pose.y
        distance = math.sqrt(dist_x**2 + dist_y**2)

        angle_to_goal = math.atan2(dist_y, dist_x)

        current_theta = self.pose.theta

        angle_error = angle_to_goal - current_theta 

        msg = Twist()

        if distance > 0.1:
            msg.linear.x = self.k_linear * distance
            msg.angular.z = self.k_angular * angle_error
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info("Goal Reached!! Stopping...")

        self.cmd_vel_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args) 
    node = TurtleGoalNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()


