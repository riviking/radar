import serial
import matplotlib.pyplot as plt
import numpy as np
import time


# ============================================================
# SETTINGS
# ============================================================

PORT = "COM4"
BAUD_RATE = 115200

MIN_DISTANCE = 2
MAX_DISTANCE = 200

MIN_ANGLE = 0
MAX_ANGLE = 90


# ============================================================
# OBJECT DETECTION
# ============================================================

DETECTION_LIMIT = 195


# ============================================================
# CONNECT TO ARDUINO
# ============================================================

print("======================================")
print("       ULTRASONIC RADAR")
print("======================================")
print()

print("Connecting to Arduino...")

try:

    ser = serial.Serial(
        PORT,
        BAUD_RATE,
        timeout=1
    )

    time.sleep(2)

    ser.reset_input_buffer()

    print("Arduino connected!")
    print("Port:", PORT)
    print("Baud:", BAUD_RATE)
    print()

except serial.SerialException as e:

    print()
    print("ERROR: Could not connect to Arduino")
    print()
    print("Check:")
    print("1. Arduino is connected")
    print("2. Correct COM port")
    print("3. Serial Monitor is CLOSED")
    print("4. Serial Plotter is CLOSED")
    print()
    print("Error:", e)

    exit()


# ============================================================
# CREATE RADAR WINDOW
# ============================================================

plt.ion()

fig = plt.figure(
    figsize=(10, 8),
    facecolor="black"
)

ax = fig.add_subplot(
    111,
    polar=True,
    facecolor="black"
)


# ============================================================
# RADAR CONFIGURATION
# ============================================================

ax.set_theta_zero_location("E")

ax.set_theta_direction(1)

ax.set_thetamin(0)

ax.set_thetamax(90)

ax.set_rmin(0)

ax.set_rmax(200)


# ============================================================
# ANGLE LABELS
# ============================================================

ax.set_thetagrids(
    [0, 10, 20, 30, 40, 50, 60, 70, 80, 90],
    labels=[
        "0°",
        "10°",
        "20°",
        "30°",
        "40°",
        "50°",
        "60°",
        "70°",
        "80°",
        "90°"
    ],
    color="white"
)


# ============================================================
# DISTANCE LABELS
# ============================================================

distance_ticks = [
     20,  40, 
    60,  80,  100,
     120,  140, 
    160,  180,  200
]

ax.set_rticks(distance_ticks)

ax.set_yticklabels([
    
    "20 cm",
  
    "40 cm",
   
    "60 cm",

    "80 cm",

    "100 cm",
    
    "120 cm",

    "140 cm",

    "160 cm",

    "180 cm",

    "200 cm"
])


ax.set_rlabel_position(90)

ax.tick_params(colors="white")


# ============================================================
# TITLE
# ============================================================

ax.set_title(
    "ULTRASONIC RADAR",
    color="white",
    fontsize=24,
    fontweight="bold",
    pad=25
)

ax.grid(
    True,
    linewidth=0.8,
    alpha=0.5
)


# ============================================================
# DATA ARRAYS
# ============================================================

distances = np.full(
    MAX_ANGLE + 1,
    MAX_DISTANCE,
    dtype=float
)


# ============================================================
# PLOT OBJECTS
# ============================================================

# Sweep line

sweep_line, = ax.plot(
    [],
    [],
    linewidth=2
)


# ============================================================
# OBJECT BUBBLE + INFORMATION
# ============================================================

object_point, = ax.plot(
    [],
    [],
    "o",
    markersize=14,
    color="red"
)

object_label = ax.annotate(
    "",
    xy=(0, 0),
    xytext=(12, 12),
    textcoords="offset points",
    color="white",
    fontsize=12,
    fontweight="bold",
    bbox=dict(
        boxstyle="round,pad=0.4",
        facecolor="black",
        edgecolor="white"
    )
)

# ============================================================
# INFORMATION TEXT
# ============================================================

info_text = fig.text(
    0.02,
    0.04,
    "ANGLE: ---°     DISTANCE: --- cm     STATUS: WAITING",
    color="white",
    fontsize=13,
    fontweight="bold"
)


range_text = fig.text(
    0.67,
    0.04,
    f"RANGE: {MIN_DISTANCE}-{MAX_DISTANCE} cm     PORT: {PORT}",
    color="white",
    fontsize=11
)


# ============================================================
# SWEEP TRACKING
# ============================================================

previous_angle = 0


# ============================================================
# MAIN LOOP
# ============================================================

try:

    while plt.fignum_exists(fig.number):

        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()


        if not line:
            continue


        # ====================================================
        # READ SERIAL DATA
        # ====================================================

        try:

            parts = line.split(",")

            if len(parts) != 2:
                continue

            angle = int(float(parts[0]))

            distance = float(parts[1])

        except ValueError:

            continue


        # ====================================================
        # CHECK ANGLE
        # ====================================================

        if angle < MIN_ANGLE or angle > MAX_ANGLE:
            continue


        # ====================================================
        # CHECK DISTANCE
        # ====================================================

        if distance < MIN_DISTANCE:

            distance = MAX_DISTANCE


        if distance > MAX_DISTANCE:

            distance = MAX_DISTANCE


        # ====================================================
        # NEW SWEEP
        # ====================================================

        if angle < previous_angle:

            distances[:] = MAX_DISTANCE


        previous_angle = angle


        # ====================================================
        # SAVE READING
        # ====================================================

        distances[angle] = distance


        # ====================================================
        # DRAW SWEEP LINE
        # ====================================================

        theta = np.radians(angle)


        sweep_line.set_data(
            [theta, theta],
            [0, MAX_DISTANCE]
        )


        # ====================================================
        # FIND CLOSEST OBJECT
        # ====================================================

        valid_angles = np.where(
            distances < DETECTION_LIMIT
        )[0]


        if len(valid_angles) > 0:

            # Closest detected distance

            closest_index = np.argmin(
                distances[valid_angles]
            )


            closest_angle = valid_angles[
                closest_index
            ]


            closest_distance = distances[
                closest_angle
            ]


            # =================================================
            # SHOW ONE OBJECT BUBBLE
            # =================================================

            object_point.set_data(
                [np.radians(closest_angle)],
                [closest_distance]
            )

            object_label.xy = (
            np.radians(closest_angle),
            closest_distance
            )

            object_label.set_text(
            f"{closest_distance:.1f} cm\n"
            f"{closest_angle}°"
            )

            object_label.set_visible(True)

            # =================================================
            # STATUS
            # =================================================

            info_text.set_text(
                f"ANGLE: {closest_angle:3d}°     "
                f"DISTANCE: {closest_distance:6.1f} cm     "
                f"STATUS: OBJECT DETECTED"
            )


        else:

            object_point.set_data(
                [],
                []
            )


            info_text.set_text(
                f"ANGLE: {angle:3d}°     "
                f"DISTANCE: {distance:6.1f} cm     "
                f"STATUS: CLEAR"
            )


        # ====================================================
        # REDRAW
        # ====================================================

        fig.canvas.draw_idle()

        fig.canvas.flush_events()


except KeyboardInterrupt:

    print()
    print("Radar stopped by user.")


finally:

    try:
        ser.close()

    except:
        pass

    plt.close()

    print("Serial connection closed.")