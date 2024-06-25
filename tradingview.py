import pandas as pd

def get_tradingview_data(url):
    try:
        tables = pd.read_html(url)
        df = pd.DataFrame(tables[0])
        csv_file = 'extracted_data.csv'
        #json_data=df.to_json()
        #print(json_data)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        return csv_file
    except Exception as e:
        print(f"Erreur lors de l'extraction des données : {e}")
        return None



