#!/usr/bin/env python3
import roslib
import rospy
import sys, select, termios, tty

from geometry_msgs.msg import Twist, PoseStamped
from std_msgs.msg import Empty


def getKey(key_timeout):
	tty.setraw(sys.stdin.fileno())
	rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
	if rlist:
		key = sys.stdin.read(1)
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	else:
		key = ''
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key
	
def land():
	key = getKey(.1)
	if key == 'l':
		twist = Twist() # default 0 (detenerse)
		p.publish(twist)
		rospy.sleep(2)
		rospy.loginfo("Landing")
		pub_land.publish(empty_msg)
		rospy.sleep(2)
		landing = True
	else:	
		landing = False
	return landing
	

speed = 0.2 # m/s

if __name__=="__main__":
	settings = termios.tcgetattr(sys.stdin)
	is_flying = False
	landing = False
	count_takeoff = 0
	# init nodo
	rospy.init_node('tello_move')
	
	# publicar 
	p = rospy.Publisher('/tello/cmd_vel', Twist, queue_size = 1)
	pub_takeoff = rospy.Publisher('/tello/takeoff', Empty, queue_size = 1)
	pub_land = rospy.Publisher('/tello/land', Empty, queue_size = 1)
	
	rospy.sleep(5)

	# mensaje
	twist = Twist()
	empty_msg = Empty()
	

	for i in range(20):
		rospy.loginfo("Esperando instrucción: t:takeoff   q:salir")
		key_takeoff = getKey(2)
		if key_takeoff == 't':
			rospy.loginfo("Takeoff")
			pub_takeoff.publish(empty_msg)
			rospy.sleep(4)
			is_flying = True
			break
		elif key_takeoff == 'q':
			break

	if is_flying:
		rospy.loginfo('Inicia movimiento, aterrizar con l')
		while not landing:
		
			twist = Twist()
			twist.angular.x = -speed
			for i in range (10):
				p.publish(twist)
				rospy.sleep(.1)
				landing = land()
				if landing: 
					break
			
			twist = Twist()
			twist.angular.z = -speed
			for i in range (55):
				p.publish(twist)
				rospy.sleep(.1)
				landing = land()
				if landing: 
					break
	
	rospy.loginfo("Saliendo")

