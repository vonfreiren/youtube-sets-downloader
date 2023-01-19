import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder

# Load your dataset

df = pd.read_csv('/Users/javier/PycharmProjects/youtube-downloader/files/files.csv')

# Extract the filenames and labels
X = df['Filename']
y = df[['Title', 'Artist']]

X = np.array(X) # input features
y = np.array(y) # target values

enc = OneHotEncoder(handle_unknown='ignore')
X = enc.fit_transform(X.reshape(-1,1)).toarray()
# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Initialize the neural network model

# Initialize the models
title_model = MLPClassifier(hidden_layer_sizes=(50,), max_iter=1000, random_state=0)
artist_model = MLPClassifier(hidden_layer_sizes=(50,), max_iter=1000, random_state=0)

# Train the models
title_model.fit(X_train, y_train[:, 0])
artist_model.fit(X_train, y_train[:, 1])

# Evaluate the models
title_score = title_model.score(X_test, y_test[:, 0])
artist_score = artist_model.score(X_test, y_test[:, 1])
print("Title score: ", title_score)
print("Artist score: ", artist_score)

# Use the models to make predictions on new, unseen data
file_name = "James Hype - Old Skool Set.mp3"
new_data = np.array([file_name]) # new input data
title_prediction = title_model.predict(enc.transform(new_data.reshape(-1,1)).toarray())
artist_prediction = artist_model.predict(enc.transform(new_data.reshape(-1,1)).toarray())

print("Title prediction: ", title_prediction)
print("Artist prediction: ", artist_prediction)
