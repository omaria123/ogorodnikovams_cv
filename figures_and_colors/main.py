import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2hsv
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops

def analyze_image(image_path):
    image = plt.imread(image_path)
    hsv = rgb2hsv(image)
    gray = image.mean(axis=2)
    
    thresh = threshold_otsu(gray)
    binary = (gray > thresh * 0.9)  
    labeled = label(binary)
    regions = regionprops(labeled)
 
    circles = []
    rectangles = []
    
    for r in regions:
        if r.area < 30: 
            continue
            
        circularity = (4 * np.pi * r.area) / (max(r.perimeter, 1) ** 2)
        extent = r.area / r.bbox_area
        solidity = r.solidity
        
        circle_score = (circularity * 0.5 + 
                       (1 - r.eccentricity) * 0.3 + 
                       extent * 0.2)
        
        if circle_score > 0.88 and solidity > 0.96:
            circles.append(r)
        else:
            rectangles.append(r)
    
    def get_dominant_hue(region):
        y, x = map(int, region.centroid)
        patch = hsv[y-1:y+2, x-1:x+2, :]  
        if patch.size == 0:
            return 0
       
        mask = (patch[..., 1] > 0.2) & (patch[..., 2] > 0.3)
        return np.median(patch[mask, 0]) if np.any(mask) else 0
 
    def cluster_hues(hues, tol=0.03):
        hues_sorted = np.sort(hues)
        clusters = []
        current = [hues_sorted[0]]
        
        for h in hues_sorted[1:]:
            if h - current[-1] <= tol * (1 + 0.5/(min(h, 1-h)+0.1)):
                current.append(h)
            else:
                if len(current) >= 2:
                    clusters.append(current)
                current = [h]
        
        if len(current) >= 2:
            clusters.append(current)
        
        return {round(np.median(c), 4): len(c) for c in clusters}
  
    circle_hues = [h for r in circles if (h := get_dominant_hue(r)) > 0]
    rect_hues = [h for r in rectangles if (h := get_dominant_hue(r)) > 0]
    
    circle_clusters = cluster_hues(circle_hues)
    rect_clusters = cluster_hues(rect_hues, tol=0.04)
   
    print(f"Общее количество фигур: {len(regions)}")
    print(f"Кругов: {len(circles)}")
    print(f"Прямоугольников: {len(rectangles)}\n")
    
    print("Круги по оттенкам:")
    for hue, count in sorted(circle_clusters.items()):
        print(f"Оттенок {hue:.4f}: {count} шт.")
    
    print("\nПрямоугольники по оттенкам:")
    for hue, count in sorted(rect_clusters.items()):
        print(f"Оттенок {hue:.4f}: {count} шт.")
   
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    ax1.hist(circle_hues, bins=40, range=(0, 1), color='red', alpha=0.7)
    ax1.set_title(f'Круги ({len(circle_clusters)} оттенков)')
    ax1.set_xlabel('Hue')
    ax1.set_ylabel('Количество')
    
    ax2.hist(rect_hues, bins=40, range=(0, 1), color='blue', alpha=0.7)
    ax2.set_title(f'Прямоугольники ({len(rect_clusters)} оттенков)')
    ax2.set_xlabel('Hue')
    
    plt.tight_layout()
    plt.show()
    
    return {
        'total': len(regions),
        'circles': len(circles),
        'rectangles': len(rectangles),
        'circle_hues': circle_clusters,
        'rect_hues': rect_clusters
    }

results = analyze_image('balls_and_rects.png')




