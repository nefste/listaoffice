# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 16:54:37 2024

@author: StephanNef
"""


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time
import os
import shutil

# Funktion zum Kopieren und Umbenennen des fallback Bildes
def copy_and_rename_fallback_image(original_image_path, new_image_path):
    try:
        shutil.copy(original_image_path, new_image_path)
        print(f"Bild wurde erfolgreich als {new_image_path} gespeichert.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten beim Kopieren des Bildes: {e}")

# Funktion, die überprüft, ob ein Screenshot gemacht werden soll, und ihn macht
def attempt_screenshot(driver, produktname, url):
    screenshot_path = f"{produktname}.png"
    if not os.path.exists(screenshot_path):
        driver.get(url)
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//canvas[@data-engine="Babylon.js v6.19.1"]')))
            time.sleep(1.5)  # Kurze Pause, um sicherzustellen, dass das Canvas vollständig geladen ist
            driver.save_screenshot(screenshot_path)  # Speichere den Screenshot direkt mit Selenium
            print(f"Screenshot erfolgreich gespeichert: {screenshot_path}")
        except Exception as e:
            print(f"Screenshot fehlgeschlagen für: {screenshot_path}, {e}")
            copy_and_rename_fallback_image("logo.jpg", screenshot_path)
    else:
        print(f"Screenshot existiert bereits: {screenshot_path}")

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

df = pd.read_excel("data.xlsx")

if 'Preis' not in df.columns:
    df['Preis'] = None

df['Klasse'] = None

def update_dataframe(row):
    if pd.isnull(row['Preis']):
        # Hier wird jetzt nur attempt_screenshot aufgerufen, da die URL bereits besucht wird
        attempt_screenshot(driver, row['Produktname'], row['Link'])
    return row

df = df.apply(update_dataframe, axis=1)

df.to_excel('aktualisierte_data.xlsx', index=False)

driver.quit()

print(df)
