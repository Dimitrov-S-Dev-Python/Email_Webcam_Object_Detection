import glob
import os
import cv2
import time
from send_email import send_email

# connect to default camera
# (default webcam is 0)
video = cv2.VideoCapture(0)

time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    all_images = glob.glob("images/*.png")
    for image in all_images:
        os.remove(image)


image_with_obj = ""

while True:
    status = 0
# read a frame from video stream
    check, frame = video.read()
# convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# apply background subtraction
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (11, 11), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# draw bounding boxes
    for contour in contours:
        # ignore small contours
        if cv2.contourArea(contour) < 5_000:
            continue
        # draw bounding box around contour
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}image.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_obj = all_images[index]
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email(image_with_obj)
        clean_folder()

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()




