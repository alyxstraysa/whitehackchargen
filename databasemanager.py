import psycopg2
import os

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU:
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB = os.environ.get("DB")
    DB_HOST = os.environ.get('DB_HOST')
else:
    from secrets import *

def create_character_discord():
    
    conn = psycopg2.connect(DB_HOST, sslmode='require',
                            database=DB, user=DB_USERNAME, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
        """
            DROP TABLE IF EXISTS character_discord;

            CREATE TABLE character_discord (
                user_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                discord_id VARCHAR(255) NOT NULL,
                discord_name VARCHAR(255) NOT NULL
            );

            INSERT INTO character_discord VALUES (DEFAULT, 'Lira', '#000124', 'Mikon#2245');
            INSERT INTO character_discord VALUES (DEFAULT, 'Kari', '#000256', 'Soma#2512');
            INSERT INTO character_discord VALUES (DEFAULT, 'Mikasa', '#000384', 'Mikasa#2512');
            INSERT INTO character_discord VALUES (DEFAULT, 'Rei', '#000512', 'Rei#2512');
        """
    )

    conn.commit()
    conn.close()

def create_whitehack_character():
    conn = psycopg2.connect(DB_HOST, sslmode='require',
                            database=DB, user=DB_USERNAME, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
        """
            DROP TABLE IF EXISTS whitehack_character;

            CREATE TABLE whitehack_character (
                char_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name VARCHAR(255) NOT NULL,
                archetype VARCHAR(255) NOT NULL,
                group1 VARCHAR(255) NOT NULL,
                group2 VARCHAR(255),
                group3 VARCHAR(255),
                group4 VARCHAR(255),
                group5 VARCHAR(255),
                stat_str INTEGER NOT NULL,
                stat_dex INTEGER NOT NULL,
                stat_con INTEGER NOT NULL,
                stat_int INTEGER NOT NULL,
                stat_wis INTEGER NOT NULL,
                ST INTEGER NOT NULL,
                HP INTEGER NOT NULL,
                AC INTEGER NOT NULL,
                MV INTEGER NOT NULL,
                AV INTEGER NOT NULL
            );

            INSERT INTO whitehack_character VALUES (DEFAULT, 1, 'Terra', 'Strong', 'Black Librarians', NULL, NULL, NULL, NULL, 6, 15, 14, 9, 13, 6, 6, 1, 30, 30);
        """
    )

    conn.commit()
    conn.close()

def fetch_character_discord():
    conn = psycopg2.connect(DB_HOST, sslmode='require',
                            database=DB, user=DB_USERNAME, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("SELECT * FROM character_discord;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = {}
    for i in rows:
        users[i[0]] = {'name' : i[1], 'discord_id' : i[2], 'discord_name' : i[3]}

    return users

def fetch_whitehack_character():
    conn = psycopg2.connect(DB_HOST, sslmode='require',
                            database=DB, user=DB_USERNAME, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("SELECT * FROM whitehack_character;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    whitehack_character = {}
    for i in rows:
        whitehack_character[i[0]] = {'char_id' : i[0], 'user_id' : i[1], 'name' : i[2], 'archetype' : i[3], 'group' : i[4], 'group2' : i[5], 'group3' : i[6], 'group4' : i[7], 'group5' : i[8], 'stat_str' : i[9], 'stat_dex' : i[10], 'stat_con' : i[11], 'stat_int' : i[12], 'stat_wis' : i[13], 'ST' : i[14], 'HP' : i[15], 'AC' : i[16], 'MV' : i[17], 'AV' : i[18]}
    return whitehack_character

if __name__ == '__main__':
    #create_character_discord()
    create_whitehack_character()
    #fetch_character_discord()
    print(fetch_whitehack_character())
