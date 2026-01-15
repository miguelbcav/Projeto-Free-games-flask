from flask import Flask,render_template,request
import requests

app = Flask(__name__)

URL = "https://www.freetogame.com/api/games"
PER_PAGE = 28

def get_games():
    resp = requests.get(URL)
    resp.raise_for_status()

    return resp.json()

@app.route("/")
def home():

    search = request.args.get("search")
    page = int(request.args.get("page", 1))  # página atual
    data = get_games()

    if search:
        search = search.lower()
        data = [
            game for game in data
            if search in game["title"].lower()
        ]

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE

    games_page = data[start:end]

    games = [
        {   
            "id": game['id'],
            "title": game['title'],
            "thumbnail": game['thumbnail'],
        }
        for game in games_page
    ]

    total_pages = (len(data) + PER_PAGE - 1) // PER_PAGE

    return render_template(
        "index.html",         
        games=games,
        page=page,
        total_pages=total_pages,
        search=search
        )

@app.route("/game/<int:game_id>")
def game(game_id):
    from deep_translator import GoogleTranslator

    data = get_games()

    for game in data:
        if game['id'] == game_id:
            translated = GoogleTranslator(
                source="auto",
                target="pt"
            ).translate(game["short_description"])

            game_data = {
                "id": game['id'],
                "title": game['title'],
                "thumbnail": game['thumbnail'],
                "short_description": translated,
                "game_url": game['game_url'],
                "genre": game['genre'],
                "platform": game['platform'],
                "developer": game['developer'],
                "release_date": game['release_date']
            }

            return render_template("game.html", game=game_data)

    return "Jogo não encontrado", 404

if __name__ == "__main__":
    app.run()

