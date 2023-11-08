import tensorflow as tf
import os

from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from database import add_word, word_exists


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

import gui
