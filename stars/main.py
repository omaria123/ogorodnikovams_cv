import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from collections import defaultdict

def is_star(obj_pixels, shape):
    min_y, max_y = min(p[0] for p in obj_pixels), max(p[0] for p in obj_pixels)
    min_x, max_x = min(p[1] for p in obj_pixels), max(p[1] for p in obj_pixels)
    
    obj_matrix = np.zeros((max_y-min_y+3, max_x-min_x+3), dtype=bool)
    for y, x in obj_pixels:
        obj_matrix[y-min_y+1, x-min_x+1] = True
    
    endpoints = 0
    for y in range(1, obj_matrix.shape[0]-1):
        for x in range(1, obj_matrix.shape[1]-1):
            if obj_matrix[y,x]:
                neighbors = np.sum(obj_matrix[y-1:y+2, x-1:x+2]) - 1
                if neighbors == 1:
                    endpoints += 1
    return endpoints >= 4

def count_stars(image):
    labeled = label(image)
    regions = defaultdict(list)
    for y in range(labeled.shape[0]):
        for x in range(labeled.shape[1]):
            if labeled[y,x] > 0:
                regions[labeled[y,x]].append((y,x))
    
    star_count = 0
    for obj_id, pixels in regions.items():
        if len(pixels) < 5:  
            continue
        
        if is_star(pixels, image.shape):
            star_count += 1
    
    return star_count

image = np.load("stars.npy") 
stars = count_stars(image)
print(f"Количество звездочек: {stars}")

plt.imshow(image)
plt.show()