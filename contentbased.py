# -*- coding: utf-8 -*-
"""ContentBased.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/183w7QWz1UfT0kvwQEBjzrz_oNgPuBUUj

# **Content Based Recommendations**
"""

import pandas as pd 
import numpy as np 
df1=pd.read_csv('/content/drive/MyDrive/Movie_data/tmdb_5000_credits.csv')
df2=pd.read_csv('/content/drive/MyDrive/Movie_data/tmdb_5000_movies.csv')

from google.colab import drive
drive.mount('/content/drive')

"""The first dataset contains the following features:-

* movie_id - A unique identifier for each movie.
* cast - The name of lead and supporting actors.
* crew - The name of Director, Editor, Composer, Writer etc.

The second dataset has the following features:- 

* budget - The budget in which the movie was made.
* genre - The genre of the movie, Action, Comedy ,Thriller etc.
* homepage - A link to the homepage of the movie.
* id - This is infact the movie_id as in the first dataset.
* keywords - The keywords or tags related to the movie.
* original_language - The language in which the movie was made.
* original_title - The title of the movie before translation or adaptation.
* overview - A brief description of the movie.
* popularity - A numeric quantity specifying the movie popularity.
* production_companies - The production house of the movie.
* production_countries - The country in which it was produced.
* release_date - The date on which it was released.
* revenue - The worldwide revenue generated by the movie.
* runtime - The running time of the movie in minutes.
* status - "Released" or "Rumored".
* tagline - Movie's tagline.
* title - Title of the movie.
* vote_average -  average ratings the movie recieved.
* vote_count - the count of votes recieved.

Let's join the two dataset on the 'id' column

"""

df1.columns = ['id','tittle','cast','crew']
df2= df2.merge(df1,on='id')

"""Just a peak at our data."""

df2.head(5)

#Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer

#Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

#Replace NaN with an empty string
df2['overview'] = df2['overview'].fillna('')

#Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(df2['overview'])

#Output the shape of tfidf_matrix
tfidf_matrix.shape

"""We see that over 20,000 different words were used to describe the 4800 movies in our dataset.

With this matrix in hand, we can now compute a similarity score. There are several candidates for this; such as the euclidean, the Pearson and the [cosine similarity scores](https://en.wikipedia.org/wiki/Cosine_similarity). There is no right answer to which score is the best. Different scores work well in different scenarios and it is often a good idea to experiment with different metrics.

We will be using the cosine similarity to calculate a numeric quantity that denotes the similarity between two movies. We use the cosine similarity score since it is independent of magnitude and is relatively easy and fast to calculate. Mathematically, it is defined as follows:
![](data:image/png;base64,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)

Since we have used the TF-IDF vectorizer, calculating the dot product will directly give us the cosine similarity score. Therefore, we will use sklearn's **linear_kernel()** instead of cosine_similarities() since it is faster.
"""

# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

"""We are going to define a function that takes in a movie title as an input and outputs a list of the 10 most similar movies. Firstly, for this, we need a reverse mapping of movie titles and DataFrame indices. In other words, we need a mechanism to identify the index of a movie in our metadata DataFrame, given its title."""

#Construct a reverse map of indices and movie titles
indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()

"""We are now in a good position to define our recommendation function. These are the following steps we'll follow :-
* Get the index of the movie given its title.
* Get the list of cosine similarity scores for that particular movie with all movies. Convert it into a list of tuples where the first element is its position and the second is the similarity score.
* Sort the aforementioned list of tuples based on the similarity scores; that is, the second element.
* Get the top 10 elements of this list. Ignore the first element as it refers to self (the movie most similar to a particular movie is the movie itself).
* Return the titles corresponding to the indices of the top elements.
"""

# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df2['title'].iloc[movie_indices]

# Parse the stringified features into their corresponding python objects
from ast import literal_eval

features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)

"""Next, we'll write functions that will help us to extract the required information from each feature."""

# Get the director's name from the crew feature. If director is not listed, return NaN
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# Returns the list top 3 elements or entire list; whichever is more.
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []

# Define new director, cast, genres and keywords features that are in a suitable form.
df2['director'] = df2['crew'].apply(get_director)

features = ['cast', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)

# Print the new features of the first 3 films
df2[['title', 'cast', 'director', 'keywords', 'genres']].head(3)

"""The next step would be to convert the names and keyword instances into lowercase and strip all the spaces between them. This is done so that our vectorizer doesn't count the Johnny of "Johnny Depp" and "Johnny Galecki" as the same."""

# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

# Apply clean_data function to your features.
features = ['cast', 'keywords', 'director', 'genres']

for feature in features:
    df2[feature] = df2[feature].apply(clean_data)

"""We are now in a position to create our "metadata soup", which is a string that contains all the metadata that we want to feed to our vectorizer (namely actors, director and keywords)."""

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
df2['soup'] = df2.apply(create_soup, axis=1)

# Import CountVectorizer and create the count matrix
from sklearn.feature_extraction.text import CountVectorizer

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])

# Compute the Cosine Similarity matrix based on the count_matrix
from sklearn.metrics.pairwise import cosine_similarity

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# Reset index of our main DataFrame and construct reverse mapping as before
df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])

"""We can now reuse our **get_recommendations()** function by passing in the new **cosine_sim2** matrix as your second argument."""

get_recommendations('The Dark Knight Rises', cosine_sim2)

get_recommendations('The Godfather', cosine_sim2)