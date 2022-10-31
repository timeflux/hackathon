#/bin/bash

DONGLE_ADDRESS="00:1A:7D:DA:71:13"   # Change this
BITALINO_ADDRESS="20:18:06:13:02:44" # Change this

DONGLE_DEVICE=$(hciconfig | grep -B 1 $DONGLE_ADDRESS | head -n 1 | awk -F':' '{print $1}')
BLUETOOTH_DEVICES=$(hciconfig | grep ^hci | awk -F: '{print $1}')

bluetooth_init() {
	for DEVICE in $BLUETOOTH_DEVICES
	do
		if [ "$DEVICE" != "$DONGLE_DEVICE" ]
		then
			sudo hciconfig $DEVICE down
		fi
	done
}

echo "Setting up Bluetooth"
bluetooth_init

echo "Binding Bitalino to virtual port"
sudo rfcomm bind 0 $BITALINO_ADDRESS
sudo chown $USER /dev/rfcomm0

# Unbind
# sudo rfcomm release 0