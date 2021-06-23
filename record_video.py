import cv2
import cv
import numpy as np
import os
import time


def play_video():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 24)  # Частота кадров
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)  # Ширина кадров в видеопотоке.
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Высота кадров в видеопотоке.


    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("camera", gray)  # Будет показывать в оттенках серого.
        # cv2.imshow("camera", img)
        if cv2.waitKey(10) == 27:  # Клавиша Esc
            break
    cap.release()
    cv2.destroyAllWindows()


def get_video(video_url, video_file='kek.avi'):
    cap = cv2.VideoCapture(video_url)
    fps = 20.0
    image_size = (640, 480)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'XVID'), fps, image_size)

    i = 0
    while True:
        ret, frame = cap.read()
        out.write(frame)
        time.sleep(0.05)
        i = i + 1
        if i > 100:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print("Successfully saved")
