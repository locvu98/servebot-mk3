#!/usr/bin/env python
'''
Created on November 20, 2010
'''
import threading
import serial
#from cStringIO import StringIO
#from io import BytesIO
from io import StringIO
import time
import rospy

def _OnLineReceived(line):
	#print(line)
	rospy.info("no mess")


class SerialDataGateway(object):
	'''
	Helper class for receiving lines from a serial port
	'''

	def __init__(self, port="/dev/ttyUSB0", baudrate=115200, lineHandler = _OnLineReceived):
		'''
		Initializes the receiver class. 
		port: The serial port to listen to.
		receivedLineHandler: The function to call when a line was received.
		'''
		self._Port = port
		self._Baudrate = baudrate
		self.ReceivedLineHandler = lineHandler
		self._KeepRunning = False

	def Start(self):
		self._Serial = serial.Serial(port = self._Port, baudrate = self._Baudrate, timeout = 1)

		self._KeepRunning = True
		#rospy.loginfo('before listen func')
		self._ReceiverThread = threading.Thread(target=self._Listen)
		#rospy.loginfo('after listen func')
		self._ReceiverThread.setDaemon(True)
		self._ReceiverThread.start()

	def Stop(self):
		rospy.loginfo("Stopping serial gateway")
		self._KeepRunning = False
		time.sleep(.1)
		self._Serial.close()

	def _Listen(self):
		rospy.loginfo("listening")
		stringIO = StringIO()
		#stringIO = BytesIO()
		while self._KeepRunning:
			data = self._Serial.read().decode("UTF-8")
			#rospy.loginfo(data)
			if data == '\r':
				pass
			if data == '\n':
                # Return bytes containing the entire contents of the buffer.
				#rospy.loginfo("before calling func")
				self.ReceivedLineHandler(stringIO.getvalue())
				#rospy.loginfo("after calling func")
				stringIO.close()
				stringIO = StringIO()
				#stringIO = BytesIO()
			else:
				#rospy.loginfo(data)
                # writing to a buffer
				stringIO.write(data)

	def Write(self, data):
		info = "Writing to serial port: %s" %data
		rospy.loginfo(info)
		self._Serial.write(data)

	if __name__ == '__main__':
		dataReceiver = SerialDataGateway("/dev/ttyUSB0",  115200)
		dataReceiver.Start()

		raw_input("Hit <Enter> to end.")
		dataReceiver.Stop()


