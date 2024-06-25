import time
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import google.generativeai as genai


genai.configure(api_key='AIzaSyDJOep98ePv8DcYLDjc9xJUpAX33fkpYTM')

model = genai.GenerativeModel('gemini-1.5-flash')

class Product:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def to_dict(self):
        return {
            'title': self.title,
            'link': self.link
        }



def scrape_google_search(search_keyword, scroll_count=0):
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.google.com/search?q=" + search_keyword)

        for _ in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        search_results = soup.find_all("div", class_="tF2Cxc")

       

        products = []

        for i, result in enumerate(search_results):
            try:
                title = result.h3.text
                link = result.a["href"]
                products.append(Product(title, link))
                

            except Exception as e:
                print(f"Erreur lors du traitement du lien : {link}\nErreur : {e}")
                continue

        return products

    finally:
        driver.quit()





def analyze_with_gemini(products):
    prompt = 'Voici une liste de produit avec leurs liens et je veux que vous faites une analyse sur les offres en mentionnant les prix si c est possible (je ne veux pas des remarques juste une analyse en bref). voici la liste\n'
    for product in products : 
        prompt+= 'produit : '+product.title+ ' ; lien : '+product.link+'\n'
         
    response = model.generate_content(prompt)
    data = response.text
    return data

