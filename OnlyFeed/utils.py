def get_games():
    cur = db.cursor()
    cur.execute("SELECT name FROM steam_video_games")
    results = cur.fetchall()

    with open("games.txt", "a+") as f:
        for result in results:
            game = result[0].replace("'", " ")
            f.write("- \'" + str(game) + "\'\n")

get_games()