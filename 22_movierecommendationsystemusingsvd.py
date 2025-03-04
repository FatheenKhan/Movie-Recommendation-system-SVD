

### Importing the basic libraries
"""

import numpy as np
import pandas as pd

"""### Importing & Parsing the dataset as ratings and movies details"""

ratingData = pd.io.parsers.read_csv('ratings.dat', 
    names=['user_id', 'movie_id', 'rating', 'time'],
    engine='python', delimiter='::')
movieData = pd.io.parsers.read_csv('movies.dat',
    names=['movie_id', 'title', 'genre'],
    engine='python', delimiter='::')
print(ratingData)

"""### Create the ratings matrix of shape (m×u)"""

ratingMatrix = np.ndarray(
    shape=(np.max(ratingData.movie_id.values), np.max(ratingData.user_id.values)),
    dtype=np.uint8)
ratingMatrix[ratingData.movie_id.values-1, ratingData.user_id.values-1] = ratingData.rating.values
print(ratingMatrix)

"""### Subtract Mean off - Normalization"""

normalizedMatrix = ratingMatrix - np.asarray([(np.mean(ratingMatrix, 1))]).T
print(normalizedMatrix)

"""### Computing SVD"""

A = normalizedMatrix.T / np.sqrt(ratingMatrix.shape[0] - 1)
U, S, V = np.linalg.svd(A)

"""### Calculate cosine similarity, sort by most similar and return the top N"""

def similar(ratingData, movie_id, top_n):
    index = movie_id - 1 # Movie id starts from 1
    movie_row = ratingData[index, :]
    magnitude = np.sqrt(np.einsum('ij, ij -> i', ratingData, ratingData)) #Einstein summation |  traditional matrix multiplication and is equivalent to np.matmul(a,b)
    similarity = np.dot(movie_row, ratingData.T) / (magnitude[index] * magnitude)
    sort_indexes = np.argsort(-similarity) #Perform an indirect sort along the given axis (Last axis)
    return sort_indexes[:top_n]

"""### Select k principal components to represent the movies, a movie_id to find recommendations and print the top_n results"""

k = 50
movie_id = 2
top_n = 5

sliced = V.T[:, :k] # representative data
indexes = similar(sliced, movie_id, top_n)

print('Recommendations for Movie {0}: \n'.format(
movieData[movieData.movie_id == movie_id].title.values[0]))
for id in indexes + 1:
    print(movieData[movieData.movie_id == id].title.values[0])
