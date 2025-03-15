import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage.morphology import (binary_closing, binary_opening, binary_dilation, binary_erosion)
data = np.load("wires6npy.txt")

labeled = label(data)
result = binary_erosion(data, np.ones(3).reshape(3, 1))
num_wires = np.max(labeled)
print("Количество проводов:", num_wires)

for wire in range(1, num_wires + 1):
    nwire = (labeled == wire)
    labeled_wire = label(nwire)
    erosia = binary_erosion(nwire, np.ones(3).reshape(3, 1))
    num_parts = np.max(label(erosia))
    if num_parts > 1:
        print(f"Провод {wire} порван на {num_parts} частей")
    elif wire >= np.max(labeled):
        print (f"Провод {wire} не существует")
    else:
        print(f"Провод {wire} не порван")

plt.imshow(result)
plt.show()