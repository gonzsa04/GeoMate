#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
serv = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
prefs = {'profile.default_content_setting_values': {'images':2}}

options.add_experimental_option('prefs', prefs)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"

driver = webdriver.Chrome(options = options, service=serv)
driver.minimize_window()

'''if os.path.exists("outPut.txt"):
  os.remove("outPut.txt")
fichero = open('outPut.txt', 'a',  encoding="UTF-8")'''

if os.path.exists("outPut.csv"):
  os.remove("outPut.csv")
fichero = open('outPut.csv', 'w',  encoding="UTF-8", newline='')

with open('Geolocalizacion-automatica.csv', encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    writer = csv.writer(fichero, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    Url_With_Coordinates = []
    i = 0
    j = 0
    for row in csv_reader:
        row[0] = row[0].lower()
        row[0] = row[0].replace(' ', '+')
        row[0] = row[0].replace('.', '+')
        row[0] = row[0].replace('\'', '')
        row[0] = row[0].replace('º', '+')
        row[0] = row[0].replace('ª', '+')
        row[0] = row[0].replace('á', 'a')
        row[0] = row[0].replace('é', 'e')
        row[0] = row[0].replace('í', 'i')
        row[0] = row[0].replace('ó', 'o')
        row[0] = row[0].replace('ú', 'u')
        row[0] = row[0].replace('ç', 'c')
        row[0] = row[0].replace("s/n", '')
        row[0] = row[0].replace('++', '+')

        driver.get("https://www.google.es/maps/place/"+row[0])

        if i < 1: 
            #driver.find_element(By.CSS_SELECTOR, "Acepto").click()VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc
            driver.execute_script("document.getElementsByClassName('VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc')[3].click()")
            #time.sleep(10)

        Url_With_Coordinates.append(driver.find_element(By.CSS_SELECTOR, 'meta[itemprop=image]').get_attribute('content'))

        row = []
        url = ''
        latitud = ''
        longitud = ''
        problems = ''

        try:
            latitud, longitud = Url_With_Coordinates[i][Url_With_Coordinates[i].rfind('=') + 1:-1].split(',')
            url = driver.current_url
        
        except:
            try:
                latitud, longitud = Url_With_Coordinates[i].split('?center=')[1].split('&zoom=')[0].split('%2C')
                url = driver.current_url
            except:
                try:
                    url = driver.current_url
                    time.sleep(10)
                    latitud, longitud, a = driver.current_url[driver.current_url.find('@') + 1: driver.current_url.find("z/data")].split(',')
                except:
                    url = driver.current_url
                    problems = 'Hubo problemas con esta direccion'
                    j+=1
        
        if problems != '':
            latitud = 1
            longitud = 1

        writer.writerow([url, latitud, longitud])

        os.system('cls')
        print(str(i) + '\n' + driver.current_url)
        
        i+=1

        #if i > 1: break

    print('\n' + 'numero de errores: ' + str(j))
    
driver.close()
driver.quit()