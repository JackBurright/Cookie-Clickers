from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidCookieDomainException

import time
import re
import pickle


chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": "/saveFile",
    "directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)
wait2 = WebDriverWait(driver, 2)
wait10 = WebDriverWait(driver, 10)



def saveCookies(file):
    cookies = driver.get_cookies()
    with open(file, 'wb') as file:
        pickle.dump(cookies, file)
    return

def loadCookies(file):
    current_url = driver.current_url
    current_domain = current_url.split('/')[2]
    with open(file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            if cookie['domain'] == current_domain or cookie['domain'].startswith('.'):
                try:
                    # Add each cookie to the WebDriver session
                    driver.add_cookie(cookie)
                except InvalidCookieDomainException as ex:
                    print(f"Ignoring cookie '{cookie}' due to InvalidCookieDomainException: {str(ex)}")
                    continue
    driver.refresh()
    return

def clickCookie(num):
    cookie_to_click = wait10.until(EC.element_to_be_clickable((By.ID, 'bigCookie')))
    for _ in range(num):
        cookie_to_click.click()
    return 

def clickLanguage():
    try:
        language = driver.find_element(By.ID, 'langSelect-EN')
        language.click()
        return True
    except:
        return False

def getNumCookies():
    num_cookies_title =  wait10.until(EC.element_to_be_clickable((By.ID, 'cookies')))
    num_cookies = int(re.findall(r'\d+', num_cookies_title.text)[0])
    return num_cookies

def buyCursor(num):
    buy_cursor = driver.find_element(By.ID, 'product0')
    for _ in range(num):
        buy_cursor.click()
    return

def priceCursor():
    click_price = driver.find_element(By.ID, 'productPrice0')
    click_price_int = int(click_price.text)
    return click_price_int

def buyGrandma(num):
    buy_grandma = driver.find_element(By.ID, 'product1')
    for _ in range(num):
        buy_grandma.click()
    return

def priceGrandma():
    grandma_price = driver.find_element(By.ID, 'productPrice1')
    grandma_price_int = int(grandma_price.text) 
    return grandma_price_int

def buyUpgrade():
    next_upgrade = wait2.until(EC.element_to_be_clickable((By.ID, 'upgrade0')))
    class_attribute = next_upgrade.get_attribute("class")
    if "enabled" in class_attribute.split():
        next_upgrade.click()
        return True
    return False

def startGame():
    driver.get('https://orteil.dashnet.org/cookieclicker/')
    if not clickLanguage():
        time.sleep(3)
        if not clickLanguage():
            raise AssertionError

    time.sleep(1)
    clickCookie(30)
    buyCursor(1)
    return


def downloadSaveFile():
    optionTab = wait2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#prefsButton > div')))
    optionTab.click()
    time.sleep(10)
    saveGame = wait2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div > div > div:nth-child(5) > a:nth-child(1)')))
    saveGame.click()
    return


startGame()
time.sleep(5)
downloadSaveFile()

time.sleep(520)
driver.quit()