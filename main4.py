import os
from numba import jit, cuda

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
from ultralytics import YOLO
model = YOLO("yolov8n.pt")


def recv():
    results = model.track(source="video.mp4", show = True)
    return results

if __name__ == "__main__":
    a = recv()

