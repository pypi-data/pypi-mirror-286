import logging
from selenium.webdriver.common.by import By
import time
import vision

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Định nghĩa các giá trị hợp lệ cho action_style
ACTION_STYLE_SIGN_UP = 'sign up'
ACTION_STYLE_SIGN_IN_MAVIS_ID_SDK = 'sign in mavis id sdk'
ACTION_STYLE_SIGN_IN_DASHBOARD = 'sign in dashboard'

VALID_ACTION_STYLES = [
    ACTION_STYLE_SIGN_UP,
    ACTION_STYLE_SIGN_IN_MAVIS_ID_SDK,
    ACTION_STYLE_SIGN_IN_DASHBOARD
]

err_msg_xpath = '//div[@class="axie-captcha-error-message"]'
confirm_btn_xpath = '//button[text()="Confirm"]'
rotate_left_btn_xpath = '//button[@class="axie-captcha-rotate-button axie-captcha-rotate-left-button"]'
rotate_right_btn_xpath = '//button[@class="axie-captcha-rotate-button axie-captcha-rotate-right-button"]'
sign_up_xpath = '//h1[text()="Verify to continue"]'
sign_in_mavis_id_sdk_xpath = '//div[text()="Enter your recovery password"]'
sign_in_mavis_dashboard_xpath = '//img[@alt="Sky Mavis Logo"]'

def check_captcha(driver, action_style):
    try:
        time.sleep(1)
        driver.find_element(By.XPATH, err_msg_xpath)
        logging.error("Failed to orient the captcha correctly.")
        return False
    except Exception:
        try:
            next_msg = ''
            if action_style == ACTION_STYLE_SIGN_UP:
                next_msg = sign_up_xpath
            elif action_style == ACTION_STYLE_SIGN_IN_MAVIS_ID_SDK:
                next_msg = sign_in_mavis_id_sdk_xpath
            elif action_style == ACTION_STYLE_SIGN_IN_DASHBOARD:
                next_msg = sign_in_mavis_dashboard_xpath      
            time.sleep(2)
            driver.find_element(By.XPATH, next_msg)
            return True
        except Exception as e:
            logging.error(f"Error in check_captcha: {str(e)}")
            return False

def bypass_captcha(driver, wrapper_image, action_style):
    if action_style not in VALID_ACTION_STYLES:
        logging.error(f"Invalid action_style: {action_style}. Valid options are: {', '.join(VALID_ACTION_STYLES)}")
        return False
    
    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        attempt += 1
        logging.info(f"Attempt {attempt}/{max_attempts}")
        count = 0
        for _ in range(13): 
            count += 1
            image = vision.capture_image(wrapper_image, count)
            if count == 1:
                check_color_left = vision.determine_more_colorful_left_right(image)
            if vision.is_correct_orientation(image, count):
                logging.info("Captcha is correctly oriented.")
                logging.info("Checking...")
                driver.find_element(By.XPATH, confirm_btn_xpath).click()
                if check_captcha(driver, action_style):
                    logging.info("Captcha bypassed successfully.")
                    return True
                else:
                    logging.info("Captcha bypass failed.")
                    break  # Lặp lại vòng lặp trong trường hợp captcha không đúng
            else:
                if check_color_left:
                    driver.find_element(By.XPATH, rotate_left_btn_xpath).click()
                else:
                    driver.find_element(By.XPATH, rotate_right_btn_xpath).click()
        if attempt < max_attempts:
            logging.info("Retrying...")
        else:
            logging.error("Maximum attempts reached. Captcha bypass failed.")
            return False
