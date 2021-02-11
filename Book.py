import datetime
import time
import argparse
import pytz
import credentials

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from dateutil import tz
from InverseExponentialBackoff import IEB

parent_url = "https://ubc.perfectmind.com/"
my_username = credentials.MY_USERNAME
my_password = credentials.MY_PASSWORD

# Full XML paths to elements
perfectmind_login = "/html/body/div[1]/div[6]/div/div/div/div[2]/div/div[1]/div/div[1]/p[4]/a"
register_now_button = "/html/body/div[4]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[4]/a"
arc_button = "/html/body/div[2]/div[2]/div/div/div[1]/div[4]/div[3]/div[1]/div/ul/li[1]/a"
list_of_classes = "//*[@id='classes']"
list_of_classes_elements = ".//input[@class='bm-button bm-class-details bm-details-button']"
register_button = "/html/body/div[2]/div[2]/div/div/div/div[1]/div/section[2]/a"

def is_skipday_weekday():
    return (datetime.date.today() + datetime.timedelta(days=2)).weekday() < 5

def is_tomorrow_weekday():
    return (datetime.date.today() + datetime.timedelta(days=1)).weekday() < 5

def is_today_weekday():
    return datetime.datetime.today().weekday() < 5

def get_offset(time_slot):
    offset = 0
    offset += 5 if is_today_weekday() else 4
    offset += 9 if is_tomorrow_weekday() else 6
    offset += time_slot
    return offset

def book(time_slot):
    # selenium.webdriver.Chrome instance is destructed during garb collection process. 
    # Initializing it as a global var prevents this instance from being GC'd
    global driver 
    ieb = IEB(datetime.time(12,0,0)) # Set end time to 12PM PST
    driver = webdriver.Chrome('./chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get(parent_url)
    driver.maximize_window()
    driver.find_element_by_xpath(perfectmind_login).click()
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(my_username)
    password.send_keys(my_password)
    driver.find_element_by_name("_eventId_proceed").click()
    wait = WebDriverWait(driver, 120)
    wait.until(ec.visibility_of_element_located((By.XPATH, register_now_button))).click()
    wait.until(ec.visibility_of_element_located((By.XPATH, arc_button))).click()
    offset = get_offset(time_slot)
    print("offset: " + str(offset))
    classes = wait.until(ec.visibility_of_element_located((By.XPATH, list_of_classes)))
    time_slots = classes.find_elements_by_xpath(list_of_classes_elements)
    time_slots[offset].click()

    while True:
        try:
            # Wait for element, then start IEB
            driver.find_element_by_xpath(register_button).click()
            break
        except Exception:
            ieb.next()
            driver.refresh()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Select a time slot')
    parser.add_argument('--slot', metavar='N', type=int, required=True)
    args = parser.parse_args()
    print(args.slot)
    book(args.slot)