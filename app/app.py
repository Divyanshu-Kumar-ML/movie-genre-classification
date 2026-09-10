import re
from pathlib import Path

import joblib
import streamlit as st


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"


# --------------------------------------------------
# Load trained model artifacts
# --------------------------------------------------

model = joblib.load(
    MODEL_DIR / "tfidf_logistic_model.pkl"
)

tfidf = joblib.load(
    MODEL_DIR / "tfidf_vectorizer.pkl"
)

genres = joblib.load(
    MODEL_DIR / "genres.pkl"
)

threshold = joblib.load(
    MODEL_DIR / "threshold.pkl"
)


# --------------------------------------------------
# Text preprocessing
# --------------------------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# --------------------------------------------------
# Genre prediction
# --------------------------------------------------

def predict_genres(description):

    cleaned_description = clean_text(description)

    text_tfidf = tfidf.transform(
        [cleaned_description]
    )

    probabilities = model.predict_proba(
        text_tfidf
    )[0]

    predicted_genres = [
        genres[i]
        for i, probability in enumerate(probabilities)
        if probability >= threshold
    ]

    return predicted_genres


# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------

st.set_page_config(
    page_title="Movie Genre Classifier",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Genre Classifier")

st.write(
    "Enter a movie description to predict its genres "
    "using a machine learning model."
)


# --------------------------------------------------
# Input
# --------------------------------------------------

description = st.text_area(
    "Movie Description",
    placeholder=(
        "Example: A detective investigates a "
        "mysterious murder..."
    ),
    height=150
)


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if st.button("Predict Genres"):

    if not description.strip():

        st.warning(
            "Please enter a movie description."
        )

    else:

        predicted_genres = predict_genres(
            description
        )

        if predicted_genres:

            st.subheader("Predicted Genres")

            for genre in predicted_genres:
                st.write(f"🎬 {genre}")

        else:

            st.warning(
                "No genre was predicted."
            )


# --------------------------------------------------
# Model Information
# --------------------------------------------------

st.divider()

st.subheader("About the Model")

st.write(
    "Model: TF-IDF + One-vs-Rest Logistic Regression"
)

st.write(
    "Task: Multi-label movie genre classification"
)

st.write(
    f"Number of genres: {len(genres)}"
)

st.write(
    f"Classification threshold: {threshold:.2f}"
)