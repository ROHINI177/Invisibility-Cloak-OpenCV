import cv2
import numpy as np
import time

print("""
Harry :  Hey !! Would you like to try my invisibility cloak ??
         It's awesome !!

         Prepare to get invisible .....................
""")

# Capture from webcam
cap = cv2.VideoCapture(0)
time.sleep(3)  # wait for camera to warm up

# Capture background (30 frames for smoothness)
for i in range(30):
    ret, background = cap.read()
background = np.flip(background, axis=1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: Failed to grab frame from webcam.")
        break

    frame = np.flip(frame, axis=1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ✅ Proper red color ranges in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # ✅ Noise removal (important)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)

    # Inverse mask
    mask_inv = cv2.bitwise_not(mask)

    # Cloak effect
    res1 = cv2.bitwise_and(background, background, mask=mask)      # replace cloak area with background
    res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)            # keep rest of frame
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    # Show outputs
    cv2.imshow("🧙 Invisibility Cloak", final_output)
    cv2.imshow("🎭 Mask Debug (White = Detected Red)", mask)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
