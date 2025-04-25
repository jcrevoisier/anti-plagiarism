from flask import Flask, request, jsonify, render_template
import os
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from googlesearch import search as google_search
import re

app = Flask(__name__)

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Remove blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    
    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    
    return tokens

def get_chunks(tokens, chunk_size=10):
    return [' '.join(tokens[i:i+chunk_size]) for i in range(0, len(tokens), chunk_size)]

def search_for_plagiarism(chunks, num=5):
    results = []
    
    for chunk in chunks[:5]:  # Limit to first 5 chunks to avoid rate limiting
        try:
            search_results = list(google_search(chunk, num_results=num))
            if search_results:
                results.append({
                    'chunk': chunk,
                    'sources': search_results
                })
        except Exception as e:
            results.append({
                'chunk': chunk,
                'error': str(e)
            })
    
    return results

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/check-plagiarism', methods=['POST'])
def check_plagiarism():
    data = request.json
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url']
    
    # Extract text from URL
    text = extract_text_from_url(url)
    
    # Preprocess text
    tokens = preprocess_text(text)
    
    # Get chunks
    chunks = get_chunks(tokens)
    
    # Search for plagiarism
    plagiarism_results = search_for_plagiarism(chunks)
    
    return jsonify({
        'url': url,
        'results': plagiarism_results
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
