This **README** is designed for your project repository. It covers the hardware setup, the software logic, and the specific quirks of using an Ender 3 Pro and a Pi Camera V3 NoIR for automated grid scanning.

---

# 🛰️ EnderScan-XY: Automated Grid Imaging System

A high-precision, 2D gantry-based imaging system built from a repurposed **Ender 3 Pro** and a **Raspberry Pi Camera Module V3 Wide NoIR**. This system automates the process of moving a camera to specific coordinates, pausing for stability, and capturing high-resolution images across a 10x10 grid.

## 🛠 Hardware Configuration

* **Motion Controller:** Ender 3 Pro Motherboard (retaining original NEMA 17 steppers).
* **Imaging:** Raspberry Pi Camera Module V3 (Wide Angle, NoIR version).
* **Connection:** USB (Serial) from Raspberry Pi to Ender 3.
* **Cable Management:** Extended CSI lens cable with dedicated strain relief.

## 📐 Scan Specifications

* **Z-Height:** 5.0 inches (127mm) fixed altitude.
* **Grid Density:** 10 x 10 (100 total capture points).
* **Step Increment:** 0.5 inches (12.7mm) between stops.
* **Pattern:** "Snake" (Zig-Zag) to minimize mechanical wear and cable tension.

## 🚀 Installation & Setup

### 1. Raspberry Pi Preparation

Ensure you are using a modern OS (Bullseye or later) to support the `Picamera2` library.

```bash
pip install pyserial
sudo apt install libcamera-apps

```

### 2. Physical Setup

1. Mount the **Pi Camera V3** to the Ender 3 X-axis carriage (where the hotend was previously located).
2. Connect the Ender 3 to the Raspberry Pi via **USB**.
3. Ensure the **Extended Lens Cable** is routed away from the stepper motor wires to prevent EMI (Interference).
4. Clear the print bed of all obstructions.

## 💻 Software Logic

The system utilizes a Python-based controller that communicates with the printer via **G-Code** over a Serial connection.

### Core Loop:

1. **Home All Axes (`G28`)**: Establishes the `0,0,0` origin.
2. **Lift to Altitude**: Moves the Z-axis to the 5-inch mark.
3. **Coordinate Iteration**:
* Calculates the next  coordinate.
* Sends `G1` movement command.
* Waits **1.5 seconds** for mechanical vibrations to settle.
* Triggers the `Picamera2` capture.


4. **Save & Rename**: Images are saved with coordinate-based filenames (e.g., `x4_y2.jpg`) into a timestamped session folder.

## ⚠️ Important Considerations

* **NoIR Lighting:** Since this is the NoIR (No Infrared) camera, standard daylight may appear discolored. For best results, use a consistent **IR Light source** mounted to the gantry for "night-vision" style scanning.
* **Step Overlap:** Given the **Wide Angle** lens (120° FOV) at 5 inches high, the 0.5-inch step will result in significant image overlap. This is ideal for photogrammetry or stitching software.
* **Serial Port:** On Linux/Pi, the printer usually appears at `/dev/ttyUSB0`. If the script fails to connect, verify the port using `ls /dev/tty*`.

---

