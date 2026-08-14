import cv2
from ultralytics import YOLO

model = YOLO(r"C:\Users\siriu\OneDrive\Escritorio\SigiRec (4)\SigiRec\runs\detect\train-3\weights\best.pt")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    results = model(frame)
    annotated_frame = results[0].plot()
    cv2.imshow("SIGIREC IA", annotated_frame)
    tecla = cv2.waitKey(1)  

    if tecla == 27:  #La tecla 27 es ESC
        break

cap.release()
cv2.destroyAllWindows()