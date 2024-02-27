import os
import time
from datetime import datetime, timedelta

import pandas as pd
from rich import inspect, print
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

#!: CONFIG!
excelname="xxxx.xlsx"
sheetname="Sheet1"
id=""
pasw=""
url = ""
url2=""
#------------------------------------------------------------------------

driver = webdriver.Chrome()
driver.maximize_window()

def accept_alert():                                              #use this just to accept the alert shown
    try:
        temp=WebDriverWait(driver, 10).until(EC.alert_is_present())
    except:
        driver.quit()
    else:
        driver.switch_to.alert.accept()

def login():
    driver.get(url)
    accept_alert()
    user = driver.find_element(By.NAME,"mb_id")
    user.clear()
    user.send_keys(id)
    pas = driver.find_element(By.NAME,"mb_password")
    pas.clear()
    pas.send_keys(pasw)
    btn = driver.find_element(By.CLASS_NAME, "btn-e")
    btn.click()
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'sidebar-left-nav')))
        return(True)
    except Exception as e:
        print("An error occurred:", e)

def fill_data():
    print("Total data: "+str(len(data)))
    stot=0
    ftot=0
    for d in data:                                                   #loop through all datas read from Excel
        driver.get(url2)
        klas_utama=d[0]
        kode=d[2]
        origin=d[5]
        desc_1=d[7]
        kelompok=d[9]
        image1=os.path.abspath(str(d[10]))
        
        '''
        Sample of data structure in the dropdown element:
           Option A
                Option A1
                Option A2
                    Option A2x
                    Option A2y
                Option A3
           Option B
           Option C
        '''
        #NOTE: set data in element that has options like dropdown.
        try:
            kls_utama=Select(driver.find_element(By.NAME,"ca_id"))
            
            options=kls_utama.options
            for x in options:
                tmp=x.text.strip()                                    #strip the option because it might have 'tabs' or 'empty spaces' prefix.
                if klas_utama in tmp:
                    kls_utama.select_by_visible_text(x.text)          #MUST use the original visible text from the option
            
            kel=Select(driver.find_element(By.NAME,"it_info_gubun"))  #another example of dropdown element, but this one is simpler, there is no sub-category
            kel.select_by_visible_text(kelompok)
            
            #for elemet type: text input field
            tmp=driver.find_element(By.NAME,"it_id")
            tmp.clear()                                              #MUST clear first if has default value
            tmp.send_keys(kode)   
            
            if origin!=None:                                         #we can use this None cause all NaN already changed to it.
                tmp=driver.find_element(By.NAME,"it_origin")
                tmp.send_keys(origin)
                
            #for element type: file uploader 
            tmp=driver.find_element(By.NAME,"it_img1")               
            tmp.send_keys(image1)
        
        '''
            the rich text area element's structure:
            main website
                 |
                  iFrame(0)
                  	|
                     iFrame rich text area
                     other elements    
                  other elements....
                  iFrame(1)
                  	|
                     iFrame rich text area
                     other elements
                  other elements....
				  elemt(2)
				  other elements...
				  submit button

        '''
        #NOTE: set data in richtext
            driver.switch_to.frame(0)                                                 #go to 1st iframe's URL
            board=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            driver.switch_to.frame(board)
            txtarea=driver.find_element(By.TAG_NAME, "body")
            txtarea.send_keys(desc_1)
            driver.switch_to.default_content()                                        #get back to main structure,  don't forget to use it!
            
            driver.switch_to.frame(1)                                                 #go to 2nd iframe's URL
            board=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            driver.switch_to.frame(board)
            txtarea=driver.find_element(By.TAG_NAME, "body")
            txtarea.send_keys(desc_1)
            driver.switch_to.default_content()

        except Exception as e:
            print("An error occurred", e)

        #NOTE: submit
        try:
            btn=driver.find_element(By.XPATH,"//input[@type='submit' and @value='Konfirmasi' and @class='btn-e btn-e-lg btn-e-red']")
            ActionChains(driver).move_to_element(btn).perform()
            btn.click()
        except Exception as e:
                print("An error occurred:", e)
        else:                                                                        #use this, if there is possibilities more than 1 kind of alert
            try:
                alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert_text=alert.text                                               
                if "?" in alert_text.lower():
                    print(str(kode)+" Added")
                    stot=stot+1
                else:
                    print(str(kode)+" Failed!")
                    ftot=ftot+1
                alert.dismiss()
            except TimeoutException:
                print("No alert appeared within the specified time.")
    return(stot,ftot)
        
def openfile():
    try:
        df = pd.read_excel(os.path.abspath(excelname), sheet_name=sheetname , header=None, skiprows=1)   #read excel file by skip 1st row
    except Exception as e:
        print("An error occurred while reading the Excel file:", e)
    else:
        df = df.map(lambda x: None if pd.isna(x) else x)                                                 #to make data NaN in excel field to be None
        data = [tuple(row) for row in df.values]
        return(data)

if login():
    try:        
        data=openfile()
        stot,ftot=fill_data()
        print("Success: "+str(stot))
        print("Failed: "+str(ftot))
        time.sleep(1)
        driver.close()
    except Exception as e:
        print("An error occurred:", e)
    
