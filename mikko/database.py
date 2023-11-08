import psycopg2

from decouple import config


DATABASE_URL = config('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS words (
        word TEXT PRIMARY KEY
    )
''')

def add_word(word):
    cur.execute('''
        INSERT INTO words (word) VALUES (%s)
        ON CONFLICT (word) DO NOTHING
    ''', (word,))
    conn.commit()

def word_exists(word):
    cur.execute('SELECT 1 FROM words WHERE word = %s', (word,))
    return cur.fetchone() is not None

def get_last_words(n=10):
    cur.execute('SELECT word FROM words ORDER BY word DESC LIMIT %s', (n,))
    return [row[0] for row in cur.fetchall()]
