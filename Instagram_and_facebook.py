from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import keyboard
import re
import pyautogui


def facebook():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get("https://www.facebook.com")
    time.sleep(2)
    keyboard.write("")#Enter your email here
    pyautogui.press("tab")
    keyboard.write("")#Enter your password here
    time.sleep(0.7)
    pyautogui.press("tab")
    time.sleep(0.7)
    pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(7)
    htm = driver.page_source
    k = str(re.search("aria-label=\"Messenger(.*)\"", htm))
    last_char_index = k.rfind("\"")
    k = k[:last_char_index] + "," + k[last_char_index + 1:]
    k = k[k.index("ger") + 4:k.rfind("\"")]
    res = [int(i) for i in k.split() if i.isdigit()]
    try:
        res = str(res[0])
    except:
        res = ""
    if res == "":
        k = "Sir you are all caught up"
    else:
        if res == "1":
            k = "Sir you have {} new message".format(res)
        else:
            k = "Sir you have {} new messages".format(res)
    return k
def instagram():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get("https://www.instagram.com")
    time.sleep(2)
    pyautogui.press("tab")
    pyautogui.press("tab")
    keyboard.write("")#Enter your email here
    pyautogui.press("tab")
    keyboard.write("")#Enter your password here
    time.sleep(0.4)
    pyautogui.press("tab")
    time.sleep(0.4)
    pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(7)
    htm = driver.page_source
    try:
        k = htm[htm.index("bqXJH\">")+7:]
        k = k[:k.index("<")]
        k = "Sir you Have {} new messages".format(k)
    except:
        k = "You are all caught up sir"
    return k
