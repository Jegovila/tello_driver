#!/usr/bin/env python3
import roslib
import rospy
import sys, select, termios, tty

from geometry_msgs.msg import Twist, PoseStamped
from std_msgs.msg import Empty

x=0
y=0
z=0
x_d = 0
y_d = 0
z_d = 0

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
	
def callback_ref(msg):
	global x_d,y_d,z_d
	x_d=msg.pose.position.x
	y_d=msg.pose.position.y
	z_d=msg.pose.position.z
	#rospy.loginfo('x_d: {}, y_d:{}, z_d:{},' .format(x_d,y_d,z_d))

speed = 0.2 # m/s

if __name__=="__main__":
	settings = termios.tcgetattr(sys.stdin)
	is_flying = False
	count_takeoff = 0
	# init nodo
	rospy.init_node('tello_move')
	
	# init topic for reference
	p_d = rospy.Publisher('/pos_d', PoseStamped, queue_size = 1)
	p_d.publish(PoseStamped())

	# publicar 
	p = rospy.Publisher('/tello/cmd_vel', Twist, queue_size = 1)
	pub_takeoff = rospy.Publisher('/tello/takeoff', Empty, queue_size = 1)
	pub_land = rospy.Publisher('/tello/land', Empty, queue_size = 1)
	rospy.Subscriber("/orb_slam3/camera_pose", PoseStamped, callback)
	rospy.Subscriber("/pos_d", PoseStamped, callback_ref)
	
	rospy.sleep(5)

	# mensaje
	twist = Twist()
	empty_msg = Empty()

	# anunciar y mover
	# Takeoff
	
	while True:
		rospy.loginfo("Esperando instrucción: t:takeoff   q:salir")
		key_takeoff = getKey(2)
		if key_takeoff == 't':
			rospy.loginfo("Takeoff")
			pub_takeoff.publish(empty_msg)
			rospy.sleep(4)
			is_flying = True
			termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
			break
		elif key_takeoff == 'q':
			termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
			break
		elif count_takeoff > 5:
			rospy.loginfo("No hubo respuesta")
			termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
			break			
		else:
			count_takeoff += 1
			pass


	if is_flying:
		rospy.loginfo('Inicia control, aterrizar con l')
		while True:
			twist.linear.x = x_d - z * speed * 10
			twist.linear.y = y_d + x * speed * 10
			twist.linear.z = z_d + y * speed * 10
			p.publish(twist)
			#rospy.loginfo(z_d + y * speed * 10)
			key = getKey(.1)
			if key == 'l':
				twist = Twist() # default 0 (detenerse)
				p.publish(twist)
				rospy.sleep(2)
				rospy.loginfo("Landing")
				pub_land.publish(empty_msg)
				rospy.sleep(2)
				is_flying = False
				termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
				break
			else:
				pass
		

	
	rospy.loginfo("Saliendo")

