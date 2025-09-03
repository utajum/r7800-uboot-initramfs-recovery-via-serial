import serial
import sys
import time
import os

# --- Configuration ---
FIRMWARE_FILE = 'openwrt-24.10.2-ipq806x-generic-netgear_r7800-initramfs-uImage'
#'openwrt-19.07.9-ipq806x-generic-netgear_r7800-initramfs-uImage'
SERIAL_PORT = '/dev/ttyUSB0' 
BAUD_RATE = 115200
LOAD_ADDRESS = 0x44000000
# Delay between commands (seconds)
COMMAND_DELAY = 0.005 
# --- End Configuration ---

def main():
    """Byte-by-byte upload using mm.b instead of mw.l"""
    if not os.path.exists(FIRMWARE_FILE):
        print(f"Error: Firmware file not found: {FIRMWARE_FILE}")
        sys.exit(1)

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1.0)
    except serial.SerialException as e:
        print(f"Error: Could not open serial port {SERIAL_PORT}: {e}")
        sys.exit(1)

    print("--- Byte-by-Byte Serial Upload Script ---")
    print(f"Port: {SERIAL_PORT}, Baudrate: {BAUD_RATE}")
    print(f"File: {FIRMWARE_FILE}")
    print("This version uses mw.b (memory write byte) instead of mw.l (memory write long).")
    print("It writes one byte at a time, which may be more reliable.")

    with open(FIRMWARE_FILE, 'rb') as f:
        firmware_data = f.read()

    file_size = len(firmware_data)
    
    print(f"Firmware size: {file_size} bytes")
    print(f"Load address: 0x{LOAD_ADDRESS:08x}")
    print(f"End address: 0x{LOAD_ADDRESS + file_size:08x}")
    print(f"Command delay: {COMMAND_DELAY}s")
    
    # Estimate time
    estimated_time = file_size * COMMAND_DELAY
    hours = int(estimated_time // 3600)
    minutes = int((estimated_time % 3600) // 60)
    seconds = int(estimated_time % 60)
    print(f"Estimated time: {hours}h {minutes}m {seconds}s")
    
    print(f"\nWARNING: This will send {file_size} individual byte commands!")
    input("Press Enter to start byte upload...")

    start_time = time.time()
    last_update = start_time

    for i, byte_val in enumerate(firmware_data):
        address = LOAD_ADDRESS + i
        
        # Create mw.b command for single byte
        # mw.b address value - write memory byte
        command = f"mw.b 0x{address:08x} 0x{byte_val:02x}\n".encode('ascii')

        # Send command
        ser.write(command)
        
        # Progress indicator (update every 10000 bytes or every 10 seconds)
        current_time = time.time()
        if i % 10000 == 0 or (current_time - last_update) >= 10 or i == file_size - 1:
            progress = (i + 1) / file_size * 100
            elapsed = current_time - start_time
            
            if i > 0:
                rate = i / elapsed
                eta = (file_size - i) / rate
                eta_hours = int(eta // 3600)
                eta_minutes = int((eta % 3600) // 60)
                eta_seconds = int(eta % 60)
                eta_str = f"{eta_hours:02d}:{eta_minutes:02d}:{eta_seconds:02d}"
            else:
                eta_str = "calculating..."
            
            elapsed_hours = int(elapsed // 3600)
            elapsed_minutes = int((elapsed % 3600) // 60)
            elapsed_secs = int(elapsed % 60)
            elapsed_str = f"{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_secs:02d}"
            
            sys.stdout.write(f"\r[{i+1:>7}/{file_size}] {progress:6.2f}% | Elapsed: {elapsed_str} | ETA: {eta_str} | Addr: 0x{address:08x} | Byte: 0x{byte_val:02x}")
            sys.stdout.flush()
            last_update = current_time

        # Fixed delay between commands
        time.sleep(COMMAND_DELAY)

    end_time = time.time()
    duration = end_time - start_time
    duration_hours = int(duration // 3600)
    duration_minutes = int((duration % 3600) // 60)
    duration_seconds = int(duration % 60)
    
    print(f"\n\n--- BYTE UPLOAD COMPLETE ---")
    print(f"All {file_size} bytes sent in {duration_hours:02d}:{duration_minutes:02d}:{duration_seconds:02d}")
    print(f"Average rate: {file_size/duration:.1f} bytes/second")
    print("\nAll byte commands have been sent to the router.")
    print("Connect to serial console and try: bootm 0x44000000")

    ser.close()

if __name__ == '__main__':
    main()