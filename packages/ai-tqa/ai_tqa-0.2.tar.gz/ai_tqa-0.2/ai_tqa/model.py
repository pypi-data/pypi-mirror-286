import os
import tensorflow as tf
import json
import re
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')


class TextEvaluator:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, 'data', 'my_model.h5')
        data_path = os.path.join(current_dir, 'data', 'data.json')

        self.model = tf.keras.models.load_model(model_path)
        self.max_sequence_length = self.model.input_shape[1]

        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        texts = [item['text'] for item in data]
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer()
        self.tokenizer.fit_on_texts(texts)

    def preprocess_text(self, text):
        text = re.sub(r'[^a-zA-Zа-яА-ЯёЁ\s]', '', text.capitalize())
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word.isalnum()]
        return tokens

    def evaluate_word(self, word):
        sequence = self.tokenizer.texts_to_sequences([word])
        padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=self.max_sequence_length)
        prediction = self.model.predict(padded_sequence)
        return prediction[0, 0]

    def evaluate_text(self, text):
        preprocessed_input = self.preprocess_text(text)
        sequence = self.tokenizer.texts_to_sequences([' '.join(preprocessed_input)])
        padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=self.max_sequence_length)
        prediction = self.model.predict(padded_sequence)
        bad_words = [word for word in preprocessed_input if self.evaluate_word(word) > 0.5]
        return prediction[0, 0], bad_words