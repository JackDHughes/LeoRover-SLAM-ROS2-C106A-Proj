import sys
import threading
import time

import geometry_msgs.msg
import rclpy

def main():
    driveCommands = open("commands.txt", "r")

    rclpy.init()

    node = rclpy.create_node('programmed_drive_node')

    # parameters
    stamped = node.declare_parameter('stamped', False).value
    frame_id = node.declare_parameter('frame_id', '').value
    if not stamped and frame_id:
        raise Exception("'frame_id' can only be set when 'stamped' is True")

    if stamped:
        TwistMsg = geometry_msgs.msg.TwistStamped
    else:
        TwistMsg = geometry_msgs.msg.Twist

    pub = node.create_publisher(TwistMsg, 'cmd_vel', 10)

    spinner = threading.Thread(target=rclpy.spin, args=(node,))
    spinner.start()

    twist_msg = TwistMsg()

    if stamped:
        twist = twist_msg.twist
        twist_msg.header.stamp = node.get_clock().now().to_msg()
        twist_msg.header.frame_id = frame_id
    else:
        twist = twist_msg

    try:
        for line in driveCommands:
            commands = line.split(",")

            twist.linear.x = float(commands[0])
            twist.angular.z = float(commands[1])

            print("Throttle:" + commands[0] + ", Turn:" + commands[1] + ", Duration:" + commands[2])

            if stamped:
                twist_msg.header.stamp = node.get_clock().now().to_msg()

            twist.linear.y = 0.0 #experimentally does not do anything
            twist.linear.z = 0.0 #also experimentally does not do anything
            twist.angular.x = 0.0 #does not do anything
            twist.angular.y = 1.0

            t_end = time.time() + float(commands[2])
            while time.time() < t_end:
                if int(time.time() * 10) % 3 == 0:
                    pub.publish(twist_msg)

    except Exception as e:
        print(e)

    finally:
        if stamped:
            twist_msg.header.stamp = node.get_clock().now().to_msg()

        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        pub.publish(twist_msg)
        rclpy.shutdown()
        spinner.join()


if __name__ == '__main__':
    main()