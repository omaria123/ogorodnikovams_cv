import cv2
import mss
import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import time

pyautogui.PAUSE = .01

def fullscreen():
    with mss.mss() as screenshot_tool:
        screenshot = screenshot_tool.grab(screenshot_tool.monitors[0])
        pixel_data = np.frombuffer(screenshot.rgb, dtype="uint8")
        return pixel_data.reshape((screenshot.height, screenshot.width, 3))
    
def part_screen(x, y, width, height):
    with mss.mss() as screenshot_tool:
        safe_width = max(1, width)
        safe_height = max(1, height)
        capture_area = {"top": y, "left": x, "width": safe_width, "height": safe_height}
        screenshot = screenshot_tool.grab(capture_area)
        pixel_data = np.frombuffer(screenshot.rgb, dtype="uint8")
        return pixel_data.reshape((screenshot.height, screenshot.width, 3))
    
def get_bottom_y(img):
    for y_coord in range(img.shape[0]): 
        b_pixels = 0  
        for x_coord in range(img.shape[1]):  
            if not img[y_coord][x_coord]:  
                b_pixels += 1
                if b_pixels > 200:
                    return y_coord  
            else:
                b_pixels = 0   
                
def get_cactus_width(img):
    c_zone = img[-50:-15, 150:350]
    c_zone = c_zone.sum(axis=0)
    start = end = 0
    for i in range(len(c_zone)):
        if c_zone[i] != 0:
           start = i
           break
    for i in range(len(c_zone)-1, 0, -1):
        if c_zone[i] != 0:
            end = i
            break
    return max(end-start, 20)


img = fullscreen()

img = img[100:-100, 200:-200, 2] > 200

bottom_y = get_bottom_y(img)
#print(bottom_y)
left_x = np.where(img[bottom_y] == 0)[0][0] + 200
#print(left_x)

bottom_y += 100

width = 749
height = 170

game_img = part_screen(left_x, bottom_y-height, width, height)[:,:,2] < 200

#plt.imshow(game_img)
#plt.show()
cv2.namedWindow('Game', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Game', cv2.WND_PROP_TOPMOST, 1)
start = time.time()
time.sleep(2)
pyautogui.press("space")                                  
while True:
    k = max(0.4, 1 - (time.time()-start)/120)  
    game_img = part_screen(left_x, bottom_y-height, width, height)[:,:,2] < 200
    d_zone = game_img[-40:-15, 150:210]
    cv2_img = ((game_img==0) * 255).astype("uint8")
    cv2_img[-40:-15, 150:210]//=2
    cv2.imshow('Game', cv2_img)
    
    if np.any(d_zone):       
        pyautogui.press("space")
        k2 = get_cactus_width(game_img)/25 
        time.sleep(0.26 * k * (k2**0.8))  
        pyautogui.press("down")
    
    if cv2.pollKey()==7536640:
        cv2.destroyAllWindows()
        break
    
            
