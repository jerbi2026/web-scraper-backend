import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

genai.configure(api_key='AIzaSyDJOep98ePv8DcYLDjc9xJUpAX33fkpYTM')
model = genai.GenerativeModel('gemini-1.5-flash')

def extraire_donnees(url, chose_a_extraire):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")
        return None
    
    soup = BeautifulSoup(r.text, "lxml")
    text = soup.get_text()
    prompt = f"Organiser et faire l'extraction des {chose_a_extraire} avec leurs détails de ce texte même si le texte est long. Je veux le résultat sous forme de tableau de csv si c'est possible et sous forme UTF-8.. Je veux seulement le tableau, je ne veux aucun description et aucun titre avec le tableau et voici le texte : {text}"
    
    response = model.generate_content(prompt)
    data = response.text
    lines = data.strip().split("\n")
    data_ignored_first_last_lines = "\n".join(lines[1:-1])
    if data_ignored_first_last_lines:
        csv_file = 'extracted_data.csv'
        with open(csv_file, 'w', encoding="utf-8") as out:
            out.write(data_ignored_first_last_lines)
        return csv_file
    else:
        return None


