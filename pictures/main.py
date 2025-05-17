import cv2
import numpy as np

ref_image = cv2.imread('ogorodnikova.png')

def create_masks(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    blue_lower = np.array([90, 50, 50])
    blue_upper = np.array([130, 255, 255])
    pink_lower = np.array([140, 50, 50])
    pink_upper = np.array([170, 255, 255])
    yellow_lower = np.array([20, 50, 50])
    yellow_upper = np.array([40, 255, 255])

    masks = {
        'blue': cv2.inRange(hsv, blue_lower, blue_upper),
        'pink': cv2.inRange(hsv, pink_lower, pink_upper),
        'yellow': cv2.inRange(hsv, yellow_lower, yellow_upper)
    }

    for name, mask in masks.items():
        cv2.imwrite(f'{name}_mask.jpg', mask)
    
    return masks

masks = create_masks(ref_image)

def analyze_video(video_path, ref_masks):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Не удалось открыть видео {video_path}")

    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 

    ref_ratios = {}
    for name, mask in ref_masks.items():
        ref_ratios[name] = np.sum(mask > 0) / (mask.shape[0] * mask.shape[1])
        print(f"соотношение {name}: {ref_ratios[name]:.2%}")
    
    frame_count = 0
    match_count = 0
    match_threshold = 1.8  
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        #if frame_count % 100 == 0:  
            #print(f"Обработано кадров: {frame_count}")
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        match_score = 0
        for name, mask in ref_masks.items():
            lower = np.array([cv2.cvtColor(ref_image, cv2.COLOR_BGR2HSV)[mask > 0].min(axis=0)])
            upper = np.array([cv2.cvtColor(ref_image, cv2.COLOR_BGR2HSV)[mask > 0].max(axis=0)])
            
            current_mask = cv2.inRange(hsv, lower, upper)
            current_ratio = np.sum(current_mask > 0) / (frame.shape[0] * frame.shape[1])
           
            if ref_ratios[name] > 0:
                match_score += min(current_ratio / ref_ratios[name], 1.0)
        
        if match_score >= match_threshold:
            match_count += 1
            cv2.imwrite(f'match_{match_count}.jpg', frame)
    
    cap.release()
    return frame_count, match_count

try:
    total_frames, matches = analyze_video('output.avi', masks)
    print(f"Проанализировано кадров: {total_frames}")
    print(f"Найдено своих изображений: {matches}")
except Exception as e:
    print(f"Ошибка: {e}")
