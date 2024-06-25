from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai


genai.configure(api_key='AIzaSyDJOep98ePv8DcYLDjc9xJUpAX33fkpYTM')

model = genai.GenerativeModel('gemini-1.5-flash')
def extraire_donnees(url, chose_a_extraire):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    driver = webdriver.Chrome( options=options)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        content = element.text
       
        print("content is "+content)
        prompt = f"Organiser et faire l'extraction des {chose_a_extraire} avec leurs détails de ce texte même si le texte est long. Je veux le résultat sous forme de tableau de csv si c'est possible. Je veux seulement le tableau, je ne veux aucun description et aucun titre avec le tableau et voici le texte : {content}"
    
        response = model.generate_content(prompt)
        data = response.text
        print(data)
        lines = data.strip().split("\n")
        data_ignored_first_last_lines = "\n".join(lines[1:-1])
        if data_ignored_first_last_lines:
            csv_file = 'extracted_data.csv'
            with open(csv_file, 'w', encoding="utf-8") as out:
                out.write(data_ignored_first_last_lines)
            return csv_file
        else:
            return None
    finally:
        driver.quit()







