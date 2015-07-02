import argparse
import serial
import os
import random

def serial_loopback_test(serial_device_a, serial_device_b):
	print("Doing a loopback test between device '%s' and '%s'" % (serial_device_a, serial_device_b))
	baudrate = 921600

	# open source and sink
	ser_a = serial.Serial(serial_device_a, baudrate, timeout=1)
	ser_b = serial.Serial(serial_device_b, baudrate, timeout=1)

	loop_counter = 0

	while True:
		length = random.randrange(1, 1024)
		data = os.urandom(length)

		dir = random.choice((True, False))
		if dir:
			ser_a.write(data)
			ret = ser_b.read(length)
		else:
			ser_b.write(data)
			ret = ser_a.read(length)

		if len(ret) != length:
			print('Error in length at loop %d. Expected length: %d, got %d') % (loop_counter, length, len(ret))
			exit(1)

		if ret != data:
			print('Error in data at loop: %d' % (loop_counter))
			exit(1)

		if loop_counter % 100 == 0:
			print('Loop at %d' % (loop_counter))
		loop_counter += 1

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Loopback test of serial devices.')
	parser.add_argument('devices', nargs='+', help='Devices connected together, e.g. /dev/ttyUSB0 and /dev/ttyUSB1')
	args = parser.parse_args()
	if len(args.devices) != 2:
		print('Supply exactly two devices which are connected back to back.')
	else:
		serial_loopback_test(args.devices[0], args.devices[1])
