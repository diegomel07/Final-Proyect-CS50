from flask import Flask, render_template, request
import requests
from PIL import Image

# Configurando apliación
app = Flask(__name__)

@app.route('/')
def index():

    #quote
    quote = requests.get('https://animechan.vercel.app/api/random').json()

    #Si la longitud de la quote es muy larga
    if len(quote['quote']) > 200:
        return index()

    return render_template('index.html', quote=quote)
     

@app.route('/buscar_animes')
def buscar_animes():

    name = request.args.get('q')

    if not name:
        name.replace(' ', '%20')

    #si el tamaño del string es menor a 3:
    if len(name) < 4:
        return 'TODO'
        
    url = 'https://api.jikan.moe/v3/search/anime?q=' + name + '$page=1'

    response = requests.get(url).json()
    animes = response['results']

    return  render_template('buscar_animes.html', animes=animes)


@app.route('/buscar_mangas', methods=['POST', 'GET'])
def buscar_mangas():
    
    #quote
    quote = requests.get('https://animechan.vercel.app/api/random').json()

    #Si la longitud de la quote es muy larga
    if len(quote['quote']) > 200:
        return index()

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


