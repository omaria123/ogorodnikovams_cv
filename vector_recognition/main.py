import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import regionprops, label

def extractor(region):
    area = region.area / region.image.size
    return np.array([area])

def norm_l1(v1, v2):
    return ((v1 - v2) ** 2).sum() ** 0.5

def classificator(v, templates):
    result = "_"
    min_dist = 10 ** 16
    for key in templates:
        d = norm_l1(v, templates[key])
        if d < min_dist:
            result = key
            min_dist = d
    return result

alphabet = plt.imread("alphabet.png")[:, :, :-1]

gray = alphabet.mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)
print(len(regions))

symbols = plt.imread("alphabet-small.png")[:, :, :-1]
gray = symbols.mean(axis=2)
binary = gray < 1
slabeled = label(binary)
sregions = regionprops(slabeled)
print(len(regions))

#plt.imshow(regions[3].image)
#plt.show()
templates = {"A": extractor(regions[4]),
             "B": extractor(regions[1]), 
             "8": extractor(regions[3]), 
             "0": extractor(regions[25]), 
             "1": extractor(regions[5]), 
             "W": extractor(regions[8]), 
             "X": extractor(regions[49]), 
             "*": extractor(regions[14]),
             "-": extractor(regions[2]), 
             "/": extractor(regions[0]), 
             }

print(templates)
for i, region in enumerate(sregions):
    v = extractor(region)
    #plt.subplot(2, 5, i+1)
    #plt.title(classificator(v, templates))
    #plt.imshow(region.image)
result = {}
for region in regions:
    v = extractor(region)
    symbol = classificator(v, templates)
    result[symbol] = result.get(symbol, 0) + 1
    #plt.title(symbol+str(v))
    #plt.imshow(region.image)
    #plt.show()
print(result)
plt.show()
