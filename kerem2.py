import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os
import shutil
from selenium.webdriver.common.by import By
from image import fonkfonk
import cv2

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

url = str(input("link giriniz: "))

y = int(input("giriş kısmı var mı yoksa direkt çözüme mi geçmiş(giriş varsa 0 yoksa 1 yazın: "))
bekleme_suresi = int(input("Bekleme süresini giriniz: "))
k = int(input("kaçıncı sorudan itibaren alsın: "))
s = int(input("kaç soru var: "))

path = rf"C:\Users\{os.getlogin()}\Downloads"

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
    fonkfonk(photo+y)
    a.key_down(Keys.CONTROL).send_keys(Keys.ARROW_RIGHT).key_up(Keys.CONTROL).perform()
