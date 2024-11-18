import cv2
import numpy as np
from mss import mss
from ultralytics import YOLO

# Загрузка модели YOLO
#model = YOLO('amogus.pt')
model = YOLO('amogus.onnx')
color = (0, 255, 255)
#model.predict(source="0", show=True, conf=0.4)


# Создаем объект для захвата экрана
with mss() as sct:
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # Укажите размеры экрана, которые вы хотите захватить
    while True:
        # Делаем скриншот экрана
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        # Обработка кадра с помощью YOLO
        results = model(screenshot)[0]

        for class_id, box in zip(results.boxes.cls.cpu().numpy(),
                                 results.boxes.xyxy.cpu().numpy().astype(np.int32)):
            class_name = results.names[int(class_id)]
            x1, y1, x2, y2 = box
            cv2.rectangle(screenshot, (x1, y1), (x2, y2), color, 2)
            cv2.putText(screenshot,
                        class_name,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        color, 2)

        # Отображаем результат в окне OpenCV с размером 1920x1080
        cv2.imshow("YOLO Object Detection", cv2.resize(screenshot, (1920, 1080)))

        # Выход из цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()