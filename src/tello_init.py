#!/usr/bin/env python3
import roslib
import rospy
import sys, select, termios, tty

from geometry_msgs.msg import Twist, PoseStamped
from std_msgs.msg import Empty

x=0
y=0
z=0

def getKey(key_timeout):
	tty.setraw(sys.stdin.fileno())
	rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
	if rlist:
		key = sys.stdin.read(1)
	else:
		key = ''
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key
    
def callback(msg):
	global x,y,z
	x=msg.pose.position.x
	y=msg.pose.position.y
	z=msg.pose.position.z
	#rospy.loginfo('x: {}, y:{}, z:{},' .format(x,y,z))

speed = 0.2 # m/s

if __name__=="__main__":
	settings = termios.tcgetattr(sys.stdin)
	# init nodo
	rospy.init_node('tello_move')

	# publicar 
	p = rospy.Publisher('/tello/cmd_vel', Twist, queue_size = 1)
	pub_takeoff = rospy.Publisher('/tello/takeoff', Empty, queue_size = 1)
	pub_palmLand = rospy.Publisher('/tello/land', Empty, queue_size = 1)
	rospy.Subscriber("/orb_slam3/camera_pose", PoseStamped, callback)
	
	rospy.sleep(5)

	# mensaje
	twist = Twist()
	empty_msg = Empty()

	# anunciar y mover
	# Takeoff
	rospy.loginfo("Takeoff")
	#pub_takeoff.publish(empty_msg)
	rospy.sleep(4)
	'''
	
	# Movimiento
	rospy.loginfo("Movimiento en Y")
	twist = Twist()
	twist.linear.y = speed 
	p.publish(twist)
	rospy.sleep(4)
		
	rospy.loginfo("Movimiento en Z")
	twist = Twist()
	twist.linear.z = speed 
	p.publish(twist)
	rospy.sleep(4)
		
	rospy.loginfo("Movimiento en X")
	twist = Twist()
	twist.linear.x = speed 
	p.publish(twist)
	rospy.sleep(4)
		
	rospy.loginfo("Regreso a home")
	twist = Twist()
	twist.linear.x = -speed
	twist.linear.y = -speed 
	twist.linear.z = -speed  
	p.publish(twist)
	rospy.sleep(4)
	
		 
	# nuevo mensaje
	rospy.loginfo("Stop")
	twist = Twist() # default 0 (detenerse)
	p.publish(twist)
		
	'''
	
	rospy.loginfo('Inicia control, aterrizar con l')
	while True:
		twist.linear.x = -z * speed * 10
		twist.linear.y = x * speed * 10
		twist.linear.z = y * speed * 10
		p.publish(twist)
		#rospy.loginfo('controlando')
		key = getKey(.1)
		if key == 'l':
			termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
			break
		else:
			pass
		
	twist = Twist() # default 0 (detenerse)
	p.publish(twist)
	rospy.sleep(2)
	rospy.loginfo("Landing")
	pub_palmLand.publish(empty_msg)
	rospy.sleep(2)

