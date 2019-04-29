from selenium import webdriver
from selenium.webdriver.support.ui import Select
from urllib.request import urlopen
import json
import time

class tests:
    def __init__(self,gnt_url,getad_url):
        #global driver
        self.gnt_url=gnt_url
        self.getad_url=getad_url



    # def create_new_camp_from_gui(self):
    #     driver.get(self.gui_url)
    #     driver.maximize_window()
    #     driver.find_element_by_id("textfield1").send_keys(self.gui_user_name)
    #     driver.find_element_by_id("textfield4").send_keys(self.password)
    #     driver.find_element_by_id("target").click()
    #     driver.find_element_by_id("btnNewCampaign").click()
    #     select =Select(driver.find_element_by_css_selector("[ng-model^=PlatformType]"))
    #     select.select_by_value('Desktop')
    #     driver.find_element_by_xpath("//*[contains(text(), 'Bidding')]").click()
    #     driver.find_element_by_xpath("//*[contains(text(), 'Choose Product')]").click()
    #     driver.find_element_by_xpath("//*[contains(text(), 'eRoll')]").click()

    def check_get_ad(self):
        get_ad_works=False
        for i in range (0,35):
            time.sleep(5)
            response = urlopen(self.getad_url)
            string = response.read().decode('utf-8')
            if "Ad id=" not in string:
                print ("Get-Ad is not have Campaign inside- trying again ")
                continue
            else:
                get_ad_works=True
                print ("Get-Ad works!")
                break
        return get_ad_works


    def check_gnt(self):
        gnt_works=False
        for i in range (0,35):
            time.sleep(5)
            response = urlopen(self.gnt_url)
            string = response.read().decode('utf-8')
            if "Sucsess" not in string:
                print ("GNT is not have Campaign inside- trying again ")
                continue
            else:
                gnt_works=True
                print ("GNT works!")
                break
        return gnt_works




# liron=tests('http://staging3.advsnx.net/index.html','http://staging3.advsnx.net/asa/admin/login.aspx','bobo123','Admin1','tmf','C:\\chromedriver.exe')
# liron.check_get_ad()
# liron.check_gnt()
# liron.create_new_camp_from_gui()




