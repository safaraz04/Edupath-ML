# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b6W6sw9L4MYKDbh7H0fob5kSUJaU-oRQ
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

path = '.'
df = pd.read_excel("/content/Data_Jurusan_Lengkap.xlsx")

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Deskripsi'])

label_encoder = LabelEncoder()
df['Jurusan_Encoded'] = label_encoder.fit_transform(df['Jurusan'])

X_train, X_test, y_train, y_test = train_test_split(
    tfidf_matrix, df['Jurusan_Encoded'], test_size=0.2, random_state=42
)

model = Sequential()
model.add(Dense(64, input_dim=tfidf_matrix.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(len(df['Jurusan'].unique()), activation='softmax'))


model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train.toarray(), y_train, epochs=100, batch_size=32, validation_split=0.2)

y_pred = np.argmax(model.predict(X_test.toarray()), axis=1)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: {:.2f}".format(accuracy))

user_input = "Saya hitler "
user_input_vector = tfidf_vectorizer.transform([user_input])
predicted_probabilities = model.predict(user_input_vector.toarray())
predicted_class = np.argmax(predicted_probabilities)

predicted_jurusan = label_encoder.inverse_transform([predicted_class])[0]
print("Predicted Jurusan:", predicted_jurusan)