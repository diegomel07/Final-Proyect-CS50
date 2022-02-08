# Kishu
### Video Demo: <https://www.youtube.com/watch?v=FlWU1Qdrl5U>
### Description:
Kishu is a web when you can search your favorite animes/mangas, and see a few features of it. Secondly, offer the capability to store different types of lists so you can trake your animes/mangas, you can create: plant to watch/read, watching/reading, watched/readed and dropped. This web page is powered by the JikanAPI, an unoficial API of myanimelist.
This aplication uses the flask archives organization (templates, static, app and requierements).
To get started, in the templates folder are seven archives.
- layout.html, contains the HTML code that is repeated in each HTML file. It has code for a navigation bar, a footer, and all the bindings needed to run the page (styles, bootstrap, etc.).
- index.html is Kishu's main page, it gives information about the web and shows some anime/manga link images.
- search.html is the page that shows the results of the search that was typed in the navigation bar, this page also includes a small box to type a new search
- selection.html is the page that displays information specific to the anime/manga that a user selected. The user can access this page by clicking the plus button that appears on each result of the search page or on the profile page, or any image on the index page. This page has a button that gives the user the option to add that anime/manga to a list.
- login.html displays a small form where the user can enter their username and password.
- register.html allows the user to create an account to use the tracking services, this HTML displays a form that requires a username, a password and a confirmation password.
- profile.html shows the anime/manga that the user adds to some list.

Now, the static folder, contain the styles file in where are included all the CSS code for the style of the page.

users.db is the database in charge of store all the data, it contains three tables: users, users_animes and users_mangas.
- the table users contain the data of each user. The username, the hash of each password and a specific ID for each user.
- the users_animes tables is a table attach to the users table by the users_id. This table is in charge of store all the IDs of the animes that the users have in their lists. This table contains: the users_id, anime_id and the status (the id of the list where this anime is included)
- the users_mangas tables is a table attach to the users table by the users_id. This table is in charge of store all the IDs of the mangas that the users have in their lists. This table contains: the users_id, mangas_id and the status ((the id of the list where this anime is included)


Following is the app.py file:
At first, it contains some code for the basic functionality of the page (libraries, application initialization, etc.).
Below have some functions:
- Index, this function returns the index.html file with the JSON data returned by the Jikan API, which contains information about the anime and manga shown on this page.
- Search, returns the file search.html with the JSON data returned by the Jikan API, which contains information about the anime and manga shown on this page.
- Register, this function is in charge of controlling the data entered by the user, if the data is correct, it connects with the user's database (users.db) and adds the information in the users table. Also, this function returns the register.html file.
- Log in, this function is responsible for controlling the data entered by the user, in case the username and password coincide with the information in the user table of the user database, the function allows the user logs in to the web page.
- Logout, clears the user session
- Profile, this function returns the file profile.html, with the animes and manga that belong to the list that the user selects, and it returns all the JSON data returned by the Jikan API.
- Add to list, the purpose of this function is to query the users_animes or users_mangas table and add the mal_id (the id of each anime or manga returned by the Jikan API) to the database, in case it already exists, change state or return ("It's in the same list").
- Selection, this function return the dedicated page (selection.html) for each manga or anime that the application selects.

In the helpers.py file it only exists one function that decorate routes to require login.

And finally the requirements file, it includes all the libraries that my application uses.
