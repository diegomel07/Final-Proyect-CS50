from flask import Flask, render_template, request
import requests
from PIL import Image
import urllib.request

# Configurando apliación
app = Flask(__name__)

@app.route('/')
def index():

    #quote
    quote = requests.get('https://animechan.vercel.app/api/random').json()
   

    return render_template('index.html', quote=quote)

@app.route('/buscar_animes', methods=['POST', 'GET'])
def buscar_animes():

    #quote
    quote = requests.get('https://animechan.vercel.app/api/random').json()
    

    if request.method == 'POST':

        name = request.form.get('anime').replace(' ', '%20')

        #si el tamaño del string es menor a 3:
        if len(name) < 4:
            return 'TODO'
        
        url = 'https://api.jikan.moe/v3/search/anime?q=' + name + '$page=1'

        response = requests.get(url).json()
        animes = response['results']

        return  render_template('buscar_animes.html', animes=animes, quote=quote)

    else:
        
        return render_template('busca_animes.html', quote=quote)


@app.route('/buscar_mangas', methods=['POST', 'GET'])
def buscar_mangas():
    
    #quote
    quote = requests.get('https://animechan.vercel.app/api/random').json()

    if request.method == 'POST':

        name = request.form.get('manga').replace(' ', '%20')

        if len(name) < 4:
            return 'TODO'

        url = 'https://api.jikan.moe/v3/search/manga?q=' + name + '$page=1'

        response = requests.get(url).json()
        print(response)

        mangas = response['results']

        return render_template('buscar_mangas.html', mangas=mangas, quote=quote)

    else:
        return render_template('buscar_mangas.html', quote=quote)


