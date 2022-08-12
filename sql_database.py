import sqlite3

conn = sqlite3.connect('local_db/database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_values(user_id: int, first_name: str, last_name: str, username: str):
    cursor.execute("INSERT OR IGNORE INTO telegram_user (user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)",
                   (user_id, first_name, last_name, username))
    conn.commit()
