from selenium import * 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import *
import time 

def switch_emp_dir():
    driver = login()

    try:
        print("Navigating to Employee Directory")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'v-navigation-drawer'))
        )

        navigation_drawers = driver.find_elements(By.CLASS_NAME, 'v-navigation-drawer')

        for drawer in navigation_drawers:
            try:
                employee_dir_link = drawer.find_element(By.CSS_SELECTOR, 'a[href="/user/employee-directory"]')
                employee_dir_link.click()
                time.sleep(5)
                print("Navigated to Employee Directory successfully")
            
                break  
            except:
                continue
        return driver

    except Exception as e:
        print(f"Error occurred while switching organization: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()          
if __name__ == "__main__":
    switch_emp_dir()
