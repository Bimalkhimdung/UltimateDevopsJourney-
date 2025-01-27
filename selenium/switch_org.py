from selenium import * 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login.login import login
import time 

def switch_org():
    driver = login()
    try:
        print("Switching org")

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.v-toolbar__content'))
        )
        dots_button = driver.find_element(By.CSS_SELECTOR, 'i.v-icon.notranslate.mdi.mdi-dots-vertical.theme--dark') 
        print(f"Button HTML: {dots_button.get_attribute('outerHTML')} Clicked Successfully")
              
        dots_button.click()
        time.sleep(5)
    except Exception as e:
        print(f"Error as {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    switch_org()

