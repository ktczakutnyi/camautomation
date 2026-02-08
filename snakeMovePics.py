import serial
import time
import os
from picamera2 import Picamera2

# --- CONFIGURATION ---
PORT = '/dev/ttyUSB0'
STEP_MM = 12.7         # 0.5 inches
START_Z = 127.0        # 5 inches
GRID_SIZE = 10
OFFSET_X = 50.8        # 2 inches offset
OFFSET_Y = 50.8        # 2 inches offset

# Create folder for images
folder_name = f"scan_{int(time.time())}"
os.makedirs(folder_name)

# --- 1. CONNECT TO ENDER 3 FIRST ---
try:
    printer = serial.Serial(PORT, 115200, timeout=1)
    time.sleep(2)
    print("Connected to Ender 3")
except:
    print("Printer connection failed.")
    exit()

def send_command(cmd):
    printer.write(f"{cmd}\n".encode())
    while True:
        line = printer.readline().decode().strip()
        if line == "ok":
            break

# --- 2. PRE-SCAN MECHANICAL SETUP ---
print("Homing printer...")
send_command("G28")                      # Home X, Y, and Z
time.sleep(3)                            # Wait for homing to fully complete

print("Lifting to 5 inches...")
send_command(f"G1 Z{START_Z} F1500")     # Move to 5 inches high
time.sleep(2)                            # Wait for Z movement to complete

print("Moving to start position...")
send_command(f"G1 X{OFFSET_X} Y{OFFSET_Y} F3000")  # Move to offset start position
time.sleep(2)                            # Wait for XY movement to complete

# --- 3. NOW initialize camera (after ALL movement confirmed stopped) ---
print("All mechanical movement complete. Initializing camera...")
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()
print("Camera ready (fixed focus).")
time.sleep(2)  # Let camera stabilize

# --- 4. THE 10x10 GRID SCAN ---
print(f"Starting 100-point scan. Saving to: {folder_name}")
for row in range(GRID_SIZE):
    y_pos = OFFSET_Y + (row * STEP_MM)
    
    columns = range(GRID_SIZE) if row % 2 == 0 else reversed(range(GRID_SIZE))
    
    for col in columns:
        x_pos = OFFSET_X + (col * STEP_MM)
        
        print(f"Moving to Row:{row} Col:{col} (X:{x_pos}mm, Y:{y_pos}mm)")
        send_command(f"G1 X{x_pos} Y{y_pos} F3000")
        
        time.sleep(1.5)  # Vibration settling
        
        file_path = f"{folder_name}/x{col}_y{row}.jpg"
        picam2.capture_file(file_path)
        print(f"Captured {file_path}")

# --- 5. SHUTDOWN ---
print("Scan Complete! Retreating to start position...")
picam2.stop()
send_command(f"G1 X{OFFSET_X} Y{OFFSET_Y} Z{START_Z} F3000")
