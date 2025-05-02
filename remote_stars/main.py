import socket
import numpy as np
import matplotlib.pyplot as plt
import cv2

host = "84.237.21.36"
port = 5152

def reveal(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def find_two_points(image):
    img = image.copy()

    pos1 = np.unravel_index(np.argmax(img), img.shape)
    cv2.circle(img, (pos1[1], pos1[0]), 15, 0, -1)
    pos2 = np.unravel_index(np.argmax(img), img.shape)
  
    min_dist = 10  
    if np.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2) < min_dist:
        img[pos2] = 0
        pos2 = np.unravel_index(np.argmax(img), img.shape)
    
    return pos1, pos2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"
    plt.ion()
    plt.figure()

    for i in range(10):
        sock.send(b"get")
        bts = reveal(sock, 40002)
  
        im = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0], bts[1])

        pos1, pos2 = find_two_points(im)

        distance = np.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
        rounded_distance = round(distance, 1)

        sock.send(f"{rounded_distance}".encode())
        response = sock.recv(10)
        print(f"Image {i+1}: Distance: {rounded_distance}, Response: {response}")
 
        plt.clf()
        plt.imshow(im, cmap='gray')
        plt.plot([pos1[1], pos2[1]], [pos1[0], pos2[0]], 'r-', linewidth=2)
        plt.scatter([pos1[1], pos2[1]], [pos1[0], pos2[0]], c='red', s=50)
        plt.title(f"Dist: {rounded_distance}")
        plt.pause(0.3)
 
        sock.send(b"beat")
        beat = sock.recv(10)

plt.ioff()
plt.show()