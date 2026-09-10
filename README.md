# Movie Genre Classification
A multi-label movie genre classification project using NLP and machine learning.

## Project Overview

This project predicts one or more movie genres from a movie description.

Since a movie can belong to multiple genres, the problem is treated as a multi-label classification task.

## Dataset

The dataset was collected using the TMDB API.

After cleaning:

- 8,985 movies
- 19 genres
- Movie descriptions (`overview`) used as input
- Multiple genres allowed per movie

## Data Preprocessing

The following preprocessing steps were performed:

- Removed duplicate movie IDs
- Removed movies with missing descriptions or genres
- Converted text to lowercase
- Removed special characters
- Normalized whitespace
- Converted multiple genres into multi-hot encoded labels

## Models

Two approaches were explored:

### 1. TF-IDF + Logistic Regression

- TF-IDF feature extraction
- Unigrams and bigrams
- One-vs-Rest Logistic Regression
- Multi-label genre prediction
- Classification threshold optimized using validation data

### 2. BiLSTM

A Bidirectional LSTM model was also experimented with using trainable word embeddings.

The BiLSTM showed signs of overfitting, so the TF-IDF + Logistic Regression model was selected as the final production model.

## Results

The final TF-IDF + One-vs-Rest Logistic Regression model achieved the following results on the test set:

| Metric | Score |
|---|---:|
| Micro F1 | 0.57 |
| Macro F1 | 0.37 |
| Precision | 0.53 |
| Recall | 0.61 |
| Hamming Loss | 0.12 |

The classification threshold was optimized from the default 0.50 to 0.25, improving the overall Micro F1 score.

##  Application

The Streamlit application accepts a movie description and predicts its relevant genres.


Movie Description
       ↓
Text Cleaning
       ↓
TF-IDF Vectorization
       ↓
One-vs-Rest Logistic Regression
       ↓
Threshold = 0.25
       ↓
Predicted Genres


## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- PyTorch
- Streamlit
- Jupyter Notebook
- TMDB API
- Git & GitHub

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Divyanshu-Kumar-ML/movie-genre-classification.git
cd movie-genre-classification

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/app.py

```
##  Author

**Divyanshu Kumar**
