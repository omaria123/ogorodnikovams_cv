import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label


def detect_pencils(image_path, debug=False):
    img = plt.imread(image_path)
    if img is None:
        print(f"Не удалось загрузить изображение: {image_path}")
        return 0
    count = 0
    gray = img.mean(axis=2)
    binary = gray < 130
    labeled = label(binary)
    regions = regionprops(labeled)
    regions2 = []
    
    #plt.imshow(binary)
    #plt.show()
    for reg in regions:
        if reg.area > 5000 and min(reg.image.shape) > 100:
            regions2.append(reg)
            #plt.title(str(reg.image.shape)+" "+str(reg.eccentricity))
            #plt.imshow(reg.image)
            #plt.show()
            print(reg.area)
            
    print(len(regions2))
    #print(regions2)
    for reg in regions2:
        if reg.eccentricity > 0.97:
            count += 1
            #plt.title(str(reg.image.shape)+" "+str(reg.eccentricity))
            #plt.imshow(reg.image)
            #plt.show()
    return count 







total_pencils = 0
image_files = [f"img ({i}).jpg" for i in range(1, 13)]

for image_file in image_files:
        count = detect_pencils(image_file, debug=True)
        print(f"На изображении {image_file} обнаружено карандашей: {count}")
        total_pencils += count

print(f"\nОбщее количество карандашей: {total_pencils}")

