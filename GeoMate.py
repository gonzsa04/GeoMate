#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

options = Options()
serv = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
prefs = {'profile.default_content_setting_values': {'images':2}}

options.add_experimental_option('prefs', prefs)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"

driver = webdriver.Chrome(options = options, service=serv)
driver.maximize_window()

'''if os.path.exists("outPut.txt"):
  os.remove("outPut.txt")
fichero = open('outPut.txt', 'a',  encoding="UTF-8")'''

if os.path.exists("outPut.csv"):
  os.remove("outPut.csv")
fichero = open('outPut.csv', 'w',  encoding="UTF-8", newline='')

with open('csv_latitud_longitud_null.csv', encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    writer = csv.writer(fichero, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    Url_With_Coordinates = []
    i = 0
    errors = 0
    firstTime = True

    ogLatitud = '1000.0'
    ogLongitud = '1000.0'

    for row in csv_reader:
        if i < 1:
            firstRow = [row[1],row[2],"GO_latitud__c", "GO_longitud__c"]
        else:
            row[2] = row[2].lower()
            row[2] = row[2].replace(' ', '+')
            row[2] = row[2].replace('.', '+')
            row[2] = row[2].replace(',', '+')
            row[2] = row[2].replace('\'', '')
            row[2] = row[2].replace('º', '+')
            row[2] = row[2].replace('ª', '+')
            row[2] = row[2].replace('á', 'a')
            row[2] = row[2].replace('é', 'e')
            row[2] = row[2].replace('í', 'i')
            row[2] = row[2].replace('ó', 'o')
            row[2] = row[2].replace('ú', 'u')
            row[2] = row[2].replace('ç', 'c')
            row[2] = row[2].replace("s/n", '')
            row[2] = row[2].replace('++', '+')


            if firstTime: 
                #driver.find_element(By.CSS_SELECTOR, "Acepto").click()VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc
                driver.get("https://www.google.es/maps/place/")
                driver.execute_script("document.getElementsByClassName('VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc')[3].click()")
                firstTime = False

                time.sleep(5)
                
                content = driver.find_element(By.XPATH, "//meta[@itemprop='image']").get_attribute('content')
                ogLatitud, ogLongitud = latitud, longitud = content.split('?center=')[1].split('&zoom=')[0].split('%2C')
                
            driver.get("https://www.google.es/maps/place/"+row[2])

            latitud = '0.0'
            longitud = '0.0'
            problems = False
            
            try:
                if row[2] != '':
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "searchbox-searchbutton")))
                    element.click()

                    time.sleep(3)

                    driver.get(driver.current_url)

                    content = driver.find_element(By.XPATH, "//meta[@itemprop='image']").get_attribute('content')
                    print(content)
                    latitud, longitud = content[content.rfind('=') + 1:-1].split(',')

            except:        
                try:
                    latitud, longitud = content.split('?center=')[1].split('&zoom=')[0].split('%2C')
                except:
                    problems = True
                    errors+=1

            try:
                if (latitud == '0.0' and longitud == '0.0' and row[2] != '') or problems:
                    latitud, longitud, a = driver.current_url[driver.current_url.find('@') + 1: driver.current_url.find("y/data")].split(',')  
                    if problems:
                        problems = False
                        errors-=1
            except:
                if problems == False:
                    problems = True
                    errors+=1

            if problems:
                latitud = '1.0'
                longitud = '1.0'
                print('Error in url: ' + driver.current_url)
            else:
                if latitud == ogLatitud and longitud == ogLongitud:
                    latitud = '0.0'
                    longitud = '0.0'

        if i < 1:
            outRow = firstRow
        else:
            outRow = [row[1],driver.current_url, latitud, longitud]

        writer.writerow(outRow)

        #os.system('cls')
        print(str(i) + '\n' + str(outRow[1:]))
        
        i+=1

        #if i > 20: break

    print('\n' + 'numero de errores: ' + str(errors))
    
#driver.close()
#driver.quit()