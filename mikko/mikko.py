import tensorflow as tf
import psycopg2
import os

from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


DATABASE_URL = 'postgres://tztciskwjxplsx:cbb3ab8876f3ee91404c5449c5a259f31f43748a7fa7b0c8d8e8a288d8b99931@ec2-34-250-252-161.eu-west-1.compute.amazonaws.com:5432/d6md02f4jqr4e3'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS words (
        word TEXT PRIMARY KEY
    )
''')


class MikkoAI(tf.keras.Model):
    def __init__(self):
        super(MikkoAI, self).__init__()
        self.embedding = layers.Embedding(input_dim=1000, output_dim=64)
        self.lstm = layers.LSTM(128)
        self.dense = layers.Dense(1, activation='sigmoid')
    
    def call(self, inputs, traning=False):
        x = self.embedding(inputs)
        x = self.lstm(x)
        return self.dense(x)

model = MikkoAI()

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')

def add_word(word):
    cur.execute('''
        INSERT INTO words (word) VALUES (%s)
        ON CONFLICT (word) DO NOTHING
    ''', (word, ))
    conn.commit()

def word_exists(word):
    cur.execute('SELECT 1 FROM words WHERE word = %s', (word,))
    return cur.fetchone() is not None

while True:
    message = input('You: ')

    if message == 'quit':
        break

    for word in message.split():
        if word_exists(word):
            print(f'Mikko: znam to słowo {word}')
        else:
            print(f'Mikko: wow nowe słowo {word}')
            add_word(word)
