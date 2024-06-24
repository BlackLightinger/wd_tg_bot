from ppadb.client import Client as AdbClient
from PIL import Image
import io
import numpy as np
import cv2
from time import sleep



def find_button(main_img, tmp_img):
    img_rgb = cv2.imread(main_img)
    template = cv2.imread(tmp_img)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)
    res = (loc[::-1])
    return res[0][0], res[1][0]

#find_button("main.png", "in_battle.png")


def get_screenshot(device):
    screenshot = device.screencap()
    image = Image.open(io.BytesIO(screenshot))

    image.save("screenshot.png")


#adb.exe connect localhost:5555
client = AdbClient(host="127.0.0.1", port=5037)

device = client.devices()[0]


sleep(5)

count = 0
flag = 0
get_screenshot(device)


while True:

    try:
        x, y = find_button("screenshot.png", "coin.png")
        device.shell(f"input tap {x} {y}")
        sleep(0.3)
        count += 1
    except:
        pass

    if count >= 100:
        flag = 1

    if flag:
        try:
            get_screenshot(device)
            x, y = find_button("screenshot.png", "wallet.png")
            device.shell(f"input tap {x + 10} {y + 10}")
            flag = 0
            count = 0
        except:
            pass