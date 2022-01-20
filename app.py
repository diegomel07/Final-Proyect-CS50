from unicodedata import name
from urllib import response
from flask import Flask, render_template, request, redirect
import requests
from PIL import Image

# Configurando apliación
app = Flask(__name__)

@app.route('/')
def index():

    # get seasonal anime
    url = 'https://api.jikan.moe/v3/season'

    response = requests.get(url).json()
    season_animes = response['anime']

    # get top anime
    url = 'https://api.jikan.moe/v3/top/anime/1'
    response = requests.get(url).json()
    top_animes = response['top']


    # get top manga
    url = 'https://api.jikan.moe/v3/top/manga/1'
    response = requests.get(url).json()
    top_mangas = response['top']

        
    return render_template('index.html', season_animes=season_animes[:6], top_animes=top_animes[:6], top_mangas=top_mangas[:6])

@app.route('/search')
def search():

    quest = request.args.get('q').replace(' ', '%20')

    if quest:
        if len(quest) < 3:
            return redirect('/')
        
        url_animes = 'https://api.jikan.moe/v3/search/anime?q=' + quest + '$page=1'
        url_mangas = 'https://api.jikan.moe/v3/search/manga?q=' + quest + '$page=1'

        try:
            response_animes = requests.get(url_animes).json()
            animes = response_animes['results']
            response_mangas = requests.get(url_mangas).json()
            mangas = response_mangas['results']
        except:
            animes, mangas = {}, {}

        return render_template('search.html', animes=animes, mangas=mangas)
        
    else:

        return render_template('search.html')



