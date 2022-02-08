from flask import Flask, render_template, request, redirect, session
import requests
from string import punctuation
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

from helpers import login_required

# Configurando apliación
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def index():

    # get seasonal anime
    url = 'https://api.jikan.moe/v4/seasons/2022/winter'

    response = requests.get(url).json()
    season_animes = response['data']

    # get top anime
    url = 'https://api.jikan.moe/v4/top/anime'
    response = requests.get(url).json()
    top_animes = response['data']


    # get top manga
    url = 'https://api.jikan.moe/v4/top/manga'
    response = requests.get(url).json()
    top_mangas = response['data']

    # styling the author´s name
    for manga in top_mangas:
        author = manga['authors'][0]['name']
        author = author.replace(' ','').split(',')
        author = author[::-1]
        manga['authors'][0]['name'] = ' '.join(author)


        
    return render_template('index.html', season_animes=season_animes[:5], top_animes=top_animes[:5], top_mangas=top_mangas[:5])

@app.route('/search')
def search():

    quest = request.args.get('q')

    if quest:

        quest.rstrip()
        if len(quest) < 3:
            return redirect('/')
        
        url_animes = 'https://api.jikan.moe/v4/anime?q=' + quest + '&limit=10&order_by=members&sort=desc'
        url_mangas = 'https://api.jikan.moe/v4/manga?q=' + quest + '&limit=10&order_by=members&sort=desc'

        response_animes = requests.get(url_animes).json()
        animes = response_animes['data']
        response_mangas = requests.get(url_mangas).json()
        mangas = response_mangas['data']

        # Styling the author´s name 
        for manga in mangas:
            author = (manga['authors'][0]['name']).replace(' ','').split(',')
            author = author[::-1]
            manga['authors'][0]['name'] = ' '.join(author)


        return render_template('search.html', animes=animes, mangas=mangas)
        
    else:

        return render_template('search.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():

    # Forget any user_id
    session.clear()


    if request.method == 'POST':
        conexion = sqlite3.connect('users.db')
        db = conexion.cursor()

        username = request.form.get('username')
        password = request.form.get('password')
        conf_password = request.form.get('conf_password')

        # Si no digito username, password o conf_password
        if not username or not password or not conf_password:
            return 'TODO'
        
        # -------Checkeando el username-------

        # Si el username len no esta en el rango (0, 16)
        if len(username) not in range(5, 16):
            return 'TODO'
        
        # Si contiene algun caracter especial
        for chr in username:
            if chr in punctuation:
                return 'TODO'

        cont_nums = 0
        cont_letters = 0
        # Si no contiene letras y números
        for chr in username:
            if chr.isdigit():
                cont_nums += 1
            if chr.isalpha():
                cont_letters += 1
        if cont_letters == 0 or cont_nums == 0:
            return 'TODO'
        
        # Si el usuario ya existe
        db_users = db.execute('SELECT username FROM users WHERE username = "%s"' % username)
        if len(db_users.fetchall()) != 0:
            return 'ya esta en la base'

        #-------- Checkeando la contraseña --------
        # Si la longitud no esta en el rango (8, 21)
        if len(password) not in range(8, 21):
            return 'TODO'
        
        # Si no contiene letras y numeros
        cont_nums = 0
        cont_letters = 0
        for chr in password:
            if chr.isdigit():
                cont_nums += 1
            if chr.isalpha():
                cont_letters += 1
        if cont_letters == 0 or cont_nums == 0:
            return 'TODO'
        
        # Si la contraseña ya existe
        db_passw = db.execute('SELECT hash FROM users')

        for hash in db_passw:
            if check_password_hash(hash[0], password):
                return 'Ya existe la contraseña'
        
        # ------ Checkando validation -------
        if password != conf_password:
            return 'TODO'
        

        # ------ Registro Exitoso --------
        data = [username, generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)]
        db.execute('INSERT INTO users (username, hash) VALUES (?, ?)', data)
        conexion.commit()

        # Remember which user has logged in
        user_id = db.execute('SELECT id FROM users WHERE username = "%s"' % username)
        for i in user_id:
            session["user_id"] = i[0]


        conexion.close()
        return redirect('/')

    else:
        return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():

    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        conexion = sqlite3.connect('users.db')
        db = conexion.cursor()

        username = request.form.get('username')
        password = request.form.get('password')

        # Si no digito username, password
        if not username or not password:
            return 'TODO'
        
        # -------Checkeando el username-------
        # Si el usuario no existe
        db_users = db.execute('SELECT username FROM users WHERE username = "%s"' % username)
        if len(db_users.fetchall()) == 0:
            return 'No existe'

        #-------- Checkeando la contraseña --------
        # Si la contraseña no coincide
        db_passw = db.execute('SELECT hash FROM users WHERE username = "%s"' % username)

        for hash in db_passw:
            if not check_password_hash(hash[0], password):
                return 'la contraseña no coincide'

        # Remember which user has logged in
        db_id = db.execute('SELECT id FROM users WHERE username = "%s"' % username)
        for rows in db_id:
            session["user_id"] = rows[0]

        return redirect('/profile')

    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route('/profile')
@login_required
def profile():

    user_id = session.get('user_id')
    conexion = sqlite3.connect('users.db')
    db = conexion.cursor()

    # Recuperando el username de la persona
    username_quest = db.execute('SELECT username FROM users WHERE id = "%s"' % user_id)
    for u in username_quest:
        username = u[0]

    anime_quest = request.args.get('anime_status')
    manga_quest = request.args.get('manga_status')

    if not anime_quest and not manga_quest:
        return render_template('profile.html', username=username)

    anime, anime_status = anime_quest.split()
    anime_status = int(anime_status)

    manga, manga_status = manga_quest.split()
    manga_status = int(manga_status)


    # -----------Recuperando los animes de la persona----------------
    anime_ids = db.execute('SELECT ' + anime +'_id FROM users_'+ anime +'s WHERE user_id = "%s" AND status = %i' % (user_id, anime_status))

    url_b = 'https://api.jikan.moe/v4/'+ anime +'/'

    anime_results = []
    for ids in anime_ids:
        url = url_b + str(ids[0])
        rq = requests.get(url).json()
        anime_results.append(rq['data'])

    # -----------Recuperando los mangas de la persona----------------
    manga_ids = db.execute('SELECT ' + manga +'_id FROM users_'+ manga +'s WHERE user_id = "%s" AND status = %i' % (user_id, manga_status))

    url_b = 'https://api.jikan.moe/v4/'+ manga +'/'

    manga_results = []
    for ids in manga_ids:
        url = url_b + str(ids[0])
        rq = requests.get(url).json()
        manga_results.append(rq['data'])

    # anime status
    anime_stats = {0: 'Plan to Watch', 1:'Watching', 2:'Completed', 3:'Dropped'}

    # manga status
    manga_stats = {0: 'Plan to Read', 1:'Reading', 2:'Completed', 3:'Dropped'}
    
    current_status = (anime_stats[anime_status], manga_stats[manga_status])

    return render_template('profile.html', current_status=current_status, animes=anime_results, mangas=manga_results, username=username)




@app.route('/add_to_list', methods=['GET', 'POST'])
@login_required
def add_to_list():
    
    if request.method == 'POST':
        user_id = session.get('user_id')
        conexion = sqlite3.connect('users.db')
        db = conexion.cursor()

        result_id = int(request.form.get('id'))
        type, status = request.form.get('status').split()
        status = int(status)

        # revisando que el anime/manga no este agregado ya en la misma lista
        user_result = db.execute('SELECT '+ type +'_id FROM users_'+ type +'s WHERE user_id = "%s" AND status = %i ' % (user_id, status))

        for id in user_result:
            if id[0] == result_id:
                return 'Ya esta en la lista seleccionada'
        
        # revisando que el anime/manga exista en la db
        user_result = db.execute('SELECT '+ type +'_id FROM users_'+ type +'s WHERE user_id = "%s"' % (user_id))

        ids = []
        for id in user_result:
            ids.append(id[0])

        values = [user_id, result_id, status]

        if result_id in ids:
            # si ya esta en alguna lista
            db.execute('UPDATE users_{}s SET status = {} WHERE {}_id = {}  AND user_id = "{}"'.format(type, status, type, result_id, user_id))
        else:
            # Si no esta en la lista
            db.execute('INSERT INTO users_' + type + 's (user_id, '+ type +'_id, status) VALUES (?, ? ,?)', values)

        conexion.commit()
        conexion.close()
        

        return redirect('/profile')
        
    else:
        return redirect('/')
    

@app.route('/selection')
def selection():

    # seleccionar los datos del anime/manga y devolverlos :)
    type, result_id = request.args.get('id').split()

    url = 'https://api.jikan.moe/v4/' + type + '/' + str(result_id)

    req = requests.get(url).json()

    result = req['data']

    return render_template('selection.html', result=result) 



