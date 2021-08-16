import psycopg2
import os

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU:
    USER = os.environ.get('DB_USERNAME')
    PASSWORD = os.environ.get('DB_PASSWORD')
    DATABASE = os.environ.get("DB")
    DATABASE_URL = os.environ.get('DB_HOST')
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
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                discord_id VARCHAR(255) NOT NULL,
                discord_name VARCHAR(255) NOT NULL
            );

            INSERT INTO character_discord VALUES (DEFAULT, 'Lira', '#000124', 'Mikon#2245');
            INSERT INTO character_discord VALUES (DEFAULT, 'Kari', '#000256', 'Soma#2512');
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

    print(users)
    return users

if __name__ == '__main__':
    #create_character_discord()
    fetch_character_discord()
