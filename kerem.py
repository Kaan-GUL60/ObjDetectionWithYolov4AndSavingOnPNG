import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os
import shutil
from selenium.webdriver.common.by import By
import cv2
import numpy as np

#--------------------------------------------------------------------------------------------
model = cv2.dnn.readNetFromDarknet("yolov4-obj.cfg", "yolov4.weights")
layers = model.getLayerNames()
unconnect = model.getUnconnectedOutLayers()
unconnect = unconnect - 1

output_layers = []
for i in unconnect:
    output_layers.append(layers[int(i)])

classFile = 'obj.names'
classNames = []
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
print(classNames)

path = rf"C:\Users\{os.getlogin()}\Downloads"

#----------------------------------------------------------------------------
url = str(input("link giriniz: "))


print(path)

y = int(input("giriş kısmı var mı yoksa direkt çözüme mi geçmiş(giriş varsa 0 yoksa 1 yazın: "))
bekleme_suresi = int(input("Bekleme süresini giriniz: "))
k = int(input("kaçıncı sorudan itibaren alsın: "))
s = int(input("kaç soru var: "))

chrome_options = Options()
chrome_options.add_extension(r"extension_4_1_53_0.crx")
chrome_options.add_extension(r"extension_2_4_1_0.crx")

driver = webdriver.Chrome(options=chrome_options)
a = ActionChains(driver)

driver.get(url)
driver.maximize_window()

time.sleep(5)

driver.switch_to.window(driver.window_handles[0])
time.sleep(3)

driver.find_element(By.CLASS_NAME, "ytp-settings-button").click()

time.sleep(0.5)
driver.find_element("xpath", '//div[contains(text(),"Kalite")]').click()
time.sleep(0.5)
driver.find_element("xpath", '//span[contains(string(),"1080p")]').click()
time.sleep(1.5)

for photo in range(k-1, s+1):

    time.sleep(bekleme_suresi)
    driver.find_element(By.CLASS_NAME, "screenshotButton").click()
    time.sleep(2)

    filename = max([path + "\\" + f for f in os.listdir(path)], key=os.path.getctime)
    shutil.move(filename, os.path.join(path, f"{photo + y}.png"))
    time.sleep(1)
    print(rf'{path}\{photo+y}.png')

    img = cv2.imread(rf"C:\Users\{os.getlogin()}\Downloads\0.png")
    img_taslak = cv2.imread('bgrand.png')
    img_width = img.shape[1]
    img_height = img.shape[0]

    img_blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), swapRB=True)

    model.setInput(img_blob)
    detection_layers = model.forward(output_layers)

    ids_list = []
    boxes_list = []
    confidences_list = []

    for detection_layer in detection_layers:
        for object_detection in detection_layer:
            scores = object_detection[5:]
            predicted_id = np.argmax(scores)
            confidence = scores[predicted_id]

            if confidence > 0.10:
                label = classNames[predicted_id]
                bounding_box = object_detection[0:4] * np.array([img_width, img_height, img_width, img_height])
                (box_center_x, box_center_y, box_width, box_height) = bounding_box.astype("int")
                start_x = int(box_center_x - (box_width / 2))
                start_y = int(box_center_y - (box_height / 2))

                ids_list.append(predicted_id)
                confidences_list.append(float(confidence))
                boxes_list.append([start_x, start_y, int(box_width), int(box_height)])

    max_ids = cv2.dnn.NMSBoxes(boxes_list, confidences_list, 0.5, 0.4)

    for max_id in max_ids:
        max_class_id = max_id
        max_class_id = max_id
        box = boxes_list[max_class_id]

        start_x = box[0]
        start_y = box[1]
        box_width = box[2]
        box_height = box[3]

        predicted_id = ids_list[max_class_id]
        label = classNames[predicted_id]
        print(classNames[predicted_id])
        confidence = confidences_list[max_class_id]

        end_x = start_x + box_width
        end_y = start_y + box_height

        kesilen_soru = img[start_y:end_y, start_x:end_x]
        img_taslak[start_y:end_y, start_x:end_x] = kesilen_soru

        cv2.putText(img, label, (start_x, start_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, 1)

    cv2.imwrite("test_sonuc.png", img_taslak)

    cv2.imshow("img", img)
    cv2.waitKey(0)

    a.key_down(Keys.CONTROL).send_keys(Keys.ARROW_RIGHT).key_up(Keys.CONTROL).perform()
