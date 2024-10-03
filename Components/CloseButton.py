import pyautogui
pyautogui.useImageNotFoundException(False)

from Components.LoadImages import load_images_from_path

GLOBAL_PATH = "Images/Global"

close_button_imgs = load_images_from_path(GLOBAL_PATH, "close_button_")


def close_button():
    count = 0
    while count < 20:
        for _, image_path in close_button_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.85)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
    return False
