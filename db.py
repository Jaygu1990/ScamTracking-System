import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create a table (if it doesn't exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tiktok_username TEXT NOT NULL UNIQUE,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            province_or_state TEXT NOT NULL,
            note TEXT,
            reporting_streamer TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database and table created successfully!")
