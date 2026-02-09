
---

# 🛰️ EnderScan-XY: Automated Grid Imaging System (v2.1)

A high-precision, 2D gantry-based imaging system built from a repurposed **Ender 3 Pro** and a **Raspberry Pi Camera Module V3 Wide NoIR**. This system automates a **100-point scan** with fixed-altitude safety protocols and precise motion synchronization.

## 🛠 Hardware Configuration

* **Motion Controller:** Ender 3 Pro Motherboard
* **Imaging:** Raspberry Pi Camera Module V3 (Wide Angle, NoIR) - IMX219 sensor with fixed-focus lens
* **Connection:** USB (Serial) @ 115200 Baud
* **Mounting:** X-Carriage mount at 5-inch (127mm) Z-clearance

## 📐 Scan Specifications

* **Z-Height:** 5.0 inches (127mm) **Fixed Altitude** (maintained during entire scan and exit)
* **Scan Origin:** X=2.0 inches (50.8mm), Y=2.0 inches (50.8mm) - positioned to center grid over target area
* **Grid Density:** 10 × 10 (100 total capture points)
* **Step Increment:** 0.5 inches (12.7mm)
* **Scan Area:** 4.5 × 4.5 inches from origin point
* **Pattern:** **Snake/Boustrophedon** (zig-zag) for efficiency and cable management

## 🚀 Installation & Setup

### 1. Raspberry Pi Preparation

```bash
pip install pyserial
sudo apt install libcamera-apps
```

### 2. Physical Setup

1. Mount the **Pi Camera V3** to the X-axis carriage
2. Ensure the **Extended Lens Cable** has enough slack to reach all positions at 5-inch height
3. Connect Ender 3 to Raspberry Pi via USB
4. Verify connection: `ls /dev/ttyUSB*`

### 3. Add User to Dialout Group (if needed)

```bash
sudo usermod -a -G dialout $USER
# Log out and back in for changes to take effect
```

## 💻 Software Logic & Features

### 🎯 Fixed-Focus Design

The **IMX219 sensor** uses a **fixed-focus lens** (no autofocus hardware). The lens is factory-focused to infinity, which provides acceptable sharpness at the 5-inch working distance. For optimal focus:
- Ensure subjects are positioned at exactly 5 inches from the lens
- Consider manual lens adjustment if your camera module allows it
- Test focus quality before running full scans

### 🐍 Snake Pattern Scanning

The system moves **left-to-right** on Row 0, then **right-to-left** on Row 1, alternating for all 10 rows. Benefits:
- Reduces mechanical wear and total travel distance
- Prevents camera cable whiplash from direction changes
- Minimizes scan time

### ⚙️ Motion Synchronization (M400)

Uses G-code `M400` command to ensure **complete motion stop** before image capture:
- Prevents blurry images from vibration
- Guarantees camera initializes only after printer reaches working height
- Synchronizes all movements with 0.3s vibration settling time

### 🛡️ Collision Prevention

**Safe Z-Height Protocol:**
1. Home all axes with `G28`
2. Immediately lift to 5 inches (127mm)
3. Move to scan origin (2", 2")
4. **Camera initializes only after all movement complete**
5. At scan end: return to origin **while maintaining 5-inch height**
6. **No final homing** - prevents camera crash into subject

### 📋 Core Workflow

1. **Setup Phase:**
   - Connect to printer
   - Set units (G21=mm) and absolute positioning (G90)
   - Home axes → Lift to Z=127mm → Move to start position
   - Wait for M400 confirmation at each step

2. **Initialization:**
   - Initialize camera (only after mechanical setup complete)
   - Allow 2 seconds for exposure/white balance stabilization

3. **Scan Loop (100 points):**
   - Move to next grid position
   - M400 wait + 0.3s vibration settling
   - Capture image to timestamped folder
   - Snake pattern: alternate row directions

4. **Safe Shutdown:**
   - Stop camera
   - Return to origin at safe Z-height
   - M400 final confirmation

## ⚠️ Important Considerations

* **EMI Interference:** Route the extended ribbon cable away from stepper motor wiring to prevent image artifacts (purple lines, noise)
* **NoIR Sensor:** Use IR LEDs for consistent lighting - visible light will cause color shifts
* **Coordinate Mapping:** Images saved as `x[col]_y[row].jpg` (e.g., `x5_y3.jpg`) for easy grid reconstruction
* **Focus Distance:** IMX219 fixed lens optimized for ~8-12 inches - at 5 inches, slight softness may occur. Test and adjust Z-height if needed.

## 🛠 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| **"SerialException: could not open port"** | Wrong USB port or permission denied | Run `ls /dev/ttyUSB*` to find port. Add user to dialout group: `sudo usermod -a -G dialout $USER` |
| **Camera captures during Z-lift** | Camera initialized before movement complete | Script now uses M400 to wait - ensure you're running latest version |
| **"Camera timeout" or purple lines** | EMI from stepper motors or loose cable | Route ribbon cable away from motor wires. Verify cable seating at both ends |
| **Images are blurry** | Vibration, wrong focus distance, or motion not settled | Increase settling time to 0.5-1.0s. Verify subject is at 5" height. Consider adjusting Z-height to 8-10" for sharper focus |
| **Printer doesn't move** | Baud rate mismatch or firmware issue | Verify 115200 baud. Check printer display for errors. Try manual G-code commands via serial terminal |
| **"RuntimeError: Control AfMode not advertised"** | Trying to use autofocus on fixed-focus camera | Script updated to remove autofocus - IMX219 is fixed-focus only |
| **Grid offset wrong** | Incorrect OFFSET_X/OFFSET_Y values | Verify `OFFSET_X = 50.8` and `OFFSET_Y = 50.8` (2 inches) in script |

## 📁 Output Structure

```
scan_1770572682/
├── x0_y0.jpg
├── x1_y0.jpg
├── x2_y0.jpg
...
├── x9_y9.jpg
```

Images are named by grid position for easy reassembly into composite images or photogrammetry workflows.

---

**Version 2.1 Changes:**
- Removed autofocus (not supported on IMX219)
- Added M400 motion synchronization
- Implemented 2-inch X/Y offset for scan area positioning
- Camera now initializes only after mechanical setup complete
- Reduced vibration settling time to 0.3s (M400 ensures move completion)
