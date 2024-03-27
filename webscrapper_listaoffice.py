# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 12:36:45 2024

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

import shutil

# Funktion zum Kopieren und Umbenennen des Bildes, wenn das Erstellen eines Screenshots fehlschlägt
def copy_and_rename_fallback_image(original_image_path, new_image_name):
    try:
        # Ziel-Pfad für das neue Bild, einschließlich der neuen Erweiterung
        new_image_path = f"{new_image_name}.png"
        
        # Kopiere und benenne das Originalbild um
        shutil.copy(original_image_path, new_image_path)
        
        print(f"Bild wurde erfolgreich als {new_image_path} gespeichert.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten beim Kopieren des Bildes: {e}")

# Initialisiere den WebDriver
options = webdriver.ChromeOptions()
options.headless = True  # Füge diese Zeile hinzu, wenn du den Browser im Hintergrund laufen lassen möchtest
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Daten einlesen
df = pd.read_excel("data.xlsx")

# Überprüfe, ob die "Preis"-Spalte existiert, füge sie hinzu, falls nicht
if 'Preis' not in df.columns:
    df['Preis'] = None


def update_dataframe(row):
    if pd.isnull(row['Klasse']):# Prüfe, ob der Preis fehlt
        url = row['Link']
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)  # Warte, bis die Seite geladen ist
        
        # Preis aktualisieren
        try:
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe.pcon-iframe")))
            price_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "egr_footer_price_value")))
            # price_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "egr_footer_price_value")))
            price_text = price_element.text
            match = re.search(r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))", price_text)
            if match:
                row['Preis'] = match.group(0)
        except Exception as e:
            row['Preis'] = "NaN"
            print("Kein Preis")
        
        # Klasse aktualisieren
        try:
            class_element = driver.find_element(By.CLASS_NAME, "MuiTypography-root.MuiTypography-caption.tss-custom-l1i3w8-ArticleHeaderCustomPlaceholder-secondary.mui-1i9w2df")
            row['Klasse'] = class_element.text
        except Exception as e:
            row['Klasse'] = "Nicht gefunden"
            print("Keine Klasse")
        
        canvas = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//canvas[@data-engine="Babylon.js v6.19.1"]')))
        
        # Mache einen Screenshot des Canvas Elements
        try: 
            canvas_screenshot = canvas.screenshot_as_png
        
            # Speichere den Screenshot
            with open(f"{row['Produktname']}.png", "wb") as file:
                file.write(canvas_screenshot)
        except:
            pass
        
        
        
        # # Screenshot des Canvas Elements
        # try:
        #     # Warte, bis das Canvas Element sichtbar ist
        #     canvas = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//canvas[@data-engine="Babylon.js v6.19.1"]')))
            
        #     # Mache einen Screenshot des Canvas Elements
        #     canvas_screenshot = canvas.screenshot_as_png
            
        #     # Speichere den Screenshot
        #     with open(f"{row['Produktname']}.png", "wb") as file:
        #         file.write(canvas_screenshot)
        # except Exception as e:
        #     print("Screenshot fehlgeschlagen für:", row['Produktname'])
    
    
        # # Screenshot des Canvas Elements
        # try:
        #     # Warte, bis das Canvas Element sichtbar ist
        #     canvas = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//canvas[@data-engine="Babylon.js v6.19.1"]')))
            
        #     # Mache einen Screenshot des Canvas Elements
        #     canvas_screenshot = canvas.screenshot_as_png
            
        #     # Speichere den Screenshot
        #     with open(f"{row['Produktname']}.png", "wb") as file:
        #         file.write(canvas_screenshot)
        # except Exception as e:
        #     print("Screenshot fehlgeschlagen für:", row['Produktname'])
        #     copy_and_rename_fallback_image("logo.jpg", f"{row['Produktname']}.png")
    
    
    return row

# Aktualisiere DataFrame
df = df.apply(update_dataframe, axis=1)

# Speichern des aktualisierten DataFrames
df.to_excel('aktualisierte_data.xlsx', index=False)

# Beenden des WebDriver
driver.quit()

# Gib das aktualisierte DataFrame aus
print(df)
