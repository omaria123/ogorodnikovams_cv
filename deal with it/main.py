import cv2
import numpy as np

def create_transparent_glasses(glasses_img, black_threshold=50):

    lower_black = np.array([0, 0, 0], dtype="uint8")
    upper_black = np.array([black_threshold, black_threshold, black_threshold], dtype="uint8")

    mask = cv2.inRange(glasses_img, lower_black, upper_black)

    b, g, r = cv2.split(glasses_img)
    alpha = mask  
    glasses_rgba = cv2.merge((b, g, r, alpha))
    
    return glasses_rgba
def overlay_glasses(image, glasses, x, y, w, h):
    glasses_resized = cv2.resize(glasses, (w, h), interpolation=cv2.INTER_AREA)

    if glasses_resized.shape[0] > image.shape[0] or glasses_resized.shape[1] > image.shape[1]:
        return image

    alpha = glasses_resized[:, :, 3] / 255.0
    glasses_rgb = glasses_resized[:, :, :3]

    y1, y2 = max(0, y), min(image.shape[0], y + h)
    x1, x2 = max(0, x), min(image.shape[1], x + w)

    glasses_rgb = glasses_rgb[:y2-y1, :x2-x1]
    alpha = alpha[:y2-y1, :x2-x1]

    for c in range(3):
        image[y1:y2, x1:x2, c] = (1.0 - alpha) * image[y1:y2, x1:x2, c] + alpha * glasses_rgb[:, :, c]
    
    return image

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
capture = cv2.VideoCapture(0+cv2.CAP_DSHOW)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, -4)

face_cascade = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade-eye.xml")
glasses = cv2.imread("deal-with-it.png")  

if glasses is not None:
    glasses = create_transparent_glasses(glasses, black_threshold=50)

while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        continue
        
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    for (fx, fy, fw, fh) in faces:

        roi_gray = gray[fy:fy+fh, fx:fx+fw]
        roi_color = frame[fy:fy+fh, fx:fx+fw]

        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)

        if len(eyes) == 2:
            eyes = sorted(eyes, key=lambda x: x[0])
            (ex1, ey1, ew1, eh1), (ex2, ey2, ew2, eh2) = eyes

            distance = abs((ex1 + ew1/2) - (ex2 + ew2/2))
            if distance < fw/2 and glasses is not None:
                x = fx + min(ex1, ex2)
                y = fy + min(ey1, ey2)
                w = max(ex1 + ew1, ex2 + ew2) - min(ex1, ex2)
                h = max(ey1 + eh1, ey2 + eh2) - min(ey1, ey2)

                w = int(w * 1.5)
                h = int(h * 1.5)
                x -= int((w - (max(ex1 + ew1, ex2 + ew2) - min(ex1, ex2))) / 2)
                y -= int((h - (max(ey1 + eh1, ey2 + eh2) - min(ey1, ey2))) / 2)

                try:
                    frame = overlay_glasses(frame, glasses, x, y, w, h)

                    #cv2.rectangle(frame, (fx+ex1, fy+ey1), (fx+ex1+ew1, fy+ey1+eh1), (255, 0, 0), 2)
                    #cv2.rectangle(frame, (fx+ex2, fy+ey2), (fx+ex2+ew2, fy+ey2+eh2), (255, 0, 0), 2)
                    #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                except Exception as e:
                    print(f"Error: {e}")
                    pass

    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        break

    cv2.imshow("Camera", frame)

capture.release()
cv2.destroyAllWindows()