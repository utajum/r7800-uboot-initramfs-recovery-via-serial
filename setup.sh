#!/bin/bash

# Setup script for R7800 Serial Firmware Upload
# This script prepares your system for the experimental serial upload procedure

echo "=== R7800 Serial Upload Setup ==="
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
else
    echo "✓ Python 3 is installed"
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found. Installing..."
    sudo apt-get install -y python3-pip
else
    echo "✓ pip3 is available"
fi

# Install pyserial
echo "Installing pyserial..."
pip3 install --break-system-packages -r requirements.txt

echo
echo "=== Setup Complete ==="
echo
echo "Next steps:"
echo "1. Ensure your firmware file 'openwrt-24.10.2-ipq806x-generic-netgear_r7800-initramfs-uImage' is in this directory"
echo "2. Connect your USB-to-TTL serial adapter"
echo "3. Check your serial port with: dmesg | grep tty"
echo "4. Edit SERIAL_PORT in upload_firmware.py if needed (default: /dev/ttyUSB0)"
echo "5. Connect to router serial console and get to U-Boot prompt '(IPQ) #'"
echo "6. Exit your terminal emulator and run: python3 upload_firmware_byte.py"
echo
echo "WARNING: This process will take ~10 hours and has a high risk of failure! If it fails do not restart run the script again!"