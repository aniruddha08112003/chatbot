import nltk
nltk.download('punkt')
nltk.download('wordnet')

import json
import numpy as np
import random
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import pickle

# Initialize the lemmatizer and load the intents file
lemmatizer = WordNetLemmatizer()

with open(r'E:\flower_shop_chatbot\training\intent.json') as file:
    intents = json.load(file)

# Data preprocessing
words = []
classes = []
documents = []
ignore_words = ['?', '!', '.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and sort words and classes
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(set(words))  # Remove duplicates and sort
classes = sorted(set(classes))  # Remove duplicates and sort

# Create training data
training = []
output_empty = [0] * len(classes)

# Creating the training set
for doc in documents:
    bag = []
    word_patterns = doc[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    
    # Create bag-of-words array: 1 if word found in pattern, 0 otherwise
    bag = [1 if word in word_patterns else 0 for word in words]
    
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1  # Set the correct class label to 1
    
    training.append([bag, output_row])

# Shuffle the data and convert it to a NumPy array
random.shuffle(training)

# Convert lists into numpy arrays
train_x = np.array([item[0] for item in training])  # Features (bag of words)
train_y = np.array([item[1] for item in training])  # Labels (one-hot encoded classes)

# Build the neural network model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))  # Output layer

# Compile the model
adam = Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

# Train the model
model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save the model
model.save('model.h5')

# Save words and classes
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))
