import datetime
import psycopg2

POSTGRES = {
    'user': 'of_dck',
    'pw': 'gft78kP9!luY!',
    'db': 'onlyfeed',
    'host': 'onlyfeed.ddns.net',
    'port': '5432',
}

conn = psycopg2.connect( host=POSTGRES['host'], user=POSTGRES['user'], password=POSTGRES['pw'], dbname=POSTGRES['db'])

def days_between(d1, d2):
    print(d1)
    print(abs((d2 - d1).days))
    return abs((d2 - d1).days)

def get_games_to_compare(id_user):
    games = {}
    cur = conn.cursor()
    cur.execute('SELECT id_game_test, id_game_one, id_game_two, id_game_three FROM of_test_game_similarity WHERE id_game_test NOT IN (SELECT id_test FROM of_similarity_test_result WHERE id_user = '+str(id_user)+') ORDER BY date_create DESC LIMIT 1')
    result = cur.fetchall()

    for i in range(4):
        cur.execute('SELECT name FROM steam_video_games WHERE id = ' + str(result[0][i]))
        game_name = cur.fetchall()
        games[result[0][i]] = game_name[0][0]

    return games