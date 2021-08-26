import psycopg2
import os
from psycopg2 import sql

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU:
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB = os.environ.get("DB")
    DB_HOST = os.environ.get('DB_HOST')
else:
    from secrets import *

def connect_to_db():
    conn = psycopg2.connect(DB_HOST, sslmode='require',
                            database=DB, user=DB_USERNAME, password=DB_PASSWORD)
    cursor = conn.cursor()
    return conn, cursor    


def create_character_discord():  
    conn, cursor = connect_to_db()
    cursor.execute(
        """
            DROP TABLE IF EXISTS character_discord;

            CREATE TABLE character_discord (
                user_id SERIAL PRIMARY KEY,
                discord_id VARCHAR(255) NOT NULL,
                discord_name VARCHAR(255) NOT NULL
            );

            --INSERT INTO character_discord VALUES (DEFAULT, '#148270127610068993', 'Mikon#2245');
            --INSERT INTO character_discord VALUES (DEFAULT, '#000000000000000000', 'Soma#2512');
        """
    )

    conn.commit()
    conn.close()

def create_whitehack_character():
    conn, cursor = connect_to_db()
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
                str_group VARCHAR(255),
                dex_group VARCHAR(255),
                con_group VARCHAR(255),
                int_group VARCHAR(255),
                wis_group VARCHAR(255),
                ST INTEGER NOT NULL,
                HP INTEGER NOT NULL,
                AC INTEGER NOT NULL,
                MV INTEGER NOT NULL,
                AV INTEGER NOT NULL
            );

            INSERT INTO whitehack_character VALUES (DEFAULT, 1, 'Terra', 'Strong', 'Black Librarians', NULL, NULL, NULL, NULL, 6, 15, 14, 9, 13, NULL, NULL, NULL, NULL, NULL, 6, 6, 1, 30, 30);
            INSERT INTO whitehack_character VALUES (DEFAULT, 2, 'Aria', 'Deft', 'Elf', 'Archer', NULL, NULL, NULL, 6, 15, 14, 9, 13, NULL, NULL, NULL, NULL, NULL, 6, 6, 1, 30, 30);
        """
    )

    conn.commit()
    conn.close()

def add_new_character(char_dict):
    def cast_to_str(value):
        if value is None:
            return None
        else:
            return str(value)
    
    for key, value in char_dict.items():
        print(key)
        print(value)
        print(cast_to_str(value))

    conn, cursor = connect_to_db()
    cursor.execute("""
        INSERT INTO whitehack_character VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (char_dict['user_id'], char_dict['name'], char_dict['archetype'], char_dict['group1'], char_dict['group2'], char_dict['group3'], char_dict['group4'], char_dict['group5'], char_dict['stat_str'], char_dict['stat_dex'], char_dict['stat_con'], char_dict['stat_int'], char_dict['stat_wis'], char_dict['str_group'], char_dict['dex_group'], char_dict['con_group'], char_dict['int_group'], char_dict['wis_group'], char_dict['ST'], char_dict['HP'], char_dict['AC'], char_dict['MV'], char_dict['AV']))

    conn.commit()
    conn.close()
    return "Character added"
    

def register_new_user(user_data):
    conn, cursor = connect_to_db()
    cursor.execute("SELECT * FROM character_discord WHERE discord_id = %s;", (str(user_data['discord_id']),))
    rows = cursor.fetchall()
    
    if len(rows) > 0 and rows[0][0] is not None:
        return False
    else:
        cursor.execute(
            """
                INSERT into character_discord (user_id, discord_id, discord_name) VALUES (DEFAULT, %s, %s);
            """, (str(user_data['discord_id']), str(user_data['discord_name']))
        )
        conn.commit()
        conn.close()
        return True

def fetch_user_id(discord_id):
    conn, cursor = connect_to_db()
    cursor.execute("SELECT user_id FROM character_discord where discord_id = %s;", (str(discord_id),))
    rows = cursor.fetchall()
    conn.close()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return None


def fetch_character_discord():
    conn, cursor = connect_to_db()
    cursor.execute("SELECT * FROM character_discord;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    users = {}
    for i in rows:
        users[i[0]] = {'user_id' : i[0], 'discord_id' : i[1], 'discord_name' : i[2]}

    return users

def fetch_character_discord_by_id(user_id):
    conn, cursor = connect_to_db()
    cursor.execute("SELECT * FROM character_discord WHERE user_id = %s;", (str(user_id),))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(rows) == 0:
        return None
    else:
        characters = {}
        for i in rows:
            characters[i[0]] = {'user_id' : i[0], 'discord_id' : i[1], 'discord_name' : i[2]}
        return characters

def fetch_whitehack_character():
    conn, cursor = connect_to_db()
    cursor.execute("SELECT * FROM whitehack_character ORDER BY char_id;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    whitehack_character = {}
    for i in rows:
        whitehack_character[i[0]] = {'char_id': i[0], 'user_id': i[1], 'name': i[2], 'archetype': i[3], 'group1': i[4], 'group2': i[5],
                                     'group3': i[6], 'group4': i[7], 'group5': i[8], 'stat_str': i[9], 'stat_dex': i[10], 'stat_con': i[11], 'stat_int': i[12], 'stat_wis': i[13], 'str_group': i[14], 'dex_group': i[15],
                                     'con_group': i[16], 'int_group': i[17], 'wis_group': i[18], 'ST': i[19], 'HP': i[20], 'AC': i[21], 'MV': i[22], 'AV': i[23]}
    return whitehack_character

def update_whitehack_character(char_id, update_data):
    conn, cursor = connect_to_db()
    cursor.execute("SELECT * FROM whitehack_character WHERE char_id = %s;", (str(char_id),))
    rows = cursor.fetchall()
    
    if len(rows) == 0:
        return "No character found"
    else:
        for k, v in update_data.items():
            if k == 'char_id':
                pass
            if v == None:
                pass
            else:
                cursor.execute(
                    sql.SQL("UPDATE whitehack_character SET {} = %s WHERE char_id = %s;").format(sql.Identifier(k)), (v, str(char_id))
                )
        conn.commit()
        cursor.close()
        conn.close()
        
        return "Character updated"
    
def fetch_whitehack_character_by_id(id):
    conn, cursor = connect_to_db()
    cursor.execute("SELECT * FROM whitehack_character WHERE char_id = %s;", (id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    whitehack_character = {}
    if len(rows) == 0:
        return None
    else:
        for i in rows:
            whitehack_character[i[0]] = {'char_id': i[0], 'user_id': i[1], 'name': i[2], 'archetype': i[3], 'group1': i[4], 'group2': i[5],
                                        'group3': i[6], 'group4': i[7], 'group5': i[8], 'stat_str': i[9], 'stat_dex': i[10], 'stat_con': i[11], 'stat_int': i[12], 'stat_wis': i[13], 'str_group': i[14], 'dex_group': i[15],
                                        'con_group': i[16], 'int_group': i[17], 'wis_group': i[18], 'ST': i[19], 'HP': i[20], 'AC': i[21], 'MV': i[22], 'AV': i[23]}
        return whitehack_character
            
def add_whitehack_character(args):
    conn = psycopg2.connect(DB_HOST, sslmode='require',
                            database=DB, user=DB_USERNAME, password=DB_PASSWORD)
    return

if __name__ == '__main__':
    #create_character_discord()
    #create_whitehack_character()
    #fetch_character_discord()
    #register_new_user({'discord_id': '12345', 'discord_name':'Dog#2456'})
    pass
