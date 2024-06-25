from flask import Flask, request, jsonify , send_from_directory
from flask_cors import CORS
import dynamique_website
import imdb
import mot_cle
import simple_site
import tradingview
import os

app = Flask(__name__)
CORS(app)  
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def home():
    return "Welcome to the Web Scraping API!"



@app.route('/scrape/dynamic', methods=['POST'])
def scrape_dynamic():
    data = request.json
    url = data.get('url')
    chose_a_extraire = data.get('chose_a_extraire')
    if not url or not chose_a_extraire:
        return jsonify({'error': 'URL and chose_a_extraire are required'}), 400

    csv_file = dynamique_website.extraire_donnees(url, chose_a_extraire)
    
    
    if csv_file:
        output_file = os.path.join('static', csv_file)
        if os.path.exists(output_file):
            os.remove(output_file)
        os.rename(csv_file, output_file)
        return jsonify({'message': 'Data extracted successfully', 'file': csv_file}), 200
    else:
        return jsonify({'error': 'Failed to extract data'}), 500

@app.route('/scrape/imdb', methods=['POST'])
def scrape_imdb():
    data = request.json
    url = data.get('url')
   
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    csv_file = imdb.fetch_imdb_data_and_generate_csv(url)
    if csv_file:
         output_file = os.path.join('static', csv_file)
         if os.path.exists(output_file):
            os.remove(output_file)
         os.rename(csv_file, output_file)
         return jsonify({'message': 'Data extracted successfully', 'file': csv_file}), 200
    else:
        return jsonify({'error': 'Failed to extract data'}), 500

@app.route('/scrape/keyword', methods=['POST'])
def scrape_keyword():
    data = request.json
    search_keyword = data.get('search_keyword')
    scroll_count = data.get('scroll_count', 0)
    
    if not search_keyword:
        return jsonify({'error': 'search_keyword is required'}), 400

    products = mot_cle.scrape_google_search(search_keyword, scroll_count)
    analysis = mot_cle.analyze_with_gemini(products)
    
    products_data = [product.to_dict() for product in products]
    
    return jsonify({'message': 'Search and analysis completed', 'analysis': analysis, 'products': products_data}), 200


@app.route('/scrape/simple', methods=['POST'])
def scrape_simple():
    data = request.json
    url = data.get('url')
    chose_a_extraire = data.get('chose_a_extraire')
    if not url or not chose_a_extraire:
        return jsonify({'error': 'URL and chose_a_extraire are required'}), 400

    csv_file = simple_site.extraire_donnees(url, chose_a_extraire)
    if csv_file:
        output_file = os.path.join('static', csv_file)
        if os.path.exists(output_file):
            os.remove(output_file)
        os.rename(csv_file, output_file)
        return jsonify({'message': 'Data extracted successfully', 'file': csv_file}), 200
    else:
        return jsonify({'error': 'Failed to extract data'}), 500


@app.route('/scrape/tradingview', methods=['POST'])
def scrape_tradingview():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        csv_file = tradingview.get_tradingview_data(url)
        if csv_file:
            output_file = os.path.join('static', csv_file)
            if os.path.exists(output_file):
                os.remove(output_file)
            os.rename(csv_file, output_file)
            return jsonify({'message': 'Data extracted successfully', 'file': csv_file}), 200
        else:
            return jsonify({'error': 'Failed to extract data'}), 500
    except Exception as e:
        print(f"Erreur lors de l'appel de l'API : {e}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
