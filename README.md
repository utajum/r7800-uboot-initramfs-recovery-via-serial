# Netgear R7800 Serial Firmware Upload (Experimental)

This repository contains an experimental method for uploading OpenWrt firmware to a Netgear R7800 router via serial connection. This procedure is intended as a last-resort recovery method when other methods (LAN/TFTP, USB) have failed.

**WARNING: This procedure is highly experimental and extremely slow. While challenging, this process does work.**

## Firmware Image Details

*   `openwrt-24.10.2-ipq806x-generic-netgear_r7800-initramfs-uImage`: This is the OpenWrt initramfs firmware image specifically targeted for the Netgear R7800. This image is loaded into the router's RAM and runs a temporary operating system. Both this version and `openwrt-19.07.9-ipq806x-generic-netgear_r7800-initramfs-uImage` have been tested and confirmed to work with this upload method. However, the 19.x version exhibited non-functional Wi-Fi (due to existing broken LAN ports on the test router I could not get a network connection), while the 24.x version functioned correctly.

## Script Details

*   `upload_firmware_byte.py`: This Python script facilitates the byte-by-byte upload of the firmware image to the router's memory via a serial connection. It uses `mw.b` (memory write byte) U-Boot commands, sending one byte at a time.

### `upload_firmware_byte.py` Configuration

The script has configurable parameters at the top:

```python
# --- Configuration ---
FIRMWARE_FILE = 'openwrt-24.10.2-ipq806x-generic-netgear_r7800-initramfs-uImage'
SERIAL_PORT = '/dev/ttyUSB0' 
BAUD_RATE = 115200
LOAD_ADDRESS = 0x44000000
# Delay between commands (seconds)
COMMAND_DELAY = 0.005
# --- End Configuration ---
```

The `COMMAND_DELAY` parameter introduces a small pause between sending each byte command. Increasing this value can potentially improve transfer reliability, especially in environments with unstable serial connections. The current default of `0.005` seconds has been tested multiple times and rarely resulted in corrupted bytes, indicating a reasonable balance between speed and reliability.


### Estimated Transfer Time

The `upload_firmware_byte.py` script will estimate the transfer time based on the firmware size and the `COMMAND_DELAY`. For the `openwrt-24.10.2-ipq806x-generic-netgear_r7800-initramfs-uImage` file, which is approximately 7.2MB, and a `COMMAND_DELAY` of 0.005 seconds, the estimated time will be very long (around 10 hours).

## Procedure Overview

1.  **Hardware Setup**: Connect your computer to the R7800 router using a reliable USB-to-TTL 3.3V serial adapter.
2.  **Software Requirements**: Ensure Python 3 and the `pyserial` library are installed (`pip3 install pyserial`). A helper script, `setup.sh`, is provided to automate this installation, but it is not mandatory.
3.  **Prepare Router**: Power on the router and interrupt the boot process (by pressing the reset button during boot) to reach the U-Boot prompt `(IPQ) #` via a serial terminal emulator (e.g., `minicom`, `screen`). **Exit the terminal emulator before running the Python script.**
4.  **Configure Script**: Edit `upload_firmware_byte.py` to set the correct `SERIAL_PORT`.
5.  **Run Script**: Execute the `upload_firmware_byte.py` script from your terminal: `python3 upload_firmware_byte.py`.
6.  **WAIT**: The script will begin the byte-by-byte transfer. This process will take a very long time. Do not interrupt the connection or let your computer go to sleep.
7.  **Boot Image (if successful)**: If the script completes without errors, reconnect to the router's serial console and issue the U-Boot command `bootm 0x44000000` to attempt booting the uploaded image.

## Risks and Expectations

*   **Extreme Slowness**: The byte-by-byte transfer is inherently slow, potentially taking many hours.
*   **Data Integrity Considerations**: Any interruption or electrical noise can lead to data inconsistencies. However, the process can be repeated from the U-Boot prompt **without restarting the router**, as the memory addresses will be overwritten correctly in subsequent passes if a byte was missed or corrupted. The script does not verify data integrity.
*   **Environmental Sensitivity**: Power flickers, loose cables, or the computer going to sleep can disrupt the transfer. Maintaining a stable environment is crucial.
*   **Achievable with Persistence**: Due to the nature of serial communication for large files, success requires patience and a stable setup. If the `bootm` command fails or results in unexpected output, it indicates a data issue, and another pass of the upload process is recommended.

If successful, the router will boot a temporary OpenWrt instance from RAM. You would then need to flash a permanent `sysupgrade` image.

## Additional Resources

*   **OpenWrt R7800 Device Page**: For more detailed information and official documentation regarding the Netgear R7800 and OpenWrt, please refer to the [OpenWrt R7800 Wiki](https://openwrt.org/toh/netgear/r7800).