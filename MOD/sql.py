import sqlite3


def sql_connection(func):
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect("previous_games.db")
        cursor = connection.cursor()
        rv = func(cursor, *args, **kwargs)
        cursor.close()
        connection.commit()
        connection.close()
        return rv

    return wrapper


@sql_connection
def retrieve_previous_games(cursor, offset):
    query = f"""SELECT GameID, Outcome, IsSinglePlayer, Topology, GridSize, Day, Month, Year, Time
    FROM Game, Settings
    WHERE Game.SettingsID = Settings.SettingsID
    ORDER BY GameID DESC
    LIMIT 5
    OFFSET {offset};"""
    cursor.execute(query)
    return cursor.fetchall()


@sql_connection
def calculate_total_games(cursor):  # Aggregate SQL functions
    query = """SELECT COUNT(GameID)
    FROM Game;"""
    cursor.execute(query)
    return cursor.fetchall()[0][0]


@sql_connection
def retrieve_win_rates(cursor):
    player1_query = """SELECT COUNT(GameID)
    FROM Game
    WHERE Outcome = 1;"""
    cursor.execute(player1_query)
    player1_wins = cursor.fetchall()[0][0]

    player2_query = """SELECT COUNT(GameID)
    FROM Game
    WHERE Outcome = 2;"""
    cursor.execute(player2_query)
    player2_wins = cursor.fetchall()[0][0]

    total_games = calculate_total_games()

    return player1_wins / total_games, player2_wins / total_games


@sql_connection
def retrieve_settings_id(cursor, is_single_player, topology, grid_size, line_size):
    query = f"""SELECT SettingsID
    FROM Settings
    WHERE IsSinglePlayer = {is_single_player}
        AND Topology = \"{topology}\"
        AND GridSize = {grid_size}
        AND LineSize = {line_size};"""
    cursor.execute(query)
    result = cursor.fetchall()
    if bool(result):
        return result[0][0]
    return False


@sql_connection
def insert_settings(cursor, is_single_player, topology, grid_size, line_size):
    query = f"""INSERT INTO Settings
    VALUES (NULL, {is_single_player}, \"{topology}\", {grid_size}, {line_size});"""
    cursor.execute(query)


@sql_connection
def get_latest_settings_id(cursor):
    query = f"""SELECT SettingsID
    FROM Settings
    ORDER BY SettingsID DESC
    LIMIT 1"""
    cursor.execute(query)
    return cursor.fetchall()[0][0]


@sql_connection
def insert_game(cursor, settings_id, outcome, day, month, year, time):
    query = f"""INSERT INTO Game
    VALUES (NULL, {settings_id}, {outcome}, {day}, {month}, {year}, \"{time}\");"""
    cursor.execute(query)


@sql_connection
def get_latest_game_id(cursor):
    query = f"""SELECT GameID
    FROM Game
    ORDER BY GameID DESC
    LIMIT 1"""
    cursor.execute(query)
    return cursor.fetchall()[0][0]


@sql_connection
def insert_move(cursor, move_no, game_id, player, square):
    query = f"""INSERT INTO Move
    VALUES ({move_no}, {game_id}, {player}, \"{square}\")"""
    cursor.execute(query)


@sql_connection
def retrieve_settings(cursor, game_id):  # Cross-table parameterised SQL
    query = f"""SELECT Topology, GridSize, LineSize, IsSinglePlayer
    FROM Settings
    WHERE SettingsID = (SELECT SettingsID FROM Game WHERE GameID = {game_id});"""
    cursor.execute(query)
    return cursor.fetchall()[0]


@sql_connection
def retrieve_moves(cursor, game_id):
    query = f"""SELECT Square
    FROM Move
    WHERE GameID = {game_id}
    ORDER BY MoveNo;"""
    cursor.execute(query)
    return cursor.fetchall()
