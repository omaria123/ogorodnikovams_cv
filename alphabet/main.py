import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import regionprops, label
from pathlib import Path


def filling_factor(region):
    return region.image.mean()


def recognize(region):
    if filling_factor(region) == 1:
        return "-"
    
    euler = region.euler_number
    match euler:
        case -1:  
            if 1 in region.image.mean(0):                 
                mean_col = region.image.mean(0)
                if mean_col[-1] == 1:  
                    if region.image.mean(1)[0] == 1:  
                        return "D"
                    else:
                        return "P"
                return "B"
            return "8"
        case 0:  
            tmp = region.image.copy()
            tmp[-1, :] = 1
            tmp_labeled = label(tmp)
            tmp_regions = regionprops(tmp_labeled)
            if tmp_regions[0].euler_number == -1:
                return "A"
            return "0"
        case _:
            if 1 in region.image.mean(0):  
                return "1"
            tmp = region.image.copy()
            tmp[[0, -1], :] = 1
            tmp_labeled = label(tmp)
            tmp_regions = regionprops(tmp_labeled)
            euler = tmp_regions[0].euler_number
            if euler == -1:
                return "X"
            elif euler == -2:
                return "W"
            if region.eccentricity > 0.5:
                return "/"
            else:
                return "*"
    return "?"


symbols = plt.imread(Path(__file__).parent / "symbols.png")
gray = symbols[:, :, :-1].mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)

result = {}
out_path = Path(__file__).parent / "out"
out_path.mkdir(exist_ok=True)
plt.figure()


for i, region in enumerate(regions):
    print(f"{i+1}/{len(regions)}")
    symbol = recognize(region)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
    
    plt.cla()
    plt.title(symbol)
    plt.imshow(region.image)
    plt.savefig(out_path / f"{i:03d}.png")


for symbol, count in sorted(result.items()):
    print(f"{symbol}: {count}")

print("\nОбщее количество символов:", sum(result.values()))