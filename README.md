Yes, we should definitely update the **README**. Since we added the **Focus Lock** feature and changed the **Shutdown Sequence** to prevent the camera from crashing into your subject, the documentation needs to reflect those safety improvements.

Here is the updated version.

---

# 🛰️ EnderScan-XY: Automated Grid Imaging System (v2.0)

A high-precision, 2D gantry-based imaging system built from a repurposed **Ender 3 Pro** and a **Raspberry Pi Camera Module V3 Wide NoIR**. This system automates a **100-point scan** with fixed-altitude safety protocols.

## 🛠 Hardware Configuration

* **Motion Controller:** Ender 3 Pro Motherboard.
* **Imaging:** Raspberry Pi Camera Module V3 (Wide Angle, NoIR).
* **Connection:** USB (Serial) @ 115200 Baud.
* **Mounting:** X-Carriage mount at 5-inch (127mm) Z-clearance.

## 📐 Scan Specifications

* **Z-Height:** 5.0 inches (127mm) **Fixed Altitude** (Maintained during exit).
* **Grid Density:** 10 x 10 (100 total capture points).
* **Step Increment:** 0.5 inches (12.7mm).
* **Pattern:** **Snake/Boustrophedon** (Zig-Zag) for efficiency.

## 🚀 Installation & Setup

### 1. Raspberry Pi Preparation

```bash
pip install pyserial
sudo apt install libcamera-apps

```

### 2. Physical Setup

1. Mount the **Pi Camera V3** to the X-axis carriage.
2. Ensure the **Extended Lens Cable** has enough slack to reach  at a 5-inch height.
3. Connect via USB.

## 💻 Software Logic & Features

### 🟢 Focus Lock (New)

To prevent the camera from "hunting" for focus at every stop (which adds time and causes inconsistency), the script performs one `autofocus_cycle()` at the start and locks the lens position for the entire 100-image duration.

### 🐍 Snake Pattern

The system moves  on Row 1, then  on Row 2. This reduces mechanical strain and prevents the long camera cable from whip-lashing.

### 🛡️ Crash Prevention (Updated)

Standard `G28` (Homing) is **disabled** at the end of the scan. The system is programmed to stay at the 5-inch Z-height while returning to the `0,0` origin to ensure it passes safely over the scanned object.

### Core Loop:

1. **Home & Lift:** Home axes and immediately rise to 5 inches.
2. **Focus:** Lock focus at the start position.
3. **Move → Pause → Snap:** * Move to .
* **Wait 1.5s** (Settling time).
* Capture to timestamped folder.


4. **Safe Return:** Return to `X0 Y0` while maintaining `Z127`.

## ⚠️ Important Considerations

* **EMI Interference:** Keep the extended ribbon cable away from the stepper motors to avoid image artifacts.
* **NoIR Lighting:** Use IR LEDs for consistent exposure, as the NoIR sensor will shift colors in natural light.
* **Coordinate Mapping:** Images are saved as `img_x[col]_y[row].jpg` for easy sorting.

---

Here is the updated **Troubleshooting** section for your README, followed by the final, complete code.

### 🛠 Troubleshooting Section (Add to README)

| Issue | Cause | Solution |
| --- | --- | --- |
| **"SerialException: could not open port"** | Wrong USB port or permission denied. | Run `ls /dev/ttyUSB*` to find the port. Ensure your user is in the `dialout` group. |
| **"Camera timeout" or purple lines** | EMI from motors or loose cable. | Route the extended lens cable away from motor wires. Check the ribbon seating. |
| **Images are blurry** | Vibration or Focus Lock failed. | Increase `time.sleep` to **2.0** or ensure the subject is 5 inches away during the initial focus. |
| **Printer doesn't move** | Baud rate mismatch or "Locked" state. | Ensure `BAUD` is 115200. Check if the printer screen says "Homing Failed." |

---





