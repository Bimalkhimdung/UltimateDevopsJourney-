from selenium import * 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import *
from switch_emp_directory import * 
import time 

def select_user_name():
    driver = None 
    retries = 1
    for tries in range(retries):
        try:            
            driver = switch_emp_dir()
    
            if not driver:
                print("Login failed. Cannot select user name.")
                return    
            print("Selecting user name")
    
            # Wait for the v-card_text div to be present
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'div.v-card__text'))
            )
    
            user_name_element = driver.find_element(By.CSS_SELECTOR, 'div.v-card__text a.text-h6')
    
            user_name = user_name_element.text
            print(f"User Name: {user_name}")
    
            user_name_element.click()
            time.sleep(5)
            break
        except Exception as e:
            print(f"Attempt {tries + 1 } failed: {e}")
            if driver:
                driver.quit()
            if tries == retries -1:
                print("Max retires reached. Exiting")
                raise
            time.sleep(5)
        except Exception as e:
            print(f"Error occurred while selecting user name: {e}")
            import traceback
            traceback.print_exc() 
            if driver:
                driver.quit()
            break    
        finally:
            if driver and tries == retries - 1:
                driver.quit()
    
if __name__ == "__main__":
    select_user_name()