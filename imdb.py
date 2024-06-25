import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

genai.configure(api_key='AIzaSyDJOep98ePv8DcYLDjc9xJUpAX33fkpYTM')

def fetch_imdb_data_and_generate_csv(url, output_file='extracted_data.csv'):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(url, headers=headers)
        soup = BeautifulSoup(result.text, "html.parser")
        text = soup.text
        prompt = "Organiser et faire l'extraction des films et séries avec leurs détails (n'oubliez pas les titres) de ce texte même si le texte est long. Je veux le résultat sous forme de tableau de csv si c'est possible. Je veux seulement le tableau, je ne veux aucune description et aucun titre avec le tableau et voici le texte : " + text
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
    except Exception as e:
        print(f"Erreur lors de l'exécution de la fonction : {e}")
        return None



#fetch_imdb_data_and_generate_csv(url="https://www.imdb.com/chart/top/", output_file='imdb.csv')
