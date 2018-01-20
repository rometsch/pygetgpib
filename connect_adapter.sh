#!/usr/bin/env bash
# Author: Thomas Rometsch (thomas.rometsch@gmail.com)
# Date: 2018-01-20
# This script connects a Agilent/Keysight 82357B Adapter

# First check whether the adapter is connected to the system

function flashFirmware {
# Define a pattern to find the adapter in the output of 'lsusb'
UsbIdentifierString="82357B"
LsusbStr="$(lsusb | grep $UsbIdentifierString)"

# Extract the Bus and Device number
Bus="$(echo $LsusbStr | awk '{print $2}')"
# use awk to remove the trailing : after the device number
Device="$(echo $LsusbStr | awk '{print substr( $4, 1, length($4)-1 )}')"
UsbDevPath="/dev/bus/usb/$Bus/$Device"

# Flash the firmware to the device
fxload -D $UsbDevPath -t fx2 -I gpib/gpib_firmware-2008-08-10/agilent_82357a/measat_releaseX1.8.hex

# Sleep 3 seconds to give the system time. 3 sec determined by testing
sleep 3
}

# Try to flash the firmware twice. This is neededd for some reason
# Pause inbetween
flashFirmware
flashFirmware

# change device permission
chmod 666 /dev/gpib0

# make sure the gpib lib is in /lib
ln -sf /usr/local/lib/libgpib.so.0 /lib

# configure gpib
gpib_config
