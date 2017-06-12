import cv2

cap = cv2.VideoCapture('http://192.168.1.30:8080/video?x.mjpeg')

while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(30) == 27:
        break
cap.release()
cv2.destroyAllWindows()