from ultralytics import YOLO
import cv2
import numpy as np

# Загрузка модели YOLO
#model = YOLO('yolov8n.pt')
model = YOLO('amogus.pt')
color = (0, 255, 255)
capture = cv2.VideoCapture(str("video3.mp4"))

# Получаем параметры видео: ширина, высота и fps
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = capture.get(cv2.CAP_PROP_FPS)

# Настраиваем VideoWriter для сохранения видео
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Кодек для mp4
output = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

while True:
    ret, frame = capture.read()
    if not ret:
        break  # Выход из цикла, если кадры закончились

    results = model(frame)[0]

    for class_id, box in zip(results.boxes.cls.cpu().numpy(),
                             results.boxes.xyxy.cpu().numpy().astype(np.int32)):
        class_name = results.names[int(class_id)]
        x1, y1, x2, y2 = box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame,
                    class_name,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    color, 2)

    # Сохраняем обработанный кадр в видеофайл
    output.write(frame)

capture.release()
output.release()  # Закрываем VideoWriter после завершения записи
cv2.destroyAllWindows()
