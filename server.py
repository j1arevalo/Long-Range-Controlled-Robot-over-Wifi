PROTOCOL_VERSION = '2'

import evdev
import json

version = input()
if version != PROTOCOL_VERSION:
	raise Exception('Invalid protocol version. Got {}, expected {}.'.format(version, PROTOCOL_VERSION))

devices_json = json.loads(input())
devices = []
for device_json in devices_json:
	capabilities = {}
	for k, v in device_json['capabilities'].items():
		capabilities[int(k)] = [x if not isinstance(x, list) else (x[0], evdev.AbsInfo(**x[1])) for x in v]
	devices.append(evdev.UInput(capabilities, name=device_json['name'] + ' (via input-over-ssh)', vendor=device_json['vendor'], product=device_json['product']))

print('Device created')

while True:
	event = json.loads(input())
	#print(event)
	devices[event[0]].write(event[1], event[2], event[3])
