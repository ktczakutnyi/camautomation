import serial
import time
import os
from picamera2 import Picamera2

# --- CONFIGURATION ---
PORT = '/dev/ttyUSB0'  # Ender 3 USB Port
STEP_MM = 12.7         # 0.5 inches
START_Z = 127.0        # 5 inches
GRID_SIZE = 10 

# --- 1. INITIALIZE CAMERA ---
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

# Create folder for images
folder_name = f"scan_{int(time.time())}"
os.makedirs(folder_name)

# --- 2. CONNECT TO ENDER 3 ---
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

# --- 3. PRE-SCAN SETUP ---
print("Homing printer and lifting to 5 inches...")
send_command("G28")                      # Home X, Y, and Z
send_command(f"G1 Z{START_Z} F1500")     # Move to 5 inches high
send_command("G1 X0 Y0 F3000")           # Ensure we are at the start

# --- 4. FOCUS LOCK ---
# IMX219 has a fixed-focus lens - no autofocus needed
print("Camera ready (fixed focus).")
# Let camera stabilize exposure/white balance
time.sleep(2)


# --- 5. THE 10x10 GRID SCAN ---
print(f"Starting 100-point scan. Saving to: {folder_name}")

for row in range(GRID_SIZE):
    y_pos = row * STEP_MM

    # Logic for "Snake" pattern (zigzag)
    # Even rows go 0 -> 9, Odd rows go 9 -> 0
    columns = range(GRID_SIZE) if row % 2 == 0 else reversed(range(GRID_SIZE))
    
    for col in columns:
        x_pos = col * STEP_MM

        # 1. TELL PRINTER TO MOVE
        print(f"Moving to Row:{row} Col:{col} (X:{x_pos}mm, Y:{y_pos}mm)")
        send_command(f"G1 X{x_pos} Y{y_pos} F3000")

        # 2. THE PAUSE (Crucial for clear photos)
        # The script stops here and waits 1.5 seconds 
        # for the gantry to stop shaking.
        # Vibration settling time - crucial for long cables
        time.sleep(1.5) 
        
        # 3. Capture Image
        file_path = f"{folder_name}/x{col}_y{row}.jpg"
        picam2.capture_file(file_path)
        print(f"Captured point {col} in row {row} file: {file_path}")
       

# --- 6. SHUTDOWN ---
print("Scan Complete! Retreating to start position...")
picam2.stop()

# Move to X0 Y0 while STAYING at the 5-inch (START_Z) height
# We use F3000 to move quickly
send_command(f"G1 X0 Y0 Z{START_Z} F3000")
