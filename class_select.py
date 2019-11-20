from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import time
from argparse import ArgumentParser
import yaml
from datetime import datetime, timedelta, timezone

def wait_for_page_change(driver, contains):
    while contains not in driver.title:
        time.sleep(0.001)

def main():
    case_id = ""
    password = ""
    days_from_now = 0
    hour = 0
    minute = 0

    # how many minutes before desired time to log into SIS.
    # not sure how long the timeout is but be careful
    login_offset = 3

    with open("config.yaml", 'r') as stream:
        try:
            content = yaml.safe_load(stream)
            # print(content)
            case_id = content["id"]
            password = content["password"]
            hour = content["hour"]
            minute = content["minute"]
            days_from_now = content["days_from_now"]
        except yaml.YAMLError as e:
            print(e)
            exit()
        except FileNotFoundError as e:
            print("config.yaml not found")
            exit()

    send_time = datetime.now()
    send_time = send_time.replace(day=send_time.day+days_from_now, hour=hour, minute=minute,second=0, microsecond=100)
    # print(send_time)
    enter_time = send_time - timedelta(minutes=login_offset)
    print("Waiting until {} to enter portal (5 minutes before {}).".format(enter_time, send_time))

    while datetime.now() < enter_time:
        continue

    driver = webdriver.Chrome()
    try:
        driver.get("https://sis.case.edu/psp/P92SCWR/?cmd=login&languageCd=ENG&")

        wait_for_page_change(driver, "CWRU Student")

        elem = driver.find_element_by_id("userid")
        elem.clear()
        elem.send_keys(case_id)

        elem = driver.find_element_by_id("pwd")
        elem.clear()
        elem.send_keys(password)

        elem = driver.find_element_by_name("Sign in")
        elem.click()

        wait_for_page_change(driver, "My Homepage")


        elem = driver.find_element_by_id("win0groupletPTNUI_LAND_REC_GROUPLET$2")
        elem.click()

        wait_for_page_change(driver, "Class Search")

        elem = driver.find_element_by_id("SCC_LO_FL_WRK_SCC_VIEW_BTN$3")
        elem.click()

        wait_for_page_change(driver, "Shopping Cart")

        radio_select = driver.find_elements_by_class_name("ps-checkbox")
        for i in radio_select:
            i.click()

        elem = driver.find_element_by_id("DERIVED_SSR_FL_SSR_ENROLL_FL")
        elem.click()

        time.sleep(0.5)

        elem = driver.find_element_by_id("#ICYes")

        delta = send_time - datetime.now()
        print("Waiting for {} seconds".format(delta.seconds))
        while datetime.now()<send_time:
            continue
        
        elem.click() # pray to god

        print("Pressed enroll, good look!")
    finally:
        time.sleep(60)
        driver.close()

if __name__ == "__main__":
    main()
