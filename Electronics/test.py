from lidar_lite import Lidar_Lite
import time
lidar = Lidar_Lite()
connected = lidar.connect(1)

if connected < -1:
	print("Not Connected")

else:
	print("Connected")

while True:
    distance = lidar.getDistance()
    velocity = lidar.getVelocity()
    print("Distance = %s" % (distance))
    print("Velocity = %s" % (velocity))
    time.sleep(0.200)
	#if int(distance) < 50:
	#   print("Too Close!!! Back Off!!!")
