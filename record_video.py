# importing the required packages
import pyautogui
import cv2, os
import numpy as np

def record_video():
    # Specify resolution
    resolution = (1920, 1080)

    # Specify video codec
    codec = cv2.VideoWriter_fourcc(*"XVID")

    # Specify name of Output file
    if os.path.exists("videos/video.mp4"):
        os.remove("videos/video.mp4")
    if os.path.exists("videos/video-small.mp4"):
        os.remove("videos/video-small.mp4")
    filename = "videos/video.mp4"

    # Specify frames rate. We can choose any
    # value and experiment with it
    fps = 40

    # Creating a VideoWriter object
    out = cv2.VideoWriter(filename, codec, fps, resolution)

    # Create an Empty window
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

    # Resize this window
    cv2.resizeWindow("Live", 24, 13)

    while True:
        # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()

        # Convert the screenshot to a numpy array
        frame = np.array(img)

        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Write it to the output file
        out.write(frame)

        # Optional: Display the recording screen
        # cv2.imshow('Live', frame)

        # Stop recording when we press 'q'
        if cv2.waitKey(1) in (ord('q'), ord('й')):
            break

    # Release the Video writer
    out.release()

    # Destroy all windows
    cv2.destroyAllWindows()

    os.system('ffmpeg -i videos/video.mp4 -b 4000k videos/video-small.mp4')

if __name__ == "__main__":
    record_video()