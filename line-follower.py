from GUI import GUI
from HAL import HAL
import numpy as np
import cv2

kp = 0.1
kd = 0.01

prev_error = HAL.getImage().shape[1] / 2
accum_error = 0

while True:
    #  Get the image from the camera
    image = HAL.getImage()

    #  Convert the image to grayscale
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_threshold = np.array([0, 120, 70])
    upper_threshold = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_threshold, upper_threshold)
    lower_threshold = np.array([170, 120, 70])
    upper_threshold = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_threshold, upper_threshold)
    mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.bitwise_not(mask)

    #  Find the center of the line
    M = cv2.moments(mask)

    #  If the line is found, calculate the error
    if M['m00'] > 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(image, (cx, cy), 20, (0, 0, 255), 1)
        err = cx - image.shape[1] / 2
        p = err
        d = err - prev_error
        control_signal = p * kp + d * kd

        #  Set the motor speeds
        HAL.setV(1)
        HAL.setW(control_signal)

        #  Update the previous error
        prev_error = err
    else:
        #  If the line is not found, stop the robot
        HAL.setV(1)
        HAL.setW(0)
        prev_error = image.shape[1] / 2
    
    #  Display the image
    GUI.showImage(image)
