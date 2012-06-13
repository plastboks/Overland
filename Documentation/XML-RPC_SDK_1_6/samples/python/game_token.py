import xmlrpclib
import binascii
import sys
import random
import time

def send_message(to, text, alerttone=0x01, icon=0x0A, alertpattern = 0x01):
	action = 0x01
	responseenabler = 0xff
	messageid = 0x0001
	repeat = 3
	totype = "endpoint"
	ledcontrol = 0x00
	colorcontrol = 0x02
	setupspec = 0x00
	alertvolume = 0xFF
	alerttimeout = 0x05
	displaytimeout = 10
	callback = ""

	retry = True
	while retry:
		server.endpoint_sms_advanced(session, action, responseenabler, messageid, repeat, totype, to, ledcontrol,
			                           icon, colorcontrol, setupspec, alerttone, alertpattern, alertvolume,
			                           alerttimeout, displaytimeout, text, callback)

		wait = True
		start = time.time()
		while wait and time.time() - start < 5:
			events = server.session_receive(session, 1)
			for event in events:
				if "from" in event and event["from"] == to:
					if event["type"] == "endpoint_release":
						print "Message release " + str(event["reason"])
						wait = False
						if event["reason"] == 0x00:
							retry = False
					else:
						print "Message unexpected event: " + str(event)


def configure_sensor(to, element, data):
	retry = True
	start1 = time.time()
	while retry and time.time() - start1 < 45:
		server.endpoint_hardware_extension(session, element, 0x01, 0x03, "endpoint", to, xmlrpclib.Binary(binascii.unhexlify(data)))
		wait = True
		start2 = time.time()
		while wait and time.time() - start2 < 15:
			events = server.session_receive(session, 1)
			for event in events:
				if "from" in event and event["from"] == to:
					if event["type"] == "endpoint_hardware_extension" and event["element"] == element and event["reason"] == 0x01:
						wait = False
						retry = False
					elif event["type"] == "endpoint_release":
						print "Sensor release " + str(event["reason"])
						wait = False
					else:
						print "Sensor unexpected event: " + str(event)

	return not retry


def task_alarm(to, timeout = 10):
	send_message(to, "Press the alarm button")

	start = time.time()
	while time.time() - start < timeout:
		events = server.session_receive(session, 1)
		for event in events:
			if "from" in event and event["from"] == to:
				if event["type"] == "endpoint_status" and event["status"] == 0x0C:
					return True
				else:
					print "Unexpected event: " + str(event)
	return False


def task_function(to, timeout = 10):
	send_message(to, "Activate MSF function 1234")

	start = time.time()
	while time.time() - start < timeout:
		events = server.session_receive(session, 1)
		for event in events:
			if "from" in event and event["from"] == to:
				if event["type"] == "endpoint_call_setup" and event["to"] == "1234":
					call = event["call"]
					server.endpoint_call_accept(session, call)
					server.endpoint_call_release(session, call, 0x00)
					return True
				else:
					print "Unexpected event: " + str(event)
	return False


def task_longpress(to, timeout = 10):
	send_message(to, "Long press keypad 9")

	start = time.time()
	while time.time() - start < timeout:
		events = server.session_receive(session, 1)
		for event in events:
			if "from" in event and event["from"] == to:
				if event["type"] == "endpoint_call_setup" and event["to"] == "9":
					call = event["call"]
					server.endpoint_call_accept(session, call)
					server.endpoint_call_release(session, call, 0x00)
					return True
				else:
					print "Unexpected event: " + str(event)
	return False


def task_run(to, timeout = 10):
	configure_sensor(user, 0x03, "000A")

	send_message(to, "Activate the running alarm")

	start = time.time()
	wait = True
	result = False
	while wait and time.time() - start < timeout:
		events = server.session_receive(session, 1)
		for event in events:
			if "from" in event and event["from"] == to:
				if event["type"] == "endpoint_hardware_extension" and event["element"] == 0x03 and event["reason"] == 0x10:
					wait = False
					result = True
				else:
					print "Unexpected event: " + str(event)

	configure_sensor(user, 0x03, "0000")

	return result


def task_notvertical(to, timeout = 10):
	configure_sensor(user, 0x04, "0005")

	send_message(to, "Activate the not vertical alarm")

	start = time.time()
	wait = True
	result = False
	while wait and time.time() - start < timeout:
		events = server.session_receive(session, 1)
		for event in events:
			if "from" in event and event["from"] == to:
				if event["type"] == "endpoint_hardware_extension" and event["element"] == 0x04 and event["reason"] == 0x10:
					wait = False
					result = True
				else:
					print "Unexpected event: " + str(event)

	configure_sensor(user, 0x04, "0000")

	return result


def task_nomove(to, timeout = 10):
	configure_sensor(user, 0x02, "0005")

	send_message(to, "Activate the no move alarm")

	start = time.time()
	wait = True
	result = False
	while wait and time.time() - start < timeout:
		events = server.session_receive(session, 1)
		for event in events:
			if "from" in event and event["from"] == to:
				if event["type"] == "endpoint_hardware_extension" and event["element"] == 0x02 and event["reason"] == 0x10:
					wait = False
					result = True
				else:
					print "Unexpected event: " + str(event)

	configure_sensor(user, 0x02, "0000")

	return result


def task_rip(to, timeout = 10):
	configure_sensor(user, 0x01, "0001")

	send_message(to, "Activate the tear off alarm")

	start = time.time()
	wait = True
	result = False
	while wait and time.time() - start < timeout:
		events = server.session_receive(session, 1)
		for event in events:
			if "from" in event and event["from"] == to:
				if event["type"] == "endpoint_hardware_extension" and event["element"] == 0x01 and event["reason"] == 0x10:
					wait = False
					result = True
				else:
					print "Unexpected event: " + str(event)

	configure_sensor(user, 0x01, "0000")

	return result

def task_menu(to, timeout = 10):
	call = server.endpoint_call_setup(session, to, "", "What color is an orange?", 0x81)
	start = time.time()
	result = False
	while call > 0 and time.time() - start < timeout:
		events = server.session_receive(session, 1)
		for event in events:
			if "call" in event and event["call"] == call:
				if event["type"] == "endpoint_call_accept":
					server.endpoint_call_menu(session, call, ("Green", "Orange", "Blue"))
				elif event["type"] == "endpoint_call_menu":
					if event["item"] == 2:
						result = True
					server.endpoint_call_release(session, call, 0)
					call = 0
				else:
					print "Unexpected event: " + str(event)
			else:
				print "Unexpected event: " + str(event)
	if call > 0:
		server.endpoint_call_release(session, call, 0)
	return result

tasks = [task_alarm, task_longpress, task_function, task_run, task_notvertical, task_nomove, task_rip, task_menu]


if len(sys.argv) >= 3:
	host = sys.argv[1]
	to = sys.argv[2:]
else:
	print "Usage: " + sys.argv[0] + " <host> <to...>"
	exit(1)

server = xmlrpclib.Server("http://" + host)
session = server.session_login("GW-DECT/admin", "ip6000")

noanswer = list()
for i in range(0, len(to)):
	print to[i]
	for sensor in range(1, 5):
		if not configure_sensor(to[i], sensor, "0000"):
			noanswer.append(i)
			break
for i in noanswer:
	del to[i]
print to

score = dict()
score["failed"] = 0
score["succes"] = 0
random.shuffle(to)
random.shuffle(tasks)
i = 0
while True:
	task = tasks[i % len(tasks)]
	user = to[i % len(to)]
	print "%s %s" % (task, user)
	if task(user, 10):
		score["succes"] += 1
		print "Succes"
		send_message(user, "Great !", 0x04, 0x80)
	else:
		score["failed"] += 1
		print "Failed"
		send_message(user, "Failed !", 0x00, 0x68, 0x04)
	time.sleep(5)
	i += 1
	print "Score: %d / %d (%d%%)" % (score["succes"], score["succes"] + score["failed"], score["succes"] * 100 / (score["succes"] + score["failed"]))

server.session_logout(session)

