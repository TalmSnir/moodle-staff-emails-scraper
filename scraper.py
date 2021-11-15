from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re
import csv

# !uncomment the line below and line 104 to enable writing to google drive sheet
# import sheet

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
driver = webdriver.Chrome(
    'chromedriver.exe', options=chrome_options)
driver.maximize_window()


def navigating_to_login_page(driver):
    """[navigate to the main login page, switches the driver to the iframe of the login section]""

    Args:
        driver ([WebElement])
    """
    driver.get('https://nidp.tau.ac.il/nidp/saml2/sso?SAMLRequest=jZJfS8MwFMW%2FSsl7%2F6Xd5kJXmA5xMHVs1QdfJE3uXKBNam4q%2Bu1tuw0nwvAxN%2Ff87rmHmyGvq4bNW7fXG3hvAZ33WVca2fAxI63VzHBUyDSvAZkTbDu%2FXzEaRKyxxhlhKnImuazgiGCdMpp4y8WMvCaSjkEmk6icUiHT5IpLSGWcjscjgHKykymUopQwKon3DBY75Yx0oE6O2MJSo%2BPadaWIxn6U%2BHFcxFNGY0bpC%2FEW3TZKczeo9s41yMJQK9kEjrcBF4GqhmfYG6choiHe%2FOTwxmhsa7BbsB9KwNNm9cOojZEVnFF4l9%2BJcsT5XGDQ7Js%2FzcRbH3O7Vloq%2FXY5svLQhOyuKNb%2B%2BnFbkDzrJ7AhApv%2F01QNjkvueO8pC88B2eEGHrrRy8XaVEp8ebfG1txddtZXlPR3QytzlmtUoB0J8wP%2F91nl3w%3D%3D&RelayState=https%3A%2F%2Fmoodle.tau.ac.il%2Fauth%2Fsaml2%2Flogin.php&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=esiUUwcwgw%2Fz0k4Z4diYKohoOyG5jxDyHW1MUrZ2%2BTDEm8Qi4nOku0cXDa7AWeEfh8cRIUnTGzqO4XS0cG4BHD5X9KMNfLUdCFSfWu7FW7JAgEbpAgVq6N%2F8J5MFMQwPZRqaxUXYQrpfovFcFOkDwetQNLPG4YH44RKxklMQ%2B0pRlEsQVTguYqXQ5AsgFmlOq7mrqD2%2BLuKeYJe1MbqMfSMOrwvJQqe8GFffd9nqExWRcI8gYDopZdCoAE5xsoqhPWACa3%2By%2FA2aZjmWH9MhjaLhKfZic3cSpbCdUj88Yx2vbZjVp4Y5Esp4rOo4ng95tLyso4dZ%2FHrJGDX5wGibsQ%3D%3D')

    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, 'content')))

    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, 'credentials')))


def user_login(driver, username, user_id, user_password):
    """[input the credentials of the user to the login form and navigate through two more follow up pages to the main moodle page]""

    Args:
        driver ([WebElement]) 
        username,user_id,user_password ([string]):credentials for the user login
    """
    user_name_box = driver.find_element_by_name('Ecom_User_ID')
    user_name_box.send_keys(username)

    user_id_box = driver.find_element_by_name('Ecom_User_Pid')
    user_id_box.send_keys(user_id)

    user_password_box = driver.find_element_by_name('Ecom_Password')
    user_password_box.send_keys(user_password)

    login_btn = driver.find_element_by_class_name('subBottun')
    login_btn.click()

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.LINK_TEXT, ('התחבר/י')))).click()

    driver.find_element_by_class_name('btn-primary').click()


def course_scraper(driver):
    """[scrape the visible courses in the moodle of the user and write to a csv file the staff's names and emails]""

    Args:
        driver ([WebElement]) 
    """

    driver.implicitly_wait(20)
    courses_list = driver.find_elements_by_class_name(
        'visible-course-card')

    with open('staff_database.csv', 'a', newline='', encoding='utf-8-sig') as database:
        writer = csv.writer(database)
        writer.writerow(['staff member', 'email'])
        for i in range(3, len(courses_list)+1):

            driver.implicitly_wait(20)

            driver.find_element_by_xpath(
                f'//*[@id="page-container-1"]/div/div/div[{i}]/a').click()

            driver.implicitly_wait(10)
            teachers_list = driver.find_element_by_class_name(
                'teachers_list').find_elements_by_tag_name('a')

            for teacher in teachers_list:
                teacher.click()

                course_win = driver.window_handles[0]

                win_new = driver.window_handles[1]
                driver.switch_to_window(win_new)

                teacher_name = driver.find_element_by_tag_name('h1').text

                teacher_email_a = driver.find_element_by_class_name("contact-item").find_element_by_tag_name(
                    'a')
                teacher_email_address = re.findall(
                    '[^:]+@+\S+', teacher_email_a.get_attribute("href"))
                writer.writerow([teacher_name, teacher_email_address[0]])

                #! uncomment the line below and change the sheet.py at the  correct places to write the data to google drive sheet
                # sheet.write_to_sheet(teacher_name, teacher_email_address[0])

                driver.close()
                driver.switch_to_window(course_win)
            driver.back()


# *enter your login info and remove the comments
username = 'your_Moodle_username' 
user_id = 'your_Moodle_id'
user_password = 'your_Moodle_password'

navigating_to_login_page(driver)
driver.implicitly_wait(5)
user_login(driver, username, user_id, user_password)
driver.implicitly_wait(5)
course_scraper(driver)

driver.quit()
