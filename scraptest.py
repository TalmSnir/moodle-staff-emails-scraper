from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import re
import csv

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])


driver = webdriver.Chrome(
    'staff_emails_scraper\chromedriver.exe', options=chrome_options)

driver.maximize_window()


driver.get('https://nidp.tau.ac.il/nidp/saml2/sso?SAMLRequest=jZJfS8MwFMW%2FSsl7%2F6Xd5kJXmA5xMHVs1QdfJE3uXKBNam4q%2Bu1tuw0nwvAxN%2Ff87rmHmyGvq4bNW7fXG3hvAZ33WVca2fAxI63VzHBUyDSvAZkTbDu%2FXzEaRKyxxhlhKnImuazgiGCdMpp4y8WMvCaSjkEmk6icUiHT5IpLSGWcjscjgHKykymUopQwKon3DBY75Yx0oE6O2MJSo%2BPadaWIxn6U%2BHFcxFNGY0bpC%2FEW3TZKczeo9s41yMJQK9kEjrcBF4GqhmfYG6choiHe%2FOTwxmhsa7BbsB9KwNNm9cOojZEVnFF4l9%2BJcsT5XGDQ7Js%2FzcRbH3O7Vloq%2FXY5svLQhOyuKNb%2B%2BnFbkDzrJ7AhApv%2F01QNjkvueO8pC88B2eEGHrrRy8XaVEp8ebfG1txddtZXlPR3QytzlmtUoB0J8wP%2F91nl3w%3D%3D&RelayState=https%3A%2F%2Fmoodle.tau.ac.il%2Fauth%2Fsaml2%2Flogin.php&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=esiUUwcwgw%2Fz0k4Z4diYKohoOyG5jxDyHW1MUrZ2%2BTDEm8Qi4nOku0cXDa7AWeEfh8cRIUnTGzqO4XS0cG4BHD5X9KMNfLUdCFSfWu7FW7JAgEbpAgVq6N%2F8J5MFMQwPZRqaxUXYQrpfovFcFOkDwetQNLPG4YH44RKxklMQ%2B0pRlEsQVTguYqXQ5AsgFmlOq7mrqD2%2BLuKeYJe1MbqMfSMOrwvJQqe8GFffd9nqExWRcI8gYDopZdCoAE5xsoqhPWACa3%2By%2FA2aZjmWH9MhjaLhKfZic3cSpbCdUj88Yx2vbZjVp4Y5Esp4rOo4ng95tLyso4dZ%2FHrJGDX5wGibsQ%3D%3D')

WebDriverWait(driver, 20).until(
    EC.frame_to_be_available_and_switch_to_it((By.ID, 'content')))

WebDriverWait(driver, 20).until(
    EC.frame_to_be_available_and_switch_to_it((By.ID, 'credentials')))

# *enter your login info and remove the comments
# username =
# user_id =
# user_password =


user_name_box = driver.find_element_by_name('Ecom_User_ID')
user_name_box.send_keys(username)


user_id_box = driver.find_element_by_name('Ecom_User_Pid')
user_id_box.send_keys(user_id)

user_password_box = driver.find_element_by_name('Ecom_Password')
user_password_box.send_keys(user_password)

login_btn = driver.find_element_by_class_name('subBottun')
login_btn.click()
driver.switch_to.default_content()

WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.LINK_TEXT, ('התחבר/י')))).click()

driver.find_element_by_class_name('btn-primary').click()
WebDriverWait(driver, 5)
courses_list = driver.find_elements_by_class_name(
    'dashboard-card')
main_win = driver.window_handles[0]
for course in courses_list:
    # !there is a problem with moving between courses
    course_page = course.find_element_by_tag_name('a').click()
    WebDriverWait(driver, 5)
    teachers_list = driver.find_element_by_class_name(
        'teachers_list').find_elements_by_tag_name('a')

    for teacher in teachers_list:

        teacher.click()

        course_win = driver.window_handles[0]

        win_new = driver.window_handles[1]
        driver.switch_to_window(win_new)

        teacher_name = driver.find_element_by_tag_name('h1').text
        print(teacher_name)
        teacher_email_a = driver.find_element_by_class_name("contact-item").find_element_by_tag_name(
            'a')
        teacher_email_address = re.findall(
            '[^:]+@+\S+', teacher_email_a.get_attribute("href"))
        print(teacher_email_address)
        driver.close()
        driver.switch_to_window(course_win)
    driver.switch_to_window(main_win)


driver.quit()
