import numpy as np
import matplotlib.pyplot as plt

external = np.diag([1, 1, 1, 1]).reshape(4, 2, 2)
internal = np.logical_not(external)
cross = np.array([[[1, 0], [0, 1]], [[0, 1], [1, 0]]])

def match(a, masks):
    for mask in masks:
        if np.all((a != 0) == (mask != 0)):
            return True
    return False

def count_objects(image):
    E = 0
    rows, cols = image.shape
    for y in range(rows - 1):
        for x in range(cols - 1):
            sub = image[y:y+2, x:x+2]
            if match(sub, external):
                E += 1
            elif match(sub, internal):
                E -= 1
            elif match(sub, cross):
                E += 2
    return E / 4

image1 = np.load("example1.npy")
image2 = np.load("example2.npy")

plt.figure(figsize=(12, 6))

plt.subplot(1, 4, 1)
plt.title("Изображение 1")
plt.imshow(image1, cmap='gray')

for i in range(3):
    plt.subplot(1, 4, i + 2)
    plt.title(f"Изображение 2, слой {i+1}")
    plt.imshow(image2[:, :, i], cmap='gray')

count_image1 = count_objects(image1)
count_image2_layers = [count_objects(image2[:, :, i]) for i in range(3)]
total_image2 = sum(count_image2_layers)

print("Количество объектов на image1:", count_image1)
print("Количество объектов на image2:", total_image2)

plt.tight_layout()
plt.show()