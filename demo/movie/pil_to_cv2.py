import numpy as np
import cv2
#pil color
#cv2 gray
def pil_to_cv2(image):
    
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        # new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2GRAY)
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        # new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2GRAY)
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    return new_image
