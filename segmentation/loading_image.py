import cv2



def load_image(ip_address):
    cap = cv2.VideoCapture(ip_address)
    i = 0
    while True:
        i = (i + 1) % 15
        if i % 15 == 0:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 0)
           # cv2.imshow('frame', frame)
            if cv2.waitKey(30) == 27:
                break
            yield frame
    cap.release()
    cv2.destroyAllWindows()